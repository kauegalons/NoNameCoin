from time import time
from flask import Flask, request, redirect, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dataclasses import dataclass
from datetime import date, datetime
import requests

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

@dataclass
class Cliente(db.Model):
    id: int
    nome: str
    senha: int
    qtdMoeda: float

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(20), unique=False, nullable=False)
    senha = db.Column(db.String(20), unique=False, nullable=False)
    qtdMoeda = db.Column(db.Float, unique=False, nullable=False)
@dataclass
class Seletor(db.Model):
    id: int
    nome: str
    ip: str
    stake: float
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(20), unique=False, nullable=False)
    ip = db.Column(db.String(15), unique=False, nullable=False)
    stake = db.Column(db.Float, unique=False, nullable=False)

@dataclass
class Transacao(db.Model):
    id: int
    remetente: int
    recebedor: int
    valor: int
    horario : datetime
    status: int
    
    id = db.Column(db.Integer, primary_key=True)
    remetente = db.Column(db.Integer, unique=False, nullable=False)
    recebedor = db.Column(db.Integer, unique=False, nullable=False)
    valor = db.Column(db.Integer, unique=False, nullable=False)
    horario = db.Column(db.DateTime, unique=False, nullable=False)
    status = db.Column(db.Integer, unique=False, nullable=False)
    def __repr__(self):
        return f'<Transacao {self.id}>'

with app.app_context():
    db.create_all()

@app.route("/")
def index():
    return jsonify(['API sem interface do banco!'])

# cliente
@app.route('/cliente', methods = ['GET'])
def ListarCliente():
    if(request.method == 'GET'):
        clientes = Cliente.query.all()
        return jsonify(clientes)  

@app.route('/cliente/<string:nome>/<string:senha>/<int:qtdMoeda>', methods = ['POST'])
def InserirCliente(nome, senha, qtdMoeda):
    if request.method=='POST' and nome != '' and senha != '' and qtdMoeda != '':
        objeto = Cliente(nome=nome, senha=senha, qtdMoeda=qtdMoeda)
        db.session.add(objeto)
        db.session.commit()
        return jsonify(objeto)
    else:
        return jsonify(['Method Not Allowed'])

@app.route('/cliente/<int:id>', methods = ['GET'])
def UmCliente(id):
    if(request.method == 'GET'):
        objeto = db.session.get(Cliente, id)
        return jsonify(objeto)
    else:
        return jsonify(['Method Not Allowed'])

@app.route('/cliente/<int:id>', methods=["POST"]) 
def EditarCliente(id):
    if request.method=='POST':
        try:
            amount = request.args.get('amount', type=float)
            cliente = Cliente.query.filter_by(id=id).first()
            cliente.qtdMoeda += amount
            db.session.commit()
            return jsonify(['Alteracao feita com sucesso'])
        except Exception as e:
            data={
                "message": "Atualizacao nao realizada"
            }
            return jsonify(data)

    else:
        return jsonify(['Method Not Allowed'])

@app.route('/cliente/<int:id>', methods = ['DELETE'])
def ApagarCliente(id):
    if(request.method == 'DELETE'):
        objeto = db.session.get(Cliente, id)
        db.session.delete(objeto)
        db.session.commit()

        data={
            "message": "Cliente Deletado com Sucesso"
        }

        return jsonify(data)
    else:
        return jsonify(['Method Not Allowed'])

# seletor
@app.route('/seletor', methods = ['GET'])
def ListarSeletor():
    if(request.method == 'GET'):
        produtos = Seletor.query.all()
        return jsonify(produtos)  

@app.route('/seletor/<string:nome>/<string:ip>', methods = ['POST'])
def InserirSeletor(nome, ip):
    if request.method=='POST' and nome != '' and ip != '':
        objeto = Seletor(nome=nome, ip=ip, stake=0.0)
        db.session.add(objeto)
        db.session.commit()
        return jsonify(objeto)
    else:
        return jsonify(['Method Not Allowed'])

@app.route('/seletor/<int:id>', methods = ['GET'])
def UmSeletor(id):
    if(request.method == 'GET'):
        objeto = db.session.get(Seletor, id)
        return jsonify(objeto)
    else:
        return jsonify(['Method Not Allowed'])

@app.route('/seletor/<int:id>/<string:nome>/<string:ip>/<float:verdin>', methods=["POST"])
def EditarSeletor(id, nome, ip, verdin):
    if request.method=='POST':
        try:
            varNome = nome
            varIp = ip
            validador = Seletor.query.filter_by(id=id).first()
            db.session.commit()
            validador.nome = varNome
            validador.ip = varIp
            validador.stake += verdin
            db.session.commit()
            return jsonify(validador)
        except Exception as e:
            data={
                "message": "Atualização não realizada"
            }
            return jsonify(data)
    else:
        return jsonify(['Method Not Allowed'])

@app.route('/seletor/<int:id>', methods = ['DELETE'])
def ApagarSeletor(id):
    if(request.method == 'DELETE'):
        objeto = db.session.get(Seletor, id)
        db.session.delete(objeto)
        db.session.commit()

        data={
            "message": "Seletor Deletado com Sucesso"
        }

        return jsonify(data)
    else:
        return jsonify(['Method Not Allowed'])

# hora
@app.route('/hora', methods = ['GET'])
def horario():
    if(request.method == 'GET'):
        objeto = datetime.now()
        return jsonify(objeto)

# transações		
@app.route('/transacoes', methods = ['GET'])
def ListarTransacoes():
    if(request.method == 'GET'):
        transacoes = Transacao.query.all()
        return jsonify(transacoes)
    
@app.route('/transacoes/<int:rem>/<int:reb>/<int:valor>', methods=['POST'])
def CriaTransacao(rem, reb, valor):
    print(f"Recebido pedido de criação de transação: remetente={rem}, recebedor={reb}, valor={valor}")

    if request.method == 'POST':
        objeto = Transacao(remetente=rem, recebedor=reb, valor=valor, status=0, horario=datetime.now())
        db.session.add(objeto)
        db.session.commit()

        print(f"Transação criada e salva no banco de dados: {objeto}")

        # Selecionar validadores
        seletores = Seletor.query.all()
        print(f"Seletores encontrados: {seletores}")
        sender = requests.get(f'http://localhost:5000/cliente/{rem}') # no seletor
        sender_amount = sender.json()
        sender = requests.get(f'http://localhost:5000/cliente/{reb}')
        receiver_amount = sender.json()
        for seletor in seletores:
            try:
                url = f'http://127.0.0.1:5001/seletor/select'
                data = {
                    'seletor_id': seletor.id,
                    'seletor_nome': seletor.nome,
                    'seletor_ip': seletor.ip,
                    'transaction_id': objeto.id,
                    'transaction_amount': valor,
                    'sender': rem,
                    'sender_amount': sender_amount['qtdMoeda'],  # Adicionando o saldo do remetente
                    'receiver': reb,
                    'receiver_amount': receiver_amount['qtdMoeda'],
                    'fee': 0.015,  # Adicione uma lógica para definir a taxa se necessário
                    'timestamp': objeto.horario.isoformat()
                }
                print(f"Enviando requisição para o seletor: {url} com dados: {data}")
                response = requests.post(url, json=data)
                
                print(f"Resposta do seletor: {response.status_code}, {response.text}")
                
                if response.status_code == 200:
                    selected_validators = response.json().get("selected_validators")
                    print(f"Validadores selecionados: {selected_validators}")
                    objeto.status = response.json().get("status")
                    return jsonify(objeto)
                    # Enviar transação para validadores (omitir esta parte ou completar conforme necessidade)
                else:
                    print(f"Erro ao comunicar com o seletor {seletor.ip}: {response.status_code}")
            except requests.exceptions.RequestException as e:
                print(f"Falha ao conectar ao seletor {seletor.ip}: {e}")
        return jsonify(objeto)
    else:
        print("Método não permitido")
        return jsonify(['Method Not Allowed'])


@app.route('/transacoes/<int:id>', methods = ['GET'])
def UmaTransacao(id):
    if(request.method == 'GET'):
        objeto = db.session.get(Transacao, id)
        return jsonify(objeto)
    else:
        return jsonify(['Method Not Allowed'])

@app.route('/transacoes/<int:id>/<int:status>', methods=["POST"])
def EditaTransacao(id, status):
    if request.method=='POST':
        try:
            objeto = Transacao.query.filter_by(id=id).first()
            db.session.commit()
            objeto.id = id
            objeto.status = status
            db.session.commit()
            return jsonify(objeto)
        except Exception as e:
            data={
                "message": "transação não atualizada"
            }
            return jsonify(data)
    else:
        return jsonify(['Method Not Allowed'])

@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404

if __name__ == "__main__":
	with app.app_context():
		db.create_all()
app.run(debug=True)