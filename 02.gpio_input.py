from machine import Pin
import utime

btn_prev = False
btn_curr = False

led = Pin(25, Pin.OUT)
btn = Pin(20, Pin.IN, Pin.PULL_UP)

while True:
    btn_val = btn.value()
    
    # button pressed
    if btn_val == 0 and btn_prev == 1:    
        led.value(1)
    elif btn_val == 1 and btn_prev == 0:
        led.value(0)
        
    btn_prev = btn_val

    
        