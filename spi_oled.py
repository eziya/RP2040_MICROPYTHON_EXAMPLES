from machine import Pin, SPI
from ssd1306 import SSD1306_SPI
from utime import sleep
import framebuf

spi = SPI(0, mosi=Pin(3), sck=Pin(2))
oled = SSD1306_SPI(128, 64, spi, dc=Pin(5), res=Pin(4), cs=Pin(6))

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
