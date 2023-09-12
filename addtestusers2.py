import requests

data = {
    "passwords": [
        {
            "serviceUrl": "Amazon.com",
            "username": "Superfelix"
        },
        {
            "serviceUrl": "Ebay",
            "username": "Felix"
        },
        {
            "serviceUrl": "uni2work.de",
            "username": "DaFelix"
        }
    ],
    "uId": "A4A29E5B",
    "score": 80
}

response = requests.post("http://localhost:3000/api/passwords/add", json=data)
result = response.json()