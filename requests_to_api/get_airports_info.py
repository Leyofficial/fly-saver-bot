import requests

url = "https://skyscanner80.p.rapidapi.com/api/v1/flights/auto-complete"


def get_all_airports(city):
    querystring = {"query": city}

    headers = {
        'x-rapidapi-key': "241a7a4a99msh35336c7b2f14994p13e8fcjsn5f06ee552ab9",
        'x-rapidapi-host': "skyscanner80.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)
    res = response.json()

    if res.get('status'):
        airports = list(filter(lambda x: city.lower() in x['presentation']['title'].lower(), res['data']))
        return {'airports': airports, 'status': True}


def get_airport_id(code):
    querystring = {"query": code}

    headers = {
        'x-rapidapi-key': "241a7a4a99msh35336c7b2f14994p13e8fcjsn5f06ee552ab9",
        'x-rapidapi-host': "skyscanner80.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)
    res = response.json()
    if res.get('status') and res['data']:
        return res['data'][0]['id']
