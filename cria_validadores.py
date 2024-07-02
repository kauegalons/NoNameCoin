import requests

# =============================== REGISTRO DE VALIDADORES =============================== 
response = requests.post('http://localhost:5001/seletor/register/aaaaaaaaaa/10.0')
print(response.text)
response = requests.post('http://localhost:5001/seletor/register/b/69.0')
print(response.text)
response = requests.post('http://localhost:5001/seletor/register/c/666.0')
print(response.text)
response = requests.post('http://localhost:5001/seletor/register/d/6969.0')
print(response.text)
response = requests.post('http://localhost:5001/seletor/register/e/9669.0')
print(response.text)

