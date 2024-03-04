from json.decoder import JSONDecoder
from json.encoder import JSONEncoder
import requests
import json

def fetch_satellite_data(base_url: str, satellite_name: str, page: str, page_size: str):
    params = {
        'search': satellite_name,
        'page': page,
        'page_size': page_size
    }

    response = requests.get(base_url, params=params)
    return response.json()

def parse_satellites_data(body):
    try:
        json_response = body.get('member')
        formatted_data = []
        for satellite in json_response:
            print(satellite)
            formatted_data.append({
                "satellite_id": satellite.get('id'),
                "satellite_name": satellite.get('name'),
                "line_1": satellite.get('line1'),
                "line_2": satellite.get('line2')
            })
        return formatted_data
    except json.JSONDecodeError as e:
        print(f"Error deserializing response: {e}")
        return []

def get_satellites(satellite_name: str=None, page: str=None, page_size: str=None):
    base_url = "https://tle.ivanstanojevic.me/api/tle"
    satellites_data = fetch_satellite_data(base_url, satellite_name, page, page_size)
    satellites = parse_satellites_data(satellites_data)
    return satellites

# Beispielaufruf mit korrigierten Parametern
test = get_satellites("Starlink", "1", "1")  # Suche nach Starlink-Satelliten, erste Seite, 10 Ergebnisse
