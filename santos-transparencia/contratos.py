import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.http import FormRequest
import urllib.parse
import os
from multiprocessing import Process, Queue
from twisted.internet import reactor
from settings import CONTRATOS_PATH, DB_PATH
import csv
import sqlite3
import time
import datetime


class ContratosSpider(scrapy.Spider):
    url_base = 'https://egov.santos.sp.gov.br/sigecon/transparencia/contrato.xhtml'
    file_name = 'contratos.csv'

    def __init__(self):
        self.start_urls = [self.url_base]

    def parse(self, response):
        view_state = response.xpath("//input[@id='javax.faces.ViewState']/@value")[0].extract()

        return [FormRequest(url=self.url_base,
                            method="POST",
                            callback=self.save_file,
                            formdata={
                                "formContrato": "formContrato",
                                "formContrato:txtFornecedor": "",
                                "formContrato:txtContrato": "",
                                "formContrato:txtProcesso": "",
                                "formContrato:combotiposervico_focus": "",
                                "formContrato:combotiposervico_input": "",
                                "formContrato:combomodalidade_focus": "",
                                "formContrato:combomodalidade_input": "",
                                "formContrato:situacaoContrato": "vigente",
                                "formContrato:contratoTable_rppDD": "10",
                                "formContrato:contratoTable_rppDD": "10",
                                "formContrato:btnEmitirContratosCSV": "",
                                "javax.faces.ViewState": view_state
                            })]

    def save_file(self, response):
        if os.path.isdir(CONTRATOS_PATH.absolute()):
            with open(os.path.join(CONTRATOS_PATH.absolute(), self.file_name), 'wb') as f:
                f.write(response.body)

        self.save_to_db()

    def save_to_db(self):
        con = sqlite3.connect(os.path.join(DB_PATH.absolute(), 'santos-transparencia.db'))
        cur = con.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS contratos (id integer primary key AUTOINCREMENT NOT NULL, "
                    "contrato TEXT, "
                    "processo TEXT, "
                    "fornecedor TEXT, "
                    "objeto TEXT, "
                    "valor_total TEXT, "
                    "tipo_servico TEXT, "
                    "modalidade TEXT, "
                    "assinatura TEXT, "
                    "inicio TEXT, "
                    "termino TEXT);")
        cur.execute("CREATE UNIQUE INDEX IF NOT EXISTS idx_contrato ON contratos(contrato);")

        with open(os.path.join(CONTRATOS_PATH.absolute(), self.file_name), encoding='ISO-8859-1') as fin:
            next(fin, None)     # skipping first row of file

            dr = csv.DictReader(fin, delimiter=';')
            to_db = [(i['Contrato'],
                      i['Processo'],
                      i['Fornecedor'],
                      i['Objeto'],
                      i['Valor total'],
                      i['Tipo serviço'],
                      i['Modalidade licitação'],
                      self.convert_date(i['Assinatura']),
                      self.convert_date(i['Início']),
                      self.convert_date(i['Término']),
                      ) for i in dr]

        cur.executemany("INSERT OR REPLACE INTO contratos ("
                        "contrato, "
                        "processo, "
                        "fornecedor, "
                        "objeto, "
                        "valor_total,"
                        "tipo_servico, "
                        "modalidade, "
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
        deferred = runner.crawl(ContratosSpider)
        deferred.addBoth(lambda _: reactor.stop())
        reactor.run()
        q.put(None)
    except Exception as e:
        q.put(e)


def get_contratos():
    q = Queue()
    p = Process(target=run_spider, args=(q,))
    p.start()
    q.get()
    p.join()


def main():
    get_contratos()


if __name__ == '__main__':
    main()
