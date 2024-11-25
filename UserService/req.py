import requests

BASE = "http://127.0.0.1:5001/"

data = {"email" : "lol1@gmail.com", "password" : "1322", "name" : "Lol2", "age" : 228, "weight" : 150.0}

data1 = {"email" : "lol2@gmail.com", "password" : "1322", "name" : "Lol2", "age" : 228, "weight" : 150.0}

data2 = {"email" : "lol3@gmail.com", "password" : "1322", "name" : "Lol2", "age" : 228, "weight" : 150.0}

# response = requests.put(BASE + "userDB/0", data)
# print(response.json())
response = requests.get(BASE + "userDB/1")
print(response.json())
response = requests.patch(BASE + "userDB/" + str(1), {"age" : 12, "weight" : 12})
print(response.json())

# response = requests.put(BASE + "userDB/2", data1)
# print(response.json())
# response = requests.put(BASE + "userDB/3", data2)
# print(response.json())

# response = requests.get(BASE + "userDB/1")
# print(response.json())
# response = requests.delete(BASE + "userDB/1")
# print(response.json())
# response = requests.delete(BASE + "userDB/2")
# print(response.json())
# response = requests.get(BASE + "userDB/1")
# print(response.json())