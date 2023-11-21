from machine import Pin, SPI
from PicoDHT22 import PicoDHT22
import sdcard
import os
import time


WRITE_INTERVAL = 2

# Use SPI1(Pin#10/11/12)
spi = SPI(1, sck=Pin(10), mosi=Pin(11), miso=Pin(12))
# CS is Pin#15
sd = sdcard.SDCard(spi, Pin(15))

print('initialize sdcard OK')

# open file system
vfs = os.VfsFat(sd)

print('initialize vfs OK')

# mount at /sdcard
os.mount(vfs, '/sdcard')

print('mount file system OK')

dht22 = PicoDHT22(Pin(0))

# timer callback function
def log_temp_humidity(timer_wr):
    file = open('/sdcard/temp_humid.txt', 'a')
    
    T, H = dht22.read()
    
    if T is None:
        print("Sensor error")
    else:
        now = time.localtime()
        logging_txt = "{0:04d}-{1:02d}-{2:02d} {3:02d}:{4:02d}:{5:02d} {6:>3.1f}'C {7:>3.1f}%\n".format(now[0], now[1], now[2], now[3], now[4], now[5], now[6], T,H)
        print(logging_txt)
        file.write(logging_txt)
    
    file.close()

# initialize timer
timer_wr = machine.Timer()
timer_wr.init(freq=(1/WRITE_INTERVAL), mode=machine.Timer.PERIODIC, callback=log_temp_humidity)

print('* Start Logging...')

while True:
    pass
