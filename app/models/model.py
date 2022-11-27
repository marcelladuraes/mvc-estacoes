from flask import Flask
from flask_restful import reqparse, Api, Resource, fields
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from marshmallow import fields
from app.models.connection import user, password, database

app = Flask(__name__)
postgresql = False
if not postgresql:
    app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql://{user}:{password}@localhost/{database}'
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1234@localhost/postgres'

db = SQLAlchemy(app)
marshmallow = Marshmallow(app)
CORS(app)

class EstacaoDataBase(db.Model):
    __tablename__ = "Catalogo"
    id_estacao = db.Column(db.Integer, primary_key = True)
    nome_estacao = db.Column(db.String(256), unique = True, nullable = False)
    uf = db.Column(db.String(256), nullable = False)
    latitude = db.Column(db.String(256), nullable = False)
    longitude = db.Column(db.String(256), nullable = False)
    altitude = db.Column(db.String(256), nullable = False)
    data_fundacao = db.Column(db.String(256), nullable = False)
    codigo_wmo = db.Column(db.String(256), nullable = False)

    def __init__(self, id_estacao, nome_estacao, uf, latitude, longitude, altitude, data_fundacao, codigo_wmo):
        self.id_estacao = id_estacao
        self.nome_estacao = nome_estacao
        self.uf = uf
        self.latitude = latitude
        self.longitude = longitude
        self.altitude = altitude
        self.data_fundacao = data_fundacao
        self.codigo_wmo = codigo_wmo

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    def __repr__(self):
        return f"{self.id_estacao, self.nome_estacao, self.uf, self.latitude, self.longitude, self.altitude, self.data_fundacao, self.codigo_wmo}"

class EstacaoDataBaseSchema(marshmallow.SQLAlchemyAutoSchema):
    class Meta:
        model = EstacaoDataBase
        sqla_session = db.session

    id_estacao = fields.Number()#dump_only=True)
    nome_estacao = fields.String(required=True)
    uf = fields.String(required=True)
    latitude =  fields.String(required=True)
    longitude = fields.String(required=True)
    altitude = fields.String(required=True)
    data_fundacao = fields.String(required=True)
    codigo_wmo = fields.String(required=True)

api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument('id_estacao', type=int, help='identificador da estação')
parser.add_argument('nome_estacao', type=str, help='nome da estação')
parser.add_argument('uf', type=str, help='UF da estação')
parser.add_argument('latitude', type=str, help='latitude da estação')
parser.add_argument('longitude', type=str, help='longitude da estação')
parser.add_argument('altitude', type=str, help='altitude da estação')
parser.add_argument('data_fundacao', type=str, help='data de fundação da estação')
parser.add_argument('codigo_wmo', type=str, help='código da estação')