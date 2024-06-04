import spidev as SPI
import ST7789
import time

from PIL import Image,ImageDraw,ImageFont
import qrcode

# Raspberry Pi pin configuration:
RST = 27
DC = 25
BL = 24
bus = 0 
device = 0 

# 240x240 display with hardware SPI:
disp = ST7789.ST7789(SPI.SpiDev(bus, device),RST, DC, BL)

# Initialize library.
disp.Init()

# Clear display.
disp.clear()

#generate the QR Code
img = qrcode.make("3FHipXWBarmpVmqbFax4a2g7R6vXqNxLCh")

#resize the image to 240 pixels square
resized = img.resize((240, 240))

#display the image
disp.ShowImage(resized,0,0)
