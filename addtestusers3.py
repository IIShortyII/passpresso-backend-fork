import requests

data = {
    "passwords": [
        {
            "serviceUrl": "Amazon.com",
            "username": "Raffi123"
        },
        {
            "serviceUrl": "Ebay",
            "username": "Raffael"
        },
        {
            "serviceUrl": "uni2work.de",
            "username": "IchDerRaffi"
        }
    ],
    "uId": "CBCB3C50",
    "score": 69
}

response = requests.post("http://localhost:3000/api/passwords/add", json=data)
result = response.json()