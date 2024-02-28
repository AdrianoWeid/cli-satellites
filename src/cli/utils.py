import sys
import time
import threading
from itertools import cycle
from PIL import Image

def print_satellite_info(satellite, lat, lon) :
    pass

def display_spinner(message, duration=5):
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
