from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from decimal import Decimal
from re import sub


db = SQLAlchemy()


class Locacao(db.Model):
    __tablename__ = 'locacoes'

    id = db.Column(db.Integer, primary_key=True)
    contrato = db.Column(db.String(255))
    processo = db.Column(db.String(255))
    fornecedor = db.Column(db.String(255))
    objeto = db.Column(db.Text(255))
    valor_total = db.Column(db.String(255))
    modalidade = db.Column(db.String(255))
    assinatura = db.Column(db.String(255))
    inicio = db.Column(db.String(255))
    termino = db.Column(db.String(255))
    qtde_meses = db.Column(db.String(255))

    @staticmethod
    def count_contratos():
        total_contratos = db.engine.execute("select count(contrato) as total from locacoes").fetchone()

        return total_contratos[0]

    @staticmethod
    def count_forcedores():
        total_fornecedores = db.engine.execute("select count(distinct(fornecedor)) as total from locacoes").fetchone()

        return total_fornecedores[0]

    @staticmethod
    def valor_total_contratos():
        valores = db.engine.execute("select valor_total from locacoes where length(valor_total) > 0")
        total = 0

        for valor in valores:
            total += Decimal(sub(',', '.', sub(r'[^\d,]', '', valor[0])))

        return total

    @staticmethod
    def total_contratos_ativos():
        total_contratos = db.engine.execute(
            "select count(contrato) as total from locacoes where termino >= date()").fetchone()

        return total_contratos[0]

    @staticmethod
    def contratos_por_ano():
        result = []
        anos = db.engine.execute("select strftime('%Y', assinatura) as ano, count(contrato) as total "
                                 "from locacoes group by strftime('%Y', assinatura)")

        for ano in anos:
            result.append({
                "ano": ano[0],
                "total": ano[1]
            })

        return result
