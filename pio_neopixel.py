from utime import sleep
from PicoNeopixel import Neopixel

nPixel = 32
# num_leds, state_machine, pin, mode
neopixel_feather = Neopixel(nPixel, 0, 0, 'GRB')
neopixel_feather.brightness(10)

pos = 0
color_idx = 0

color_rgb = ((255, 0, 0), (0, 255, 0), (0, 0, 255))
color_off = (0, 0, 0)

def move_pixel():
    global pos, color_idx, colr_rgb, color_off
    
    pos = (pos + 1) % nPixel
    color_idx = (color_idx + 1) % 3
    
    for i in range(nPixel):
        if i == pos:
            neopixel_feather.set_pixel(i, color_rgb[color_idx])
        else:
            neopixel_feather.set_pixel(i, color_off)               
            
    neopixel_feather.show()    

def rainbow():
    hue_step = 65535 // nPixel
    
    for i in range(nPixel):
        current_hue = hue_step * i
        # 색상, 채도, 명도
        rgb = neopixel_feather.colorHSV(current_hue, 255, 255)
        neopixel_feather.set_pixel(i, rgb)
        
    neopixel_feather.show()   

while True:
    for i in range(nPixel):
        move_pixel()
        sleep(0.5)
        
    rainbow()
    for i in range(nPixel):        
        neopixel_feather.rotate_right(1)
        neopixel_feather.show()
        sleep(0.5)
    