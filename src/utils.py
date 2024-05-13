from datetime import datetime
from sgp4.api import Satrec, SGP4_ERRORS, jday
from PIL import Image
import sys
import time
import threading
import numpy as np

def print_satellite_info(satellitename, tle) :
    line1, line2 = tle
    satellite_rec = parse_tle(line1, line2)
    datetime_now = datetime.utcnow()
    distance_from_earth = calculate_distance_from_earth(line1, line2, datetime_now)
    
    print("SATELLITE INFORMATION")
    print(f"Name: {satellitename}")
    print(f"Epoch: {satellite_rec.epochyr}")  # Format as needed
    print(f"Inclination: {satellite_rec.inclo} degrees")
    print(f"RAAN: {satellite_rec.nodeo} degrees")
    print(f"Eccentricity: {satellite_rec.ecco}")
    print(f"Perigee: {satellite_rec.argpo} degrees")
    print(f"Mean Motion: {satellite_rec.no_kozai} revs per day")
    print(f"Distance from Earth: {distance_from_earth:.2f} km\n")

def parse_tle(line1, line2):
    satellite_rec = Satrec.twoline2rv(line1, line2)
    return satellite_rec

def calculate_distance_from_earth(line1, line2, datetime):
    earth_radius_km = 6371.0
    jd, fr = jday(datetime.year, datetime.month, datetime.day, datetime.hour, datetime.minute, datetime.second)
    satellite_rc = Satrec.twoline2rv(line1, line2)
    e, r, v = satellite_rc.sgp4(jd, fr)
    
    if e not in SGP4_ERRORS:
        distance_from_center = np.linalg.norm(r)
        distance_from_surface = distance_from_center - earth_radius_km
        return distance_from_surface
    else:
        raise Exception("Error computing satellite position")

def display_spinner(message: str, duration: int=5):
    spin_chars = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
    end_time = time.time() + duration

    def spinner():
        while time.time() < end_time:
            for char in spin_chars:
                sys.stdout.write('\r\033[35m{}\033[0m \033[35m{}\033[0m'.format(char, message))
                sys.stdout.flush()
                time.sleep(0.1)
        # Clear the spinner after completion
        sys.stdout.write('\r' + ' ' * (len(message) + 2) + '\r')
        sys.stdout.flush()

    spinner_thread = threading.Thread(target=spinner)
    spinner_thread.start()
    spinner_thread.join()

def convert_image_to_ascii(image_src: str, width, height):
    image = Image.open(image_src).convert("L")
    image = image.resize((width, height))


    ascii_image = ""
    for i, pixel in enumerate(image.getdata()):

        if pixel <= 63:
            char = "@"
        elif pixel <= 127:
            char = "%"
        elif pixel <= 192:
            char = "."
        elif pixel <= 255:
            char = " "
        else:
            char = "?"

        if i % width == 0 and i != 0:
            ascii_image += "\n"

        ascii_image += char

    return ascii_image
