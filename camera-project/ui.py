import spidev as SPI
import logging
import ST7789
import time
import os
from picamera2 import Picamera2

from PIL import Image,ImageDraw,ImageFont

def stored_pics():

    print('Checking stored pictures')
    pic_index = 0
    save_path = '/home/pi/Documents/cam/images/'
    pictures = [f for f in os.listdir(save_path) if os.path.isfile(os.path.join(save_path, f))]
    pictures.sort()
    number_of_pictures = len(pictures)

    filename = pictures[pic_index]
    capture = Image.open(f"/home/pi/Documents/cam/images/{filename}")
    capture = capture.resize((240,240)).rotate(90)
    disp.ShowImage(capture)

    print(pictures)

    while True:
        # Stick up
        if disp.digital_read(disp.GPIO_KEY_UP_PIN ) == 0: # button is released
            #draw.polygon([(20, 20), (30, 2), (40, 20)], outline=255, fill=0xff00)
            pass        
        else: # button is pressed:
            #draw.polygon([(20, 20), (30, 2), (40, 20)], outline=255, fill=0)
            try:
                pic_index = (pic_index + 1) % number_of_pictures
                filename = pictures[pic_index]
                capture = Image.open(f"/home/pi/Documents/cam/images/{filename}")
                capture = capture.resize((240,240)).rotate(90)
                disp.ShowImage(capture)
                print ("Up")
            except:
                draw.text((5, 5), 'Broken Image', fill = "RED",font=Font3)
            
        # Stick down
        if disp.digital_read(disp.GPIO_KEY_DOWN_PIN) == 0: # button is released
            #draw.polygon([(30, 60), (40, 42), (20, 42)], outline=255, fill=0xff00)
            pass        
        else: # button is pressed:
            #draw.polygon([(30, 60), (40, 42), (20, 42)], outline=255, fill=0)
            try:
                pic_index = (pic_index - 1) % number_of_pictures
                filename = pictures[pic_index]
                capture = Image.open(f"/home/pi/Documents/cam/images/{filename}")
                capture = capture.resize((240,240)).rotate(90)
                disp.ShowImage(capture)
                print ("down")
            except:
                draw.text((5, 5), 'Broken Image', fill = "RED",font=Font3)
            
        # Stick press
        if disp.digital_read(disp.GPIO_KEY_PRESS_PIN) == 0: # button is released
            #draw.rectangle((20, 22,40,40), outline=255, fill=0xff00) #center 
            pass        
        else: # button is pressed:
            #draw.rectangle((20, 22,40,40), outline=255, fill=0) #center filled
            print ("center")        
            
        # Key 3
        if disp.digital_read(disp.GPIO_KEY3_PIN) == 0: # button is released
            #draw.ellipse((70,40,90,60), outline=255, fill=0xff00) #A button      
            pass  
        else: # button is pressed:
            #draw.ellipse((70,40,90,60), outline=255, fill=0) #A button filled
            draw.rectangle((0,0,disp.width, disp.height), outline=0, fill=0)
            break
        
    draw.rectangle((0,0,disp.width, disp.height), outline=0, fill=0)

# Test camera

cam = Picamera2()
cam.configure(cam.create_still_configuration())

cam.start()

print('Start cam test')
request = cam.capture_request()
request.save("main", "test.jpg")
request.release()

# Initialize display display
disp = ST7789.ST7789()
disp.Init()
disp.clear()
disp.bl_DutyCycle(50)

# test display
image1 = Image.new("RGB", (disp.width, disp.height), "BLACK")
draw = ImageDraw.Draw(image1)

Font1 = ImageFont.truetype("Font/Font01.ttf",25)
Font2 = ImageFont.truetype("Font/Font01.ttf",35)
Font3 = ImageFont.truetype("Font/Font02.ttf",32)

draw.text((60, 68), 'Compact', fill = "WHITE",font=Font2)
draw.text((60, 108), 'Camera', fill = "WHITE",font=Font2)
disp.ShowImage(image1)

time.sleep(5)

draw.rectangle((0,0,disp.width, disp.height), outline=0, fill=0)
disp.ShowImage(image1)

print('END CAM TEST')

# Ok, its setup.

# now we need to connect it to the camera module
# And setup the camera controls
# Now I need it to 
try:
    while True:
            
        # Key 1
        if disp.digital_read(disp.GPIO_KEY1_PIN) == 0: # button is released
            #draw.ellipse((70,0,90,20), outline=255, fill=0xff00) #A button
            pass        
        else: # button is pressed:
            #draw.ellipse((70,0,90,20), outline=255, fill=0) #A button filled

            stamp = time.strftime("%Y-%m-%d:%H:%M:%S")

            print(f'Stamp: {stamp}')

            request = cam.capture_request()
            request.save("main", f"/home/pi/Documents/cam/images/{stamp}.jpg")
            request.release()
            capture = Image.open(f"/home/pi/Documents/cam/images/{stamp}.jpg")
            capture = capture.resize((240,240)).rotate(90)
            im_r=capture
            disp.ShowImage(im_r)

            time.sleep(3)

            draw.rectangle((0,0,disp.width, disp.height), outline=0, fill=0)
            disp.ShowImage(image1)

            print ("Captured")
            
        # Key 2
        if disp.digital_read(disp.GPIO_KEY2_PIN) == 0: # button is released
            #draw.ellipse((100,20,120,40), outline=255, fill=0xff00) #B button]
            pass        
        else: # button is pressed:
            #draw.ellipse((100,20,120,40), outline=255, fill=0) #B button filled
            draw.rectangle((0,0,disp.width, disp.height), outline=0, fill=0)
            stored_pics()
            print ("Selected")
            
        # Key 3
        if disp.digital_read(disp.GPIO_KEY3_PIN) == 0: # button is released
            #draw.ellipse((70,40,90,60), outline=255, fill=0xff00) #A button      
            pass  
        else: # button is pressed:
            #draw.ellipse((70,40,90,60), outline=255, fill=0) #A button filled
            print ("Back")

        draw.text((5, 5), 'Ready', fill = "WHITE",font=Font1)
        disp.ShowImage(image1)
except Exception as e:
    print('Exiting')
    print(e)

draw.rectangle((0,0,disp.width, disp.height), outline=0, fill=0)
disp.ShowImage(image1)
disp.module_exit()
print('Good exit')

# and that's it
# Once its all done, we just need to find a portable power supply and we've got a camera