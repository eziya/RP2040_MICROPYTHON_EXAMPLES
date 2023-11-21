from machine import Pin, PWM
from hcsr04 import HCSR04
import time

sensor = HCSR04(trigger_pin=0, echo_pin=1)
# 23.10월 현재 pico 에서 PWM 초기화가 정상적이지 않아서 한번에 초기화를 못하고 freq, duty 설정을 나눠야 함.
buzzer = PWM(Pin(18))
buzzer.freq(440)

while True:
    try:
        dist = sensor.distance_cm()
        print('Distance: ', dist, 'cm')
        
        if dist <= 10:
            buzzer.duty_u16(32768)
            print('buzz....')
        else:
            buzzer.duty_u16(0)
        
    except OSError as ex:
        print('Exception: ', ex)
    
    time.sleep(1)