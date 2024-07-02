import requests

# Registrando Validadores

response = requests.post('http://localhost:5001/seletor/register/a/40.0')
print(response.text)
response = requests.post('http://localhost:5001/seletor/register/b/51.0')
print(response.text)
response = requests.post('http://localhost:5001/seletor/register/c/52.0')
print(response.text)
response = requests.post('http://localhost:5001/seletor/register/d/53.0')
print(response.text)
response = requests.post('http://localhost:5001/seletor/register/e/69.0')
print(response.text)
