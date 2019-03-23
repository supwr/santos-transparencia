from flask import Flask, request, send_from_directory, render_template
from flask_sqlalchemy import SQLAlchemy
from main.model.contrato import Contrato
from main.model.locacao import Locacao
from main.model.convenio import Convenio
import locale
from pathlib import Path
from re import sub
import time
import datetime


locale.setlocale(locale.LC_ALL, 'pt_BR.utf8')

DB_PATH = Path(__file__).parent.parent.parent.parent

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///%s/db/santos-transparencia.db' % DB_PATH
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy()
db.init_app(app)


@app.template_filter('strip_cnpj')
def strip_cnpj(fornecedor):
    return sub(',', '.', sub(r'[\d-]', '', fornecedor))


@app.template_filter('convert_date')
def convert_date(str_date):
    if str_date is None or len(str_date) == 0:
        return ""
    try:
        date = datetime.datetime.strptime(str_date, '%Y-%m-%d').strftime('%d/%m/%Y')
        return date
    except:
        return ""


@app.route('/')
@app.route('/contratos')
def contratos():
    contratos = Contrato.query.all()
    total_contratos = Contrato.count_contratos()
    total_fornecedores = Contrato.count_forcedores()
    valor_total = Contrato.valor_total_contratos()
    total_contratos_ativos = Contrato.total_contratos_ativos()
    top_dez_fornecedores = Contrato.top_dez_fornecedores()

    chart_labels = []
    chart_data = []

    for contrato_por_ano in Contrato.contratos_por_ano():
        chart_labels.append(contrato_por_ano["ano"])
        chart_data.append(contrato_por_ano["total"])

    contratos_por_ano = {
        "labels": chart_labels,
        "datasets": [{
            "label": '# de Contratos',
            "data": chart_data,
            "backgroundColor": [
                'rgba(255, 99, 132, 0.2)',
                'rgba(54, 162, 235, 0.2)',
                'rgba(255, 206, 86, 0.2)',
                'rgba(75, 192, 192, 0.2)',
                'rgba(153, 102, 255, 0.2)',
                'rgba(255, 159, 64, 0.2)',
                'rgba(255, 99, 132, 0.2)',
                'rgba(54, 162, 235, 0.2)',
                'rgba(255, 206, 86, 0.2)',
                'rgba(75, 192, 192, 0.2)',
                'rgba(153, 102, 255, 0.2)',
                'rgba(255, 159, 64, 0.2)',
                'rgba(255, 99, 132, 0.2)',
                'rgba(54, 162, 235, 0.2)',
                'rgba(255, 206, 86, 0.2)',
                'rgba(75, 192, 192, 0.2)',
                'rgba(153, 102, 255, 0.2)',
                'rgba(255, 159, 64, 0.2)',
                'rgba(255, 99, 132, 0.2)',
                'rgba(54, 162, 235, 0.2)',
                'rgba(255, 206, 86, 0.2)',
                'rgba(75, 192, 192, 0.2)',
                'rgba(153, 102, 255, 0.2)',
                'rgba(255, 159, 64, 0.2)'
            ],
            "borderColor": [
                'rgba(255,99,132,1)',
                'rgba(54, 162, 235, 1)',
                'rgba(255, 206, 86, 1)',
                'rgba(75, 192, 192, 1)',
                'rgba(153, 102, 255, 1)',
                'rgba(255, 159, 64, 1)',
                'rgba(255,99,132,1)',
                'rgba(54, 162, 235, 1)',
                'rgba(255, 206, 86, 1)',
                'rgba(75, 192, 192, 1)',
                'rgba(153, 102, 255, 1)',
                'rgba(255, 159, 64, 1)',
                'rgba(255,99,132,1)',
                'rgba(54, 162, 235, 1)',
                'rgba(255, 206, 86, 1)',
                'rgba(75, 192, 192, 1)',
                'rgba(153, 102, 255, 1)',
                'rgba(255, 159, 64, 1)',
                'rgba(255,99,132,1)',
                'rgba(54, 162, 235, 1)',
                'rgba(255, 206, 86, 1)',
                'rgba(75, 192, 192, 1)',
                'rgba(153, 102, 255, 1)',
                'rgba(255, 159, 64, 1)'
            ],
            "borderWidth": 1
        }]
    }

    return render_template("contratos/index.html",
                           contratos=contratos,
                           total_contratos=total_contratos,
                           total_fornecedores=total_fornecedores,
                           valor_total="R$ ~{0:n}".format(valor_total),
                           total_contratos_ativos=total_contratos_ativos,
                           contratos_por_ano=contratos_por_ano,
                           top_dez_fornecedores=top_dez_fornecedores
                           )


@app.route('/locacoes')
def locacoes():
    locacoes = Locacao.query.all()
    total_contratos = Locacao.count_contratos()
    total_fornecedores = Locacao.count_forcedores()
    valor_total = Locacao.valor_total_contratos()
    total_contratos_ativos = Locacao.total_contratos_ativos()

    chart_labels = []
    chart_data = []

    for contrato_por_ano in Locacao.contratos_por_ano():
        chart_labels.append(contrato_por_ano["ano"])
        chart_data.append(contrato_por_ano["total"])

    contratos_por_ano = {
        "labels": chart_labels,
        "datasets": [{
            "label": '# de Contratos',
            "data": chart_data,
            "backgroundColor": [
                'rgba(255, 99, 132, 0.2)',
                'rgba(54, 162, 235, 0.2)',
                'rgba(255, 206, 86, 0.2)',
                'rgba(75, 192, 192, 0.2)',
                'rgba(153, 102, 255, 0.2)',
                'rgba(255, 159, 64, 0.2)',
                'rgba(255, 99, 132, 0.2)',
                'rgba(54, 162, 235, 0.2)',
                'rgba(255, 206, 86, 0.2)',
                'rgba(75, 192, 192, 0.2)',
                'rgba(153, 102, 255, 0.2)',
                'rgba(255, 159, 64, 0.2)',
                'rgba(255, 99, 132, 0.2)',
                'rgba(54, 162, 235, 0.2)',
                'rgba(255, 206, 86, 0.2)',
                'rgba(75, 192, 192, 0.2)',
                'rgba(153, 102, 255, 0.2)',
                'rgba(255, 159, 64, 0.2)',
                'rgba(255, 99, 132, 0.2)',
                'rgba(54, 162, 235, 0.2)',
                'rgba(255, 206, 86, 0.2)',
                'rgba(75, 192, 192, 0.2)',
                'rgba(153, 102, 255, 0.2)',
                'rgba(255, 159, 64, 0.2)'
            ],
            "borderColor": [
                'rgba(255,99,132,1)',
                'rgba(54, 162, 235, 1)',
                'rgba(255, 206, 86, 1)',
                'rgba(75, 192, 192, 1)',
                'rgba(153, 102, 255, 1)',
                'rgba(255, 159, 64, 1)',
                'rgba(255,99,132,1)',
                'rgba(54, 162, 235, 1)',
                'rgba(255, 206, 86, 1)',
                'rgba(75, 192, 192, 1)',
                'rgba(153, 102, 255, 1)',
                'rgba(255, 159, 64, 1)',
                'rgba(255,99,132,1)',
                'rgba(54, 162, 235, 1)',
                'rgba(255, 206, 86, 1)',
                'rgba(75, 192, 192, 1)',
                'rgba(153, 102, 255, 1)',
                'rgba(255, 159, 64, 1)',
                'rgba(255,99,132,1)',
                'rgba(54, 162, 235, 1)',
                'rgba(255, 206, 86, 1)',
                'rgba(75, 192, 192, 1)',
                'rgba(153, 102, 255, 1)',
                'rgba(255, 159, 64, 1)'
            ],
            "borderWidth": 1
        }]
    }

    return render_template("locacoes/index.html",
                           locacoes=locacoes,
                           total_contratos=total_contratos,
                           total_fornecedores=total_fornecedores,
                           valor_total="R$ ~{0:n}".format(valor_total),
                           total_contratos_ativos=total_contratos_ativos,
                           contratos_por_ano=contratos_por_ano
                           )


@app.route('/convenios')
def convenios():
    convenios = Convenio.query.all()
    total_convenios = Convenio.count_convenios()
    total_fornecedores = Convenio.count_forcedores()
    valor_total = Convenio.valor_total_convenios()
    total_convenios_ativos = Convenio.total_convenios_ativos()
    convenios_por_unidade = Convenio.convenios_por_unidade()
    convenios_mais_caros = Convenio.convenios_mais_caros()

    return render_template("convenios/index.html",
                           convenios=convenios,
                           total_convenios=total_convenios,
                           total_fornecedores=total_fornecedores,
                           valor_total="R$ ~{0:n}".format(valor_total),
                           total_convenios_ativos=total_convenios_ativos,
                           convenios_por_unidade_labels=convenios_por_unidade["labels"],
                           convenios_por_unidade_data=convenios_por_unidade["data"],
                           convenios_mais_caros=convenios_mais_caros
                           )


