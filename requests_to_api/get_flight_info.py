import requests


def get_flight_one_way(data):
    adults, fromId, toId, departDate, adults = data
    url = "https://skyscanner80.p.rapidapi.com/api/v1/flights/search-one-way"

    querystring = {"fromId": {fromId},
                   "toId": {toId}, "departDate": {departDate},
                   "adults": {adults}, "cabinClass": "economy"}

    headers = {
        "x-rapidapi-key": "1965246244msh0797ea4cda2a707p1482eajsn816d9c9d674a",
        "x-rapidapi-host": "skyscanner80.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    print(response.json())


def get_flight_roundtrip(data):
    adults, fromId, toId, departDate, returnDate, adults = data
    import requests

    url = "https://skyscanner80.p.rapidapi.com/api/v1/flights/search-roundtrip"

    querystring = {"fromId": {fromId},
                   "toId": {toId},
                   "departDate": {departDate}, "returnDate": {returnDate}, "adults": {adults}, "cabinClass": "economy"}

    headers = {
        "x-rapidapi-key": "1965246244msh0797ea4cda2a707p1482eajsn816d9c9d674a",
        "x-rapidapi-host": "skyscanner80.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    print(response.json())
