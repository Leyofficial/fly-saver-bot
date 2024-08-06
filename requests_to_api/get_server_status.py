import requests

url = "https://skyscanner80.p.rapidapi.com/api/v1/checkServer"


def check_server_status():
    headers = {
        "x-rapidapi-key": "e6fe1a3f63mshd0b9734cef95d2bp13a52bjsn7386479177ed",
        "x-rapidapi-host": "skyscanner80.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers)

    return response.json()
