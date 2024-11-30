import requests

BASE = "http://127.0.0.1:5001/"

data = {"email" : "lol1@gmail.com", "password" : "1322", "name" : "Lol2", "age" : 228, "weight" : 150.0}

response = requests.put(BASE + "userDB/0", data)
print(response.json())
response = requests.get(BASE + "userDB/1")
print(response.json())
response = requests.patch(BASE + "userDB/1", {"age" : 12, "weight" : 12})
print(response.json())
response = requests.delete(BASE + "userDB/1")
print(response.json())