from machine import Pin
from machine import ADC
from utime import sleep

# ADC3 is connected to internal voltage
# ADC4 is connected to internal temperature
adc3_pin = Pin(29, Pin.IN)
adc3 = ADC(3)
adc4 = ADC(4)

VOLT_CONV = 3.3 * 3 / 65535
TEMP_CONV = 3.3 / 65535

while True:
    # reading ADC
    adcVal3 = adc3.read_u16()
    adcVal4 = adc4.read_u16()
    
    # convert adc values
    voltADC = adcVal3 * VOLT_CONV
    tempADC = adcVal4 * TEMP_CONV
    temp = 27 - (tempADC - 0.706) / 0.001721        
    
    print("Input Voltage: {0:02.2f}".format(voltADC))
    print("Temperature: {0:02.2f}".format(temp))
    
    sleep(1)

