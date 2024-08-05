import requests

url = "https://skyscanner80.p.rapidapi.com/api/v1/flights/auto-complete"


def get_all_airports(city):
    querystring = {"query": city}

    headers = {
        "x-rapidapi-key": "e6fe1a3f63mshd0b9734cef95d2bp13a52bjsn7386479177ed",
        "x-rapidapi-host": "skyscanner80.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)
    res = response.json()

    if res.get('status'):
        airports = list(filter(lambda x: city.lower() in x['presentation']['title'].lower(), res['data']))
        return {'airports': airports, 'status': True}


def get_airport_id(code):
    querystring = {"query": code}

    headers = {
        "x-rapidapi-key": "e6fe1a3f63mshd0b9734cef95d2bp13a52bjsn7386479177ed",
        "x-rapidapi-host": "skyscanner80.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)
    res = response.json()
    return res['data'][0]['id']
