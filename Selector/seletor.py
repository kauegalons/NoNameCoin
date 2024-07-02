from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dataclasses import dataclass
from datetime import datetime, timedelta
import requests
import random

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///seletor.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

@dataclass
class Transacao(db.Model):
    id: int
    remetente: int
    recebedor: int
    valor: int
    horario: datetime
    status: int

    id = db.Column(db.Integer, primary_key=True)
    remetente = db.Column(db.Integer, nullable=False)
    recebedor = db.Column(db.Integer, nullable=False)
    valor = db.Column(db.Integer, nullable=False)
    horario = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.Integer, nullable=False, default=0)

@dataclass
class Validador(db.Model):
    id: int
    chave: str
    flag: int = 0
    hold: int = 0
    qtdMoeda: int

    id = db.Column(db.Integer, primary_key=True)
    chave = db.Column(db.String(100), nullable=False)
    flag = db.Column(db.Integer, nullable=False, default=0)
    hold = db.Column(db.Integer, nullable=False, default=0)
    qtdMoeda = db.Column(db.Integer, nullable=False)

with app.app_context():
    db.create_all()

@app.route("/")
def index():
    return jsonify(['Seletor ativo!'])

@app.route('/seletor/validadores', methods=['POST'])
def cadastrar_validador():
    dados = request.get_json()
    chave = dados.get('chave')
    qtdMoeda = dados.get('qtdMoeda')

    if not chave or not qtdMoeda:
        return jsonify({'message': 'Dados incompletos'}), 400
    
    if qtdMoeda < 50:
        return jsonify({'message': 'Saldo mínimo para cadastro é 50 NoNameCoins'}), 400

    validador = Validador(chave=chave, qtdMoeda=qtdMoeda)
    db.session.add(validador)
    db.session.commit()
    return jsonify(validador)

@app.route('/seletor/transacoes/<int:transacao_id>', methods=['POST'])
def selecionar_validadores(transacao_id):
    transacao = Transacao.query.get(transacao_id)

    if not transacao:
        return jsonify({'message': 'Transação não encontrada'}), 404
    
    validadores = Validador.query.filter(Validador.flag < 3, Validador.hold == 0).all()
    if len(validadores) < 3:
        transacao.horario = datetime.now() + timedelta(minutes=1)
        db.session.commit()
        return jsonify({'message': 'Transação em espera, não há validadores suficientes'}), 200

    selecao_validadores = random.choices(validadores, k=3)

    resultados = []
    for validador in selecao_validadores:
        url = f"http://{validador.chave}/transacoes"
        resposta = requests.post(url, json={'id': transacao_id})
        if resposta.status_code == 200:
            resultados.append(resposta.json())

    consensos = [resultado['status'] for resultado in resultados if 'status' in resultado]
    if consensos.count(1) > 1:
        transacao.status = 1
        # Distribui a taxa entre os validadores
        taxa = transacao.valor * 0.015
        for validador in selecao_validadores:
            validador.qtdMoeda += taxa / 3
        db.session.commit()
        return jsonify({'message': 'Transação validada com sucesso', 'transacao': transacao}), 200
    else:
        transacao.status = 2
        db.session.commit()
        return jsonify({'message': 'Transação não validada', 'transacao': transacao}), 200

@app.route('/seletor/flag/<int:validador_id>', methods=['POST'])
def adicionar_flag(validador_id):
    validador = Validador.query.get(validador_id)
    if not validador:
        return jsonify({'message': 'Validador não encontrado'}), 404
    
    validador.flag += 1
    if validador.flag > 2:
        db.session.delete(validador)
        db.session.commit()
        return jsonify({'message': 'Validador removido da rede'}), 200

    db.session.commit()
    return jsonify({'message': 'Flag adicionada ao validador', 'flag': validador.flag}), 200

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5002, debug=True)
