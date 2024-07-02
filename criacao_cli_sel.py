import requests

# =============================== REGISTRAR CLIENTES =============================== 
response = requests.post('http://localhost:5000/cliente/pinto/1234/500')
print(response.text)
response = requests.post('http://localhost:5000/cliente/cu/1234/500')
print(response.text)
response = requests.post('http://localhost:5000/cliente/fds/1234/500')
print(response.text)

# =============================== EDITAR CLIIENTES =============================== 
response = requests.post('http://localhost:5000/cliente/1/250')
print(response.text)
response = requests.post('http://localhost:5000/cliente/2/300')
print(response.text)

# =============================== DELETAR CLIENTES =============================== 
response = requests.delete('http://localhost:5000/cliente/3')
print(response.text)

# =============================== REGISTRAR SELETORES =============================== 
response = requests.post('http://localhost:5000/seletor/seletor1/123.123')
print(response.text)
response = requests.post('http://localhost:5000/seletor/seletor2/122.122')
print(response.text)

# =============================== EDITAR SELETORES =============================== 
response = requests.post('http://localhost:5000/seletor/1/seletorB/111111')
print(response.text)
response = requests.post('http://localhost:5000/seletor/2/seletorA/222222')
print(response.text)

# =============================== DELETAR SELETORES =============================== 
response = requests.delete('http://localhost:5000/seletor/2')
print(response.text)

# =============================== GET CLIENTES =============================== 
response = requests.get('http://localhost:5000/cliente/3')
print(response.text)