from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dataclasses import dataclass
from datetime import datetime
import requests

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///validador.db'
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
    status = db.Column(db.Integer, nullable=False)

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
    return jsonify(['Validador ativo!'])

@app.route('/validador/<string:chave>/<int:qtdMoeda>', methods=['POST'])
def cadastrar_validador(chave, qtdMoeda):
    if request.method == 'POST':
        if qtdMoeda < 50:
            return jsonify({'message': 'Saldo mínimo para cadastro é 50 NoNameCoins'}), 400
        
        validador = Validador(chave=chave, qtdMoeda=qtdMoeda)
        db.session.add(validador)
        db.session.commit()
        return jsonify(validador)
    else:
        return jsonify(['Method Not Allowed'])

@app.route('/transacoes', methods=['POST'])
def validar_transacao():
    if request.method == 'POST':
        dados = request.get_json()
        transacao = Transacao.query.get(dados['id'])
        
        if not transacao:
            return jsonify({'status': 2, 'message': 'Transação não encontrada'}), 404

        # Simula a validação (pode ser estendido conforme regras)
        remetente = id.query.get(transacao.remetente)
        recebedor = id.query.get(transacao.recebedor)

        if not remetente or not recebedor:
            transacao.status = 2
            db.session.commit()
            return jsonify({'status': 2, 'message': 'Cliente não encontrado'}), 404

        if remetente.qtdMoeda < transacao.valor:
            transacao.status = 2
            db.session.commit()
            return jsonify({'status': 2, 'message': 'Saldo insuficiente'}), 400

        # Atualiza o saldo do remetente e recebedor
        remetente.qtdMoeda -= transacao.valor
        recebedor.qtdMoeda += transacao.valor

        transacao.status = 1
        db.session.commit()
        return jsonify({'status': 1, 'message': 'Transação validada com sucesso'}), 200
    else:
        return jsonify(['Method Not Allowed'])

@app.route('/transacoes/flag/<int:id>', methods=['POST'])
def adicionar_flag(id):
    if request.method == 'POST':
        validador = Validador.query.get(id)
        if not validador:
            return jsonify({'message': 'Validador não encontrado'}), 404
        
        validador.flag += 1
        if validador.flag > 2:
            db.session.delete(validador)
            db.session.commit()
            return jsonify({'message': 'Validador removido da rede'}), 200

        db.session.commit()
        return jsonify({'message': 'Flag adicionada ao validador', 'flag': validador.flag}), 200
    else:
        return jsonify(['Method Not Allowed'])

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5001, debug=True)
