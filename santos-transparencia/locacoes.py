import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.http import FormRequest
import urllib.parse
import os
from multiprocessing import Process, Queue
from twisted.internet import reactor
from settings import LOCACOES_PATH, DB_PATH
import csv
import sqlite3
import time
import datetime


class LocacoesSpider(scrapy.Spider):
    url_base = 'https://egov.santos.sp.gov.br/sigecon/transparencia/locacao.xhtml'
    file_name = 'locacoes.csv'

    def __init__(self):
        self.start_urls = [self.url_base]

    def parse(self, response):
        view_state = response.xpath("//input[@id='javax.faces.ViewState']/@value")[0].extract()

        return [FormRequest(url=self.url_base,
                            method="POST",
                            callback=self.save_file,
                            formdata={
                                "formLocacao": "formLocacao",
                                "formLocacao:txtFornecedor": "",
                                "formLocacao:txtContrato": "",
                                "formLocacao:txtProcesso": "",
                                "formLocacao:combomodalidade_focus": "",
                                "formLocacao:combomodalidade_input": "",
                                "formLocacao:locacaoTable_rppDD": "10",
                                "formLocacao:locacaoTable_rppDD": "10",
                                "formLocacao:btnEmitirLocacoesCSV": "",
                                "javax.faces.ViewState": view_state
                            })]

    def save_file(self, response):
        if os.path.isdir(LOCACOES_PATH.absolute()):
            with open(os.path.join(LOCACOES_PATH.absolute(), self.file_name), 'wb') as f:
                f.write(response.body)

        self.save_to_db()

    def save_to_db(self):
        con = sqlite3.connect(os.path.join(DB_PATH.absolute(), 'santos-transparencia.db'))
        cur = con.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS locacoes (id integer primary key AUTOINCREMENT NOT NULL, "
                    "contrato TEXT, "
                    "processo TEXT, "
                    "fornecedor TEXT, "
                    "objeto TEXT, "
                    "valor_total TEXT, "                
                    "modalidade TEXT, "
                    "assinatura TEXT, "
                    "inicio TEXT, "
                    "termino TEXT,"
                    "qtde_meses TEXT"
                    ");")
        cur.execute("CREATE UNIQUE INDEX IF NOT EXISTS idx_contrato ON locacoes(contrato);")

        with open(os.path.join(LOCACOES_PATH.absolute(), self.file_name), encoding='ISO-8859-1') as fin:
            next(fin, None)     # skipping first row of file

            dr = csv.DictReader(fin, delimiter=';')
            to_db = [(i['Contrato'],
                      i['Processo'],
                      i['Fornecedor'],
                      i['Objeto'],
                      i['Valor total'],
                      i['Modalidade Licitaçao'],
                      self.convert_date(i['Assinatura']),
                      self.convert_date(i['Inicio']),
                      self.convert_date(i['Término']),
                      i['Qtde Meses'],
                      ) for i in dr]

        cur.executemany("INSERT OR REPLACE INTO locacoes ("
                        "contrato, "
                        "processo, "
                        "fornecedor, "
                        "objeto, "
                        "valor_total,"                    
                        "modalidade, "
                        "assinatura, "
                        "inicio, "
                        "termino,"
                        "qtde_meses"
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
        deferred = runner.crawl(LocacoesSpider)
        deferred.addBoth(lambda _: reactor.stop())
        reactor.run()
        q.put(None)
    except Exception as e:
        q.put(e)


def get_imoveis():
    q = Queue()
    p = Process(target=run_spider, args=(q,))
    p.start()
    q.get()
    p.join()


def main():
    get_imoveis()


if __name__ == '__main__':
    main()
