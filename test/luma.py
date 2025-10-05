from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import ssd1306, ssd1325, ssd1331, sh1106
from time import sleep

from PIL import Image, ImageDraw, ImageFont

serial = i2c(port=1, address=0x3C)
device = ssd1306(serial, height=32, rotate=2)

# Box and text rendered in portrait mode
with canvas(device) as draw:
    # draw.rectangle(device.bounding_box, outline="white", fill="black")
    font = ImageFont.truetype("tiny.ttf", 6)
    draw.text((2, 2), "Hello World", fill="white", font=font)
sleep(10)
