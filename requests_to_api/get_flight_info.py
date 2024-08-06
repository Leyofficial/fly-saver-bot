import requests
from requests_to_api.get_airports_info import get_airport_id


def get_flight_one_way(data):
    fromId, toId, departDate, adults = data
    url = "https://skyscanner80.p.rapidapi.com/api/v1/flights/search-one-way"

    querystring = {
        "fromId": fromId,
        "toId": toId,
        "departDate": departDate,
        "adults": adults,
    }

    headers = {
        "x-rapidapi-key": "e6fe1a3f63mshd0b9734cef95d2bp13a52bjsn7386479177ed",
        "x-rapidapi-host": "skyscanner80.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()


def get_flight_roundtrip(data):
    fromId, toId, departDate, returnDate, adults = data
    url = "https://skyscanner80.p.rapidapi.com/api/v1/flights/search-roundtrip"

    querystring = {
        "fromId": fromId,
        "toId": toId,
        "departDate": departDate,
        "returnDate": returnDate,
        "adults": adults,
    }

    headers = {
        "x-rapidapi-key": "e6fe1a3f63mshd0b9734cef95d2bp13a52bjsn7386479177ed",
        "x-rapidapi-host": "skyscanner80.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()


def get_summary_results(data):
    fromId = get_airport_id(data['fromIdCode'])
    toId = get_airport_id(data['toIdCode'])
    departDate = data['departure_date']
    returnDate = data.get('arrival_date')
    adults = data['adults']
    trip_type = data['trip_type']

    try:
        if trip_type == 'one_way':
            result = get_flight_one_way([fromId, toId, departDate, adults])
        elif trip_type == 'return_way':
            result = get_flight_roundtrip([fromId, toId, departDate, returnDate, adults])
        else:
            raise ValueError("Invalid trip type")

        return result
    except requests.RequestException as e:
        print(f"An error occurred: {e}")
        return None


def get_flight_detail(id: str, token: str):
    url = "https://skyscanner80.p.rapidapi.com/api/v1/flights/detail"

    querystring = {"itineraryId": id,
                   "token": token,
                   }

    headers = {
        "x-rapidapi-key": "e6fe1a3f63mshd0b9734cef95d2bp13a52bjsn7386479177ed",
        "x-rapidapi-host": "skyscanner80.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()
