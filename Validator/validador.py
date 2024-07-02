from flask import Flask, request, jsonify
import datetime
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Simulação de chaves únicas e contas
unique_keys = {}


# Dados do banco simulados para transações e contas
accounts = {
    "user1": {"balance": 1000, "last_transaction_time": None, "transaction_count": 0, "last_block_time": None, "block_duration": 60},
    "user2": {"balance": 500, "last_transaction_time": None, "transaction_count": 0, "last_block_time": None, "block_duration": 60},
}

def initialize_account(account_id):
    if account_id not in accounts:
        accounts[account_id] = {
            'balance': 0,
            'last_transaction_time': None,
            'last_block_time': None,
            'block_duration': 60,  # tempo de bloqueio em segundos
            'transactions_last_minute_count': 0
        }

@app.route('/validador', methods=['POST'])
def validador():

    data = request.json
    transaction_id = data['transaction']['id']
    validator_id = data['validator_id']
    unique_key = data['unique_key']
    sender = data['transaction']['sender']
    sender_amount = data['transaction']['sender_amount']
    receiver = data['transaction']['receiver']
    sender_amount = data['transaction']['receiver_amount']
    amount = data['transaction']['amount']
    fee = data['transaction']['fee']
    timestamp = datetime.datetime.fromisoformat(data['transaction']['timestamp'])
    last_transaction_time = datetime.datetime.fromisoformat(data['last_transaction_time']) if data.get('last_transaction_time') else None
    transactions_last_minute_count = data['transaction']['transactions_last_minute_count']

    # Inicializar contas de remetente e destinatário se não existirem
    initialize_account(sender)
    initialize_account(receiver)

    # Verificar chave única
    if unique_key != unique_keys.get(validator_id):
        return jsonify({"status": 2, "message": "Chave única inválida"}), 400
    current_time = datetime.datetime.now()
    # Verificar saldo suficiente
    if sender_amount < amount + fee:
        return jsonify({"status": 2, "message": "Saldo insuficiente"}), 400
    # Verificar se o horário da transação é válido
    if timestamp > current_time or (last_transaction_time and timestamp <= datetime.datetime.fromisoformat(last_transaction_time)):
        return jsonify({"status": 2, "message": "Horário da transação inválido"}), 400
    # Verificar o limite de transações por minuto e estado de bloqueio
    if accounts[sender]['last_block_time'] and (current_time - accounts[sender]['last_block_time']).seconds < accounts[sender]['block_duration']:
        return jsonify({"status": 2, "message": "Remetente bloqueado devido a transações excessivas"}), 400
    
    # Contar transações no último minuto
    # transactions_last_minute = [t for t in transactions if t['sender'] == sender and (current_time - datetime.datetime.fromisoformat(t['timestamp'])).seconds < 60]
    if transactions_last_minute_count > 100:
        accounts[sender]['last_block_time'] = current_time
        accounts[sender]['block_duration'] *= 2  # Dobre o tempo de bloqueio se o problema persistir
        return jsonify({"status": 2, "message": "Limite de transações por minuto excedido, remetente bloqueado"}), 400
    
    # Atualizar saldo da conta e tempo da última transação
    accounts[sender]['balance'] -= amount + fee
    accounts[sender]['last_transaction_time'] = timestamp
    accounts[receiver]['balance'] += amount
    return jsonify({"status": 1, "message": "Transação validada com sucesso"}), 200

@app.route('/validador/register_key', methods=['POST'])
def register_key():
    data = request.json
    validator_id = data['validator_id'] 
    unique_key = data['unique_key']
    unique_keys.update({validator_id : unique_key})  # Armazenar a chave única associada ao ID do validador
    return jsonify({"status": 1, "message": "Chave registrada com sucesso"}), 200

@app.route('/validador/register_transaction', methods=['POST'])
def register_transaction():
    data = request.json
    transactions.append(data)
    return jsonify({"status": 1, "message": "Transação registrada com sucesso"}), 200

@app.route('/validador/keys', methods=['GET'])
def get_keys():
    return jsonify(unique_keys)

@app.route('/validador/accounts', methods=['GET'])
def get_accounts():
    return jsonify(accounts)

@app.route('/validador/transactions', methods=['GET'])
def get_transactions():
    return jsonify(transactions)

if __name__ == '__main__':
    app.run(debug=True, port=5002)
