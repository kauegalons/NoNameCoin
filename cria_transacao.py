import requests
import json

#Simula Transação
print("Iniciando criação de transação...")
response = requests.post('http://localhost:5000/transacoes/2/1/10')
print(response.text)
print(f"Resposta do servidor: {response.status_code}")
print(f"Conteúdo da resposta: {response.json()}")

# response = requests.get('http://localhost:5000/cliente/1')
# print(response.text)
# a = response.json()
# print(a['qtdMoeda'])