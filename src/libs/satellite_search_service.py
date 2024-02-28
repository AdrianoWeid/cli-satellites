import requests
import json
import httpx


def fetch_satellite_data(base_url: str, satellite_name, page, page_size):
    params = {
        'search': satellite_name
        #'page': page,
        #'page_size': page_size
    }

    with httpx.Client() as client:
        response = client.get(base_url, params=params)

        # Überprüfen, ob die Anfrage erfolgreich war
        if response.status_code == 200:
            return response.content
        else:
            print('Es gab ein Problem mit der Anfrage an die API.')

def parse_satellites_data(body):
    try:
        data = json.loads(body)
        satellites = data.get('member')
        formatted_data = []
        for satellite in satellites:
            formatted_data.append({
                "satellite_id": satellite.get('satelliteId'),
                "satellite_name" : satellite.get('name'),
                "line_1": satellite.get('line1'),
                "line_2": satellite.get('line2')
            })

        return formatted_data
    except json.JSONDecodeError as e:
        print(f"Error deserializing response: {e}")
        return []


def get_satellites(satellite_name: str, page: str, page_size: str):
    base_url = "https://tle.ivanstanojevic.me/api/tle"
    satellites_data = fetch_satellite_data(base_url, satellite_name, page, page_size)
    satellites = parse_satellites_data(satellites_data)
    return satellites

test = get_satellites("Starlink", "1","1")
print(test)
