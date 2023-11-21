import utime
from machine import Pin
from machine import UART

# UART1 default pins
txPin = Pin(4)
rxPin = Pin(5)

# UART1
uart1 = UART(1, baudrate=115200, tx=txPin, rx=rxPin, timeout=100)

# LED
led = Pin(25, Pin.OUT)
led.value(0)

while True:    
    bytesRead = uart1.any()
    if bytesRead > 0:
        #readline returns when it reaches new line or timeout
        buf = uart1.readline()
        msg = buf.decode('UTF-8')
        print(msg)
        
        if msg.lower() == 'on':
            led.value(1)
            uart1.write('Control LED... ' + str(led.value()) + '\n')
        elif msg.lower() == 'off':
            led.value(0)
            uart1.write('Control LED... ' + str(led.value()) + '\n')
        else :
            uart1.write("Enter 'on' or 'off'\n")  