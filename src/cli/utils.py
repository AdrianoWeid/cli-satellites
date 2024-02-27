from PIL import Image

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
