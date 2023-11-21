from machine import Pin, I2C
from ds3231 import DS3231
import time

sda = Pin(8)
scl = Pin(9)

i2c0 = I2C(0, sda=sda, scl=scl)

devices = i2c0.scan()

if len(devices) == 0:
    print('* No I2C device found!')
else:
    print('* I2C devices found: ', len(devices))
    
for device in devices:
    print(' => HEX address: ', hex(device))

ds3231 = DS3231(i2c0)
ds3231.save_time()

while True:
    dt = ds3231.get_time()
    temp = ds3231.get_temperature()
    
    print("{:04d}-{:02d}-{:02d} {:02d}:{:02d}:{:02d} {:.2f}'C".format(
        dt[0], dt[1], dt[2], dt[3], dt[4], dt[5], temp))
    
    time.sleep(1)