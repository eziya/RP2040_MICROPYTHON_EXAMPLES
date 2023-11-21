from machine import Pin
import utime

pin0 = Pin(0, Pin.OUT)
pin1 = Pin(1, Pin.OUT)

leds = [pin0, pin1]
intervals = [100, 500]
tick_old = [utime.ticks_ms()] * 2

while True:
    tick_now = utime.ticks_ms()    
    
    for i, led in enumerate(leds):    
        elapsed = utime.ticks_diff(tick_now, tick_old[i])        
        
        # if interval is greater than elapsed, toggle gpio
        if elapsed > intervals[i]:
            tick_old[i] = tick_now
            led.toggle()
            
