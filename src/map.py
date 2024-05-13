from utils import convert_image_to_ascii
from satellite_position_service import get_satellite_position
import time
import threading
import os

IMAGE = "../assets/world_map.jpeg"
HEIGHT = 50
WIDTH = 100
REFRESH_INTERVAL = 30  # Refresh interval in seconds

def mark_position(image_ascii, x, y):
    lines = image_ascii.split('\n')
    if 0 <= y < len(lines) and 0 <= x < len(lines[y]):
        lines[y] = lines[y][:x] + '∆' + lines[y][x+1:]
    return '\n'.join(lines)

def mark_orbit_trails(image_ascii, orbit_trail):
    lines = image_ascii.split('\n')

    for x, y in orbit_trail:
        if 0 <= y < len(lines) and 0 <= x < len(lines[y]):
            lines[y] = lines[y][:x] + 'o' + lines[y][x+1:]
    return '\n'.join(lines)

def colorize_map(image_ascii):
    magenta = "\033[35m"
    cyan = "\033[36m"
    dark_grey = "\033[90m"
    reset = "\033[0m"    

    result = []
    for c in image_ascii:
        if c == '∆':
            result.append(f"{magenta}{c}{reset}")
        elif c == 'o':
            result.append(f"{cyan}{c}{reset}")
        else:
            result.append(f"{dark_grey}{c}{reset}")
    return ''.join(result)


def lat_long_to_ascii_coords(lat, lon, ascii_width, ascii_height):
    norm_lon = (lon + 180) / 360.0
    norm_lat = (90 - lat) / 180.0
    x = min(round(norm_lon * ascii_width), ascii_width - 1)
    y = min(round(norm_lat * ascii_height), ascii_height - 1)
    return x, y

def update_map(id, orbit_trail, image_ascii):
    lat, lon = get_satellite_position(id)
    x, y = lat_long_to_ascii_coords(lat, lon, WIDTH, HEIGHT)
    
    orbit_trail.append((x, y))
    image_ascii = mark_orbit_trails(image_ascii, orbit_trail)
    image_ascii = mark_position(image_ascii, x, y)
    return colorize_map(image_ascii)

def map_ui(id):
    def input_thread(stop_event):
        input("Press Enter to return...\n")
        stop_event.set()

    command = "cls" if os.name == "nt" else "clear"
    orbit_trail = []
    image_ascii = convert_image_to_ascii(IMAGE, WIDTH, HEIGHT)
    image_ascii = update_map(id, orbit_trail, image_ascii)
    print(image_ascii)
    
    stop_event = threading.Event()
    thread = threading.Thread(target=input_thread, args=(stop_event,))
    thread.start()

    try:
        while not stop_event.is_set():
            for _ in range(15):  # Assuming REFRESH_INTERVAL = 30 seconds
                time.sleep(1)  # Sleep for 1 second at a time
                if stop_event.is_set():
                    os.system(command)
                    break
            if stop_event.is_set():
                os.system(command)
                break
            image_ascii = convert_image_to_ascii(IMAGE, WIDTH, HEIGHT)
            image_ascii = update_map(id, orbit_trail, image_ascii)
            os.system(command)
            print(image_ascii + "\nPress Enter to return...")
    finally:
        thread.join()

