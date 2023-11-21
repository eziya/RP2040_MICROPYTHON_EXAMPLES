from machine import *
import utime

rtc = machine.RTC()
# input time tuple (YYYY, MM, DD, DayofWeek, HH, mm, SS, ss)
rtc.datetime((2023, 9, 20, 2, 12, 12, 12, 0))

while True:
    print(rtc.datetime())
    utime.sleep(1)