import requests

from requests_to_api.get_airports_info import get_all_airports


def get_flight_one_way(data):
    fromId, toId, departDate, adults = data
    url = "https://skyscanner80.p.rapidapi.com/api/v1/flights/search-one-way"

    querystring = {
        "fromId": fromId,
        "toId": toId,
        "departDate": departDate,
        "adults": adults,
        "cabinClass": "economy"
    }

    headers = {
        "x-rapidapi-key": "1965246244msh0797ea4cda2a707p1482eajsn816d9c9d674a",
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
        "cabinClass": "economy"
    }

    headers = {
        "x-rapidapi-key": "1965246244msh0797ea4cda2a707p1482eajsn816d9c9d674a",
        "x-rapidapi-host": "skyscanner80.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()


def get_summary_results(data):
    departure, arrival, departure_date, arrival_date, trip_type, adults = data
    fromId = get_all_airports(departure)
    toId = get_all_airports(arrival)
    departDate = departure_date
    returnDate = arrival_date

    try:
        if trip_type == 'one_way':
            result = get_flight_one_way([fromId, toId, departDate, adults])
        elif trip_type == 'return_way':
            result = get_flight_roundtrip([fromId, toId, departDate, returnDate, adults])
        else:
            raise ValueError("Invalid trip type")

        print(result)
        return result
    except requests.RequestException as e:
        print(f"An error occurred: {e}")
        return None
