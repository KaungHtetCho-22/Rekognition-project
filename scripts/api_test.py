import requests

url = 'https://vs16ogc6jj.execute-api.us-east-1.amazonaws.com/prod/faces'
headers = {'Content-Type': 'application/json'}

response = requests.get(url, headers=headers)
print("Status Code:", response.status_code)
print("Response Body:", response.text)
