from machine import Pin
from machine import I2C
from ssd1306 import SSD1306_I2C
from utime import sleep
import framebuf

sda = Pin(0)
scl = Pin(1)

i2c0 = I2C(0, sda=sda, scl=scl)

devices = i2c0.scan()

if len(devices) == 0:
    print("No device found!\n")
else:
    print("I2C devices found :", len(devices))
    

for device in devices:
    print(" => HEX address :", hex(device))
    
oled = SSD1306_I2C(128, 64, i2c0, 0x3c)

oled.fill(0)
oled.show()

# draw lines
for x in range(0, 128, 4):
    oled.line(0, 0, x, 63, 1)
    oled.line(127, 0, 127-x, 63, 1)
    sleep(0.1)
    oled.show()
sleep(3)

# draw text
oled.fill(0)
oled.text("Hello World~", 10, 10)
oled.show()
sleep(3)

# frame buffer
oled.fill(0)
smile = bytearray(
    b'\x0F\xF0\x1F\xF8\x3F\xFC\x7F\xFE'
    b'\xE3\x87\xDD\x78\xFF\xFF\xFF\xFF'
    b'\xFF\xFF\xFF\xFF\xEF\xF7\xF7\xEF'
    b'\x78\x1E\x3F\xFC\x1F\xF8\x0F\xF0')

fb = framebuf.FrameBuffer(smile, 16, 16, framebuf.MONO_HLSB)
oled.blit(fb, 10, 10)
oled.show()

