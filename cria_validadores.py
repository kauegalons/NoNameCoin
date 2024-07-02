import requests

# Registrando Validadores

response = requests.post('http://localhost:5001/seletor/register/a/10.0')
print(response.text)
response = requests.post('http://localhost:5001/seletor/register/b/11.0')
print(response.text)
response = requests.post('http://localhost:5001/seletor/register/c/12.0')
print(response.text)
response = requests.post('http://localhost:5001/seletor/register/d/13.0')
print(response.text)
response = requests.post('http://localhost:5001/seletor/register/e/69.0')
print(response.text)
