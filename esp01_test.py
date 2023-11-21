from machine import Pin
from esp8266 import ESP8266
import utime
import json

ssid = ""
pwd = ""
weatherkey = ""


def print_info(res):
    
    pos_start = res.find('{')
    pos_end = res.rfind('}')
    
    res = res[pos_start:(pos_end+1)]
    
    # 현재 micropython 에서는 python 과 encoding, decoding 이 다르게 동작함.
    res = bytes(res, 'raw_unicode_escape').decode('utf-8')
    
    parsed = json.loads(res)
    #print(parsed)
    print()
    
    main = parsed.get('list')[0].get('main')
    weather = parsed.get('list')[0].get('weather')[0]
            
    print('Country     : ', parsed.get('city').get('country'))
    print('City        : ', parsed.get('city').get('name'))
    print('Temperature : ', main.get('temp'))
    print('Weather     : ', weather.get('description'))
    print()

led = Pin(25, Pin.OUT)
esp01 = ESP8266(uartPort=0, baudRate=115200, txPin=16, rxPin=17)

# check connection with esp01
print("Start Up: ", esp01.startUP())

# turn off echo
print("Echo-Off: ", esp01.echoING())
print()

# read version
print("Firmware Version: ")
print(esp01.getVersion())
print()

# set wifi AP + Station mode
print("WiFi Current Mode: ", esp01.setCurrentWiFiMode())
print()

print("Try to connect with WiFi..")
while True:
    if "WIFI CONNECTED" in esp01.connectWiFi(ssid, pwd):
        print("ESP8266 connect with WiFi..")
        break
    else:
        print('.')
        utime.sleep(1)

httpCode, httpRes = esp01.doHttpGet('api.openweathermap.org',
                                    '/data/2.5/forecast?lat=37.5&lon=126.9&units=metric&cnt=1&appid=' + weatherkey)

print('HTTP Code:', httpCode)
#print('HTTP Response:', httpRes)
print()

print_info(httpRes)

print()
print("Now you're connected..")
led.on()
print()




if esp01.disconnectWiFi():
    print("Disconnected..")
else:
    print("Problem during disconnection..")
led.off()
    