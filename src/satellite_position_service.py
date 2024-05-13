import os
from dotenv import load_dotenv
import requests
load_dotenv()

def build_query_url(base_url: str, satellite_id: int):
    OBSERVER_LAT = 40.7128
    OBSERVER_LON = 74.0060
    OBSERVER_ALT = 0.0
    SECONDS = 1
    api_key = os.getenv("N2YO_API_KEY")
    if not api_key:
        raise ValueError("N2YO_API_KEY muss gesetzt werden!")

    url = f"{base_url}/{satellite_id}/{OBSERVER_LAT}/{OBSERVER_LON}/{OBSERVER_ALT}/{SECONDS}?apiKey={api_key}"
    return url


def get_satellite_position(satellite_id: int) -> tuple[float, float] | None:
    base_url = "https://api.n2yo.com/rest/v1/satellite/positions"
    url = build_query_url(base_url, satellite_id)

    response = requests.get(url)

    if response.status_code == 200:
        json_response = response.json()
        positions = json_response.get("positions", [])

        if positions:
            positions = positions[0]
            satlatitude = positions.get("satlatitude")
            satlongitude = positions.get("satlongitude")
            return satlatitude, satlongitude
        else:
            print("No positions found.")
    else:
        print("Error deserializing satellite position response: {}, status_code", response.json(), response.status_code)


def get_tle(NORAD):
    base_url = "https://api.n2yo.com/rest/v1/satellite/tle/"
    api_key = os.getenv("N2YO_API_KEY")
    url = f"{base_url}{NORAD}&apiKey={api_key}"
    response = requests.get(url)
    
    if response.status_code == 200:
        json_response = response.json()
        tle = json_response.get("tle").split("\r\n")

        if not tle:
            print("No tle-data found or NORAD_Number is wrong.")
        else:
            return tle
    else:
        print("Error deserializing satellite position response: {}, status_code", response.json(), response.status_code)