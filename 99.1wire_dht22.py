from machine import Pin
from PicoDHT22 import PicoDHT22
import time

dht22 = PicoDHT22(Pin(0))

while True:
    T, H = dht22.read()
    
    if T is None:
        print("Sensor error")
    else:            
        print("T: {0:>3.1f}'C".format(T), end=' ')
        print("H: {0:>3.1f} %".format(H))
    
    time.sleep(2)