import requests

url = 'http://localhost:5000/classify'
data = {'url': 'https://example.com'}

response = requests.post(url, json=data)
print(response.json())
