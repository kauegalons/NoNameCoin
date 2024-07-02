import requests

#CLIENTES

#Registrando clientes
response = requests.post('http://localhost:5000/cliente/leo/1234/500')
print(response.text)
response = requests.post('http://localhost:5000/cliente/kaue/1234/500')
print(response.text)
response = requests.post('http://localhost:5000/cliente/Gabriel/1234/500')
print(response.text)

#Editando clientes
response = requests.post('http://localhost:5000/cliente/1/100')
print(response.text)
response = requests.post('http://localhost:5000/cliente/2/450')
print(response.text)

#Deletando clientes
response = requests.delete('http://localhost:5000/cliente/3')
print(response.text)

#SELETORES

#Registrando seletores
response = requests.post('http://localhost:5000/seletor/seletor1/123.123')
print(response.text)
response = requests.post('http://localhost:5000/seletor/seletor2/122.122')
print(response.text)

#Editando Seletores
response = requests.post('http://localhost:5000/seletor/1/seletorB/111111')
print(response.text)
response = requests.post('http://localhost:5000/seletor/2/seletorA/222222')
print(response.text)

#Deletando seletores
response = requests.delete('http://localhost:5000/seletor/2')
print(response.text)



#Get clientes
response = requests.get('http://localhost:5000/cliente/3')
print(response.text)
