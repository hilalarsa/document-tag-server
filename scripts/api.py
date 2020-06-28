import requests

response = requests.get("http://localhost:3000/dosen")

# print(dir(response))
# print(response.json()[0]['nama_dosen'])

def get_data(tableName):
    response = requests.get("http://localhost:3000/"+tableName)
    return response.json()