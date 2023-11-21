import machine
from utime import sleep

adc0 = machine.ADC(0)

while True:
    adcVal = adc0.read_u16()
    print("ADC:", adcVal)
    sleep(0.5)
