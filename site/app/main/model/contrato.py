from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from decimal import Decimal
from re import sub


db = SQLAlchemy()


class Contrato(db.Model):
    __tablename__ = 'contratos'

    id = db.Column(db.Integer, primary_key=True)
    contrato = db.Column(db.String(255))
    processo = db.Column(db.String(255))
    fornecedor = db.Column(db.String(255))
    objeto = db.Column(db.Text(255))
    valor_total = db.Column(db.String(255))
    tipo_servico = db.Column(db.String(255))
    modalidade = db.Column(db.String(255))
    assinatura = db.Column(db.String(255))
    inicio = db.Column(db.String(255))
    termino = db.Column(db.String(255))

    @staticmethod
    def count_contratos():
        total_contratos = db.engine.execute("select count(contrato) as total from contratos").fetchone()

        return total_contratos[0]

    @staticmethod
    def count_forcedores():
        total_fornecedores = db.engine.execute("select count(distinct(fornecedor)) as total from contratos").fetchone()

        return total_fornecedores[0]

    @staticmethod
    def valor_total_contratos():
        valores = db.engine.execute("select valor_total from contratos where length(valor_total) > 0")
        total = 0

        for valor in valores:
            total += Decimal(sub(',', '.', sub(r'[^\d,]', '', valor[0])))

        return total

    @staticmethod
    def total_contratos_ativos():
        total_contratos = db.engine.execute("select count(contrato) as total from contratos where termino >= date()").fetchone()

        return total_contratos[0]

    @staticmethod
    def contratos_por_ano():
        result = []
        anos = db.engine.execute("select strftime('%Y', assinatura) as ano, count(contrato) as total "
                                    "from contratos group by strftime('%Y', assinatura)")

        for ano in anos:
            result.append({
                "ano": ano[0],
                "total": ano[1]
            })

        return result

    @staticmethod
    def top_dez_fornecedores():
        result = []
        fornecedores = db.engine.execute("select count(contrato) as total, "
                                 "fornecedor from contratos group by fornecedor order by total desc limit 10")

        for fornecedor in fornecedores:
            result.append({
                "total": fornecedor[0],
                "fornecedor": fornecedor[1]
            })

        return result
