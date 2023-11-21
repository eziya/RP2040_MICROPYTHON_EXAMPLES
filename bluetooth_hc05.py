from machine import Pin, UART, Timer

# How to configure HC-05
# AT+VERSION
# AT+NAME => AT+NAMEHC-05
# AT+PIN => AT+PIN1234
# AT+BAUD => AT+BAUD6
# AT+ROLE => AT+ROLE=S

uart = UART(0, 38400, timeout=100)
bt_timer = Timer()

# notification message every 10sec
def send_count(_timer):    
    uart.write('KEEP Alive\r\n')
    
bt_timer.init(mode=Timer.PERIODIC, freq=0.1, callback=send_count)

# echo service
while True:
    if uart.any():
        command = uart.readline()
        print(command)
        uart.write(command)
        