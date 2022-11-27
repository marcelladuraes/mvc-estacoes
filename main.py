'''
from flask import Flask
from flask_restful import reqparse, Api, Resource, fields
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from marshmallow import fields

app = Flask(__name__)
postgresql = False
if not postgresql:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:enmvst1c@localhost/estacoes'
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


class Estacao(Resource):
    def get(self, id):
        estacao = EstacaoDataBase.query.get(id)
        estacao_schema = EstacaoDataBaseSchema()
        resp = estacao_schema.dump(estacao)
        return {"estação": resp}, 200 

    def delete(self, id):
        estacao = EstacaoDataBase.query.get(id)
        db.session.delete(estacao)
        db.session.commit()
        return '', 204 

    def put(self, id):
        estacao_json = parser.parse_args()
        estacao = EstacaoDataBase.query.get(id)

        if estacao_json.get('nome_estacao'):
            estacao.nome_estacao = estacao_json.nome_estacao
        if estacao_json.get('uf'):
            estacao.uf = estacao_json.uf
        if estacao_json.get('latitude'):
            estacao.latitude = estacao_json.latitude
        if estacao_json.get('longitutde'):
            estacao.longitude = estacao_json.longitude
        if estacao_json.get('altitude'):
            estacao.altitude = estacao_json.altitude
        if estacao_json.get('data_fundacao'):
            estacao.data_fundacao = estacao_json.data_fundacao
        if estacao_json.get('codigo_wmo'):
            estacao.codigo_wmo = estacao_json.codigo_wmo
        
        db.session.add(estacao)
        db.session.commit()

        estacao_schema = EstacaoDataBaseSchema(only=['id_estacao', 'nome_estacao', 'uf', 'latitude', 'longitude', 'altitude' , 'data_fundacao', 'codigo_wmo'])
        resp = estacao_schema.dump(estacao)
    
        return {"estação": resp}, 200 

class ListaEstacao(Resource):
    def get(self):
        estacoes = EstacaoDataBase.query.all()
        estacao_schema = EstacaoDataBaseSchema(many=True) 
        resp = estacao_schema.dump(estacoes)
        return {"estacao": resp}, 200 

    def post(self):
        estacao_json = parser.parse_args()
        estacao_schema = EstacaoDataBaseSchema()
        estacao = estacao_schema.load(estacao_json)
        estacaoDataBase = EstacaoDataBase(estacao['id_estacao'], estacao['nome_estacao'], estacao['uf'], estacao['latitude'], estacao['longitude'], estacao['altitude'], estacao['data_fundacao'], estacao['codigo_wmo'])
        resp = estacao_schema.dump(estacaoDataBase.create())
        return {"estacao": resp}, 201 

api.add_resource(Estacao, '/api/v1/estacoes/<id>')
api.add_resource(ListaEstacao, '/api/v1/estacoes')
'''
from app.controller.controller import Estacao, ListaEstacao, app, api, db
if __name__ == '__main__':
    api.add_resource(Estacao, '/api/v1/estacoes/<id>')
    api.add_resource(ListaEstacao, '/api/v1/estacoes')
    with app.app_context():
        db.create_all()
    app.run(debug=True)