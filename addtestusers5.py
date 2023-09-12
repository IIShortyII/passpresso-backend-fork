import requests

data = {
    "passwords": [
        {
            "serviceUrl": "Amazon.com",
            "username": "HerrFeger"
        },
        {
            "serviceUrl": "Ebay",
            "username": "Basti"
        },
        {
            "serviceUrl": "uni2work.de",
            "username": "SebastianFeger"
        }
    ],
    "uId": "472B695B",
    "score": 20
}

response = requests.post("http://localhost:3000/api/passwords/add", json=data)
result = response.json()