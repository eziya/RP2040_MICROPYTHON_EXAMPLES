from machine import Pin, Timer
import utime

led = Pin(25, Pin.OUT)
t1 = Timer()

def blink(_timer): 
    global led
    led.toggle()

# Timer init, blink will be called every second
t1.init(mode=Timer.PERIODIC, freq=1, callback=blink)

while True:
    print('Idle...')
    utime.sleep(1)
