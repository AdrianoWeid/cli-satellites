import requests

def build_query_url(base_url: str, satellite_name: str, page: int, page_size: int):
    url = f"{base_url}?search={satellite_name}"
    return url

def fetch_satellite_data(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"An error occurred: {err}")

def get_satellites(satellite_name, page, page_size):
    base_url = "http://tle.ivanstanojevic.me/api/tle"
    url = build_query_url(base_url, satellite_name, page, page_size)
    print(url)
    satellite_data = fetch_satellite_data(url)

    if satellite_data:
        print(satellite_data)
    else:
        print("Failed to retrieve satellite data.")

get_satellites("Starlink", 1, 1)
