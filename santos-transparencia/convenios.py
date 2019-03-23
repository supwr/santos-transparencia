import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.http import FormRequest
import urllib.parse
import os
from multiprocessing import Process, Queue
from twisted.internet import reactor
from settings import CONVENIOS_PATH, DB_PATH
import csv
import sqlite3
import time
import datetime


class ConveniosSpider(scrapy.Spider):
    url_base = 'https://egov.santos.sp.gov.br/sigecon/transparencia/convenio.xhtml'
    file_name = 'convenios.csv'

    CSV_COLUMNS = ['N°',
                   'Tipo',
                   'Processo',
                   'Unidade',
                   'Fornecedor',
                   'Objeto',
                   'Valor Total',
                   'Assinatura',
                   'Início',
                   'Término'
                ]

    def __init__(self):
        self.start_urls = [self.url_base]

    def parse(self, response):
        view_state = response.xpath("//input[@id='javax.faces.ViewState']/@value")[0].extract()

        return [FormRequest(url=self.url_base,
                            method="POST",
                            callback=self.save_file,
                            formdata={
                                "formConvenio": "formConvenio",
                                "formConvenio:txtFornecedor": "",
                                "formConvenio:txtNuInstrumento": "",
                                "formConvenio:comboTpInstrumento_focus": "",
                                "formConvenio:comboTpInstrumento_input": "",
                                "formConvenio:txtProcesso": "",
                                "formConvenio:txtOrgaoResponsavel": "",
                                "formConvenio:convenioTable_rppDD": "10",
                                "formConvenio:convenioTable_rppDD": "10",
                                "formConvenio:btnEmitirConveniosCSV": "",
                                "javax.faces.ViewState": view_state
                            })]

    def save_file(self, response):
        if os.path.isdir(CONVENIOS_PATH.absolute()):
            with open(os.path.join(CONVENIOS_PATH.absolute(), self.file_name), 'wb') as f:
                f.write(response.body)

        self.save_to_db()

    def save_to_db(self):
        con = sqlite3.connect(os.path.join(DB_PATH.absolute(), 'santos-transparencia.db'))
        cur = con.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS convenios (id integer primary key AUTOINCREMENT NOT NULL, "
                    "numero TEXT, "
                    "tipo TEXT, "
                    "processo TEXT, "
                    "unidade TEXT, "
                    "fornecedor TEXT, "
                    "objeto TEXT, "
                    "valor_total TEXT, "
                    "assinatura TEXT, "
                    "inicio TEXT, "
                    "termino TEXT);")
        cur.execute("CREATE UNIQUE INDEX IF NOT EXISTS idx_numero ON convenios(numero);")

        with open(os.path.join(CONVENIOS_PATH.absolute(), self.file_name), encoding='ISO-8859-1') as fin:
            next(fin, None)     # skipping first row of file

            dr = csv.DictReader(fin, delimiter=';')
            to_db = []

            for i in dr:
                if i['N°'] == 'N°':
                    continue

                to_db.append((i['N°'],
                          i['Tipo'],
                          i['Processo'],
                          i['Unidade'],
                          i['Fornecedor'],
                          i['Objeto'],
                          i['Valor Total'],
                          self.convert_date(i['Assinatura']),
                          self.convert_date(i['Início']),
                          self.convert_date(i['Término']),
                          ))

        cur.executemany("INSERT OR REPLACE INTO convenios ("
                        "numero, "
                        "tipo, "
                        "processo, "
                        "unidade, "
                        "fornecedor,"
                        "objeto, "
                        "valor_total, "
                        "assinatura, "
                        "inicio, "
                        "termino"
                        ") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);", to_db)
        con.commit()
        con.close()

    def convert_date(self, str_date):
        if len(str_date) == 0:
            return None

        date = datetime.datetime.strptime(str_date, '%d/%m/%Y').strftime('%Y-%m-%d')
        return date


def run_spider(q):
    try:
        runner = scrapy.crawler.CrawlerRunner()
        deferred = runner.crawl(ConveniosSpider)
        deferred.addBoth(lambda _: reactor.stop())
        reactor.run()
        q.put(None)
    except Exception as e:
        q.put(e)


def get_convenios():
    q = Queue()
    p = Process(target=run_spider, args=(q,))
    p.start()
    q.get()
    p.join()


def main():
    get_convenios()


if __name__ == '__main__':
    main()
