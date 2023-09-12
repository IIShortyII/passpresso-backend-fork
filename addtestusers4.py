import requests

data = {
    "passwords": [
        {
            "serviceUrl": "Amazon.com",
            "username": "Jonas"
        },
        {
            "serviceUrl": "Ebay",
            "username": "Jonas"
        },
        {
            "serviceUrl": "uni2work.de",
            "username": "Jonas"
        }
    ],
    "uId": "8BFF4F50",
    "score": 120
}

response = requests.post("http://localhost:3000/api/passwords/add", json=data)
result = response.json()