import requests

data = {
    "passwords": [
        {
            "serviceUrl": "Amazon.com",
            "username": "Dennis97"
        },
        {
            "serviceUrl": "Ebay",
            "username": "Dennis"
        },
        {
            "serviceUrl": "uni2work.de",
            "username": "SuperStudent1234"
        }
    ],
    "uId": "CBCB3C50",
    "score": 100
}

response = requests.post("http://localhost:3000/api/passwords/add", json=data)
result = response.json()