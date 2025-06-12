import requests

url = 'https://zerocoder.ru/'

response = requests.get(url)
print(response.text)