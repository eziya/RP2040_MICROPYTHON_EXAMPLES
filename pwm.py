from machine import Pin, PWM, ADC
import utime

# ADC0, Pin26
adc = ADC(0)

# gpio0 led
pwm = PWM(Pin(0))

# 1kHz pwm
pwm.freq(1000)
cnt = 0

while True:    
    cnt += 1
    
    # update PWM every 10ms
    if(cnt > 10):    
        cnt = 0
        adcVal = adc.read_u16()    
        pwm.duty_u16(adcVal)
        #print('ADC1:', adcVal)
    
    utime.sleep_ms(1)
