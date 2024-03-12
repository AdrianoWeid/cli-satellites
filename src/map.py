from utils import convert_image_to_ascii
import time
import threading
import os

def mark_position(image_ascii, x, y):
    lines = image_ascii.split('\n')

    if 0 <= y < len(lines) and 0 <= x < len(lines[y]):
        lines[y] = lines[y][:x] + '∆' + lines[y][x+1:]

    lines = '\n'.join(lines)
    return lines

def mark_orbit_trails(image_ascii, orbit_trail):
    lines = image_ascii.split('\n')
    for point in orbit_trail:
        x = point[0]
        y = point[1]
        print(x,y)
        if 0 <= point[1] < len(lines) and 0 <= point[0] < len(lines):
            print("moin")
            lines[y] = lines[y][:x] + 'o' + lines[y][x+1:]

    lines = '\n'.join(lines)
    return lines

def colorize_map(image_ascii):
    # Definiere ANSI-Farbcodes
    magenta = "\033[35m"  # Magenta für '∆'
    cyan = "\033[36m"    # Cyan für 'o'
    dark_grey = "\033[90m"  # Dunkelgrau für den Rest
    reset = "\033[0m"    # Zurücksetzen der Farbe

    # Ersetze Zeichen durch farbige Zeichen
    colored_map = ''.join(
        f"{magenta}{c}{reset}" if c == '∆' else
        f"{cyan}{c}{reset}" if c == 'o' else
        f"{dark_grey}{c}{reset}"
        for c in image_ascii
    )

    return colored_map


def map_ui(satellite_id, lat, lon):
    IMAGE = "assets/world_map.jpeg"
    HEIGHT = 50
    WIDTH = 100
    REFRESH_INTERVAL = 30
    orbit_trail = []
    x,y = lat_long_to_ascii_coords(lat, lon, WIDTH, HEIGHT)
    image_ascii = convert_image_to_ascii(IMAGE, WIDTH, HEIGHT)
    image_ascii = mark_position(image_ascii, x,y)
    image_ascii = colorize_map(image_ascii)
    orbit_trail.append((x,y))
    print(image_ascii)

    def thread_target(stop_event):
        while not stop_event:
            time.sleep(REFRESH_INTERVAL)
            os.system('clear')
            x,y = lat_long_to_ascii_coords(lat, lon, WIDTH, HEIGHT) 
            image_ascii = convert_image_to_ascii(IMAGE, WIDTH, HEIGHT)
            image_ascii = mark_position(image_ascii, x,y)
            image_ascii = mark_orbit_trails(image_ascii, x, y)
            image_ascii = colorize_map(image_ascii)
            orbit_trail.append((x,y))

    stop_event = threading.Event()
    update_thread = threading.Thread(target=lambda: thread_target(stop_event))
    update_thread.start()

    input("\nPress Enter to return...")
    stop_event.set()
    update_thread.join()


def lat_long_to_ascii_coords(lat, lon, ascii_width, ascii_height):
    norm_lon = (lon + 180)/360.0
    norm_lat = (90.0 - lat) / 180.0

    ascii_x = round(norm_lon * ascii_width)
    ascii_y = round(norm_lat * ascii_height)

    ascii_x = min(ascii_x, ascii_width - 1)
    ascii_y = min(ascii_y, ascii_y - 1)

    return ascii_x, ascii_y
map_ui(2323,7,2)
