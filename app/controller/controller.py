from app.models.model import EstacaoDataBaseSchema, EstacaoDataBase, parser, db, app, api
from flask import Flask
from flask_restful import reqparse, Api, Resource, fields
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from marshmallow import fields

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

        estacao_schema = EstacaoDataBaseSchema(
            only=['id_estacao', 'nome_estacao', 'uf', 'latitude', 'longitude', 'altitude', 'data_fundacao',
                  'codigo_wmo'])
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
        estacaoDataBase = EstacaoDataBase(estacao['id_estacao'], estacao['nome_estacao'], estacao['uf'],
                                          estacao['latitude'], estacao['longitude'], estacao['altitude'],
                                          estacao['data_fundacao'], estacao['codigo_wmo'])
        resp = estacao_schema.dump(estacaoDataBase.create())
        return {"estacao": resp}, 201
