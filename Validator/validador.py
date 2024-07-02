from flask import Flask, request, jsonify
import datetime
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Simulação de chaves únicas e contas
unique_keys = {1: 'oqmduK8tVUYFOFbQ', 2: 'JhOAzIVerbnWkxf8', 3: 'qSsHKoTqQ3DmcXCo', 4: 'VMWdwLIURzjW5BDm'}


# Dados do banco simulados para transações e contas
accounts = {
    "user1": {"balance": 1000, "last_transaction_time": None, "transaction_count": 0, "last_block_time": None, "block_duration": 60},
    "user2": {"balance": 500, "last_transaction_time": None, "transaction_count": 0, "last_block_time": None, "block_duration": 60},
}

transactions = [
    {
        "id": 1,
        "sender": "user1",
        "receiver": "user2",
        "amount": 100,
        "fee": 1,
        "timestamp": "2024-06-01T12:00:00",
        "status": 0,
        "unique_key": None
    }
]

@app.route('/validador', methods=['POST'])
def validador():
    print(1)

    data = request.json
    print(data)
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
    print(4)
    # Verificar chave única
    print(unique_key)
    print(validator_id)
    print(unique_keys)
    print(unique_keys.get(validator_id))
    if unique_key != unique_keys.get(validator_id):
        print("teste")
        return jsonify({"status": 2, "message": "Chave única inválida"}), 400
    print(5)
    current_time = datetime.datetime.now()
    # Verificar saldo suficiente
    if sender_amount < amount + fee:
        return jsonify({"status": 2, "message": "Saldo insuficiente"}), 400
    print(6)
    # Verificar se o horário da transação é válido
    if timestamp > current_time or (accounts[sender]['last_transaction_time'] and timestamp <= accounts[sender]['last_transaction_time']):
        return jsonify({"status": 2, "message": "Horário da transação inválido"}), 400
    print(7)
    # Verificar o limite de transações por minuto e estado de bloqueio
    if accounts[sender]['last_block_time'] and (current_time - accounts[sender]['last_block_time']).seconds < accounts[sender]['block_duration']:
        return jsonify({"status": 2, "message": "Remetente bloqueado devido a transações excessivas"}), 400
    print(8)
    # Contar transações no último minuto
    transactions_last_minute = [t for t in transactions if t['sender'] == sender and (current_time - datetime.datetime.fromisoformat(t['timestamp'])).seconds < 60]
    if len(transactions_last_minute) > 100:
        accounts[sender]['last_block_time'] = current_time
        accounts[sender]['block_duration'] *= 2  # Dobre o tempo de bloqueio se o problema persistir
        return jsonify({"status": 2, "message": "Limite de transações por minuto excedido, remetente bloqueado"}), 400
    print(9)
    # Atualizar saldo da conta e tempo da última transação
    accounts[sender]['balance'] -= amount + fee
    accounts[sender]['last_transaction_time'] = timestamp
    print(10)
    accounts[receiver]['balance'] += amount
    return jsonify({"status": 1, "message": "Transação validada com sucesso"}), 200

@app.route('/validador/register_key', methods=['POST'])
def register_key():
    print("aaaaaaaaaaa")
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
