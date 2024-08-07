import requests

url = "https://skyscanner80.p.rapidapi.com/api/v1/checkServer"


def check_server_status():
    headers = {
        'x-rapidapi-key': "241a7a4a99msh35336c7b2f14994p13e8fcjsn5f06ee552ab9",
        'x-rapidapi-host': "skyscanner80.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers)

    return response.json()
