import requests
import json

reqUrl = "localhost:8000/users/"

headersList = {
 "Accept": "*/*",
 "Content-Type": "application/json" 
}

payload = json.dumps({
  "name": "mohamed",
  "password": "password"
})

response = requests.request("PUT", reqUrl, data=payload,  headers=headersList)
