from machine import Pin
import utime

led = Pin(25, Pin.OUT)
btn = Pin(20, Pin.IN, Pin.PULL_UP)

def btn_callback(pin):
    global led
    print('btn_callback called')
    led.toggle()
    
btn.irq(trigger=Pin.IRQ_FALLING, handler=btn_callback)

while True:
    print('Idle...')
    utime.sleep(1)
    