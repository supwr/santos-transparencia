from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from decimal import Decimal
from re import sub


db = SQLAlchemy()


class Convenio(db.Model):
    __tablename__ = 'convenios'

    id = db.Column(db.Integer, primary_key=True)
    numero = db.Column(db.String(255))
    tipo = db.Column(db.String(255))
    processo = db.Column(db.String(255))
    unidade = db.Column(db.Text(255))
    fornecedor = db.Column(db.String(255))
    objeto = db.Column(db.String(255))
    valor_total = db.Column(db.String(255))
    assinatura = db.Column(db.String(255))
    inicio = db.Column(db.String(255))
    termino = db.Column(db.String(255))

    @staticmethod
    def count_convenios():
        total_convenios = db.engine.execute("select count(numero) as total from convenios").fetchone()

        return total_convenios[0]

    @staticmethod
    def count_forcedores():
        total_fornecedores = db.engine.execute("select count(distinct(fornecedor)) as total from convenios").fetchone()

        return total_fornecedores[0]

    @staticmethod
    def valor_total_convenios():
        valores = db.engine.execute("select valor_total from convenios where length(valor_total) > 0")
        total = 0

        for valor in valores:
            total += Decimal(sub(',', '.', sub(r'[^\d,]', '', valor[0])))

        return total

    @staticmethod
    def total_convenios_ativos():
        total_convenios = db.engine.execute(
            "select count(numero) as total from convenios where termino >= date()").fetchone()

        return total_convenios[0]

    @staticmethod
    def convenios_por_unidade():
        result_data = []
        result_labels = []

        unidades = db.engine.execute("select unidade, count(numero) as total "
                                     "from convenios where length(unidade) > 0 group by unidade order by total desc  limit 5")

        for unidade in unidades:
            result_data.append(unidade[1])
            result_labels.append(unidade[0])

        return {"data": result_data, "labels": result_labels}

    @staticmethod
    def convenios_mais_caros():
        result = []
        fornecedores = db.engine.execute(
            "select "
            "cast(replace(replace(replace(valor_total, 'R$ ', ''), '.', ''), ',', '.') as real) as valor"
            ",valor_total, fornecedor, objeto from convenios where length(valor_total) > 0 order by valor desc limit 10"
        )

        for fornecedor in fornecedores:
            result.append({
                "valor_total": fornecedor[1],
                "fornecedor": fornecedor[2],
                "objeto": fornecedor[3]
            })

        return result
