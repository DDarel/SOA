import requests

BASE = "http://127.0.0.1:5000/"

response = requests.get(BASE + "calculate/1/55.5")
print(response.json())