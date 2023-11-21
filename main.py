from machine import Pin
from esp8266 import ESP8266
import time
import sys

print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
print("RPi-Pico MicroPython Ver:", sys.version)
print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

# Create On-board Led object
led = Pin(25, Pin.OUT)

# Create an ESP8266 Object
esp01 = ESP8266(uartPort=0, baudRate=115200, txPin=16, rxPin=17)

print("StartUP", esp01.startUP())
print("Echo-Off", esp01.echoING())
print("\r\n")

# Print ESP8266 AT command version and SDK details
print(esp01.getVersion())

# set the current Wi-Fi in SoftAP+STA
print("WiFi Current Mode:", esp01.setCurrentWiFiMode())
print("\r\n\r\n")

# Connect with the Wi-Fi
print("Try to connect with the WiFi..")

while True:
    if "WIFI CONNECTED" in esp01.connectWiFi("", ""):
        print("ESP8266 connect with the WiFi..")
        break
    else:
        print(".")
        time.sleep(2)

print("\r\n\r\n")
print("Now it's time to start HTTP Get/Post Operation.......\r\n")

while True:
    led.toggle()
    time.sleep(1)

    # Going to do HTTP Get Operation with www.httpbin.org/ip, It returns the IP address of the connected device
    httpCode, httpRes = esp01.doHttpGet("www.httpbin.org", "/ip", "RaspberryPi-Pico", port=80)
    print("------------- www.httpbin.org/ip Get Operation Result -----------------------")
    print("HTTP Code:", httpCode)
    print("HTTP Response:", httpRes)
    print("-----------------------------------------------------------------------------\r\n\r\n")

    # Going to do HTTP Post Operation with www.httpbin.org/post
    post_json = "{\"name\":\"Noyel\"}"
    httpCode, httpRes = esp01.doHttpPost("www.httpbin.org", "/post", "RPi-Pico", "application/json", post_json, port=80)
    print("------------- www.httpbin.org/post Post Operation Result -----------------------")
    print("HTTP Code:", httpCode)
    print("HTTP Response:", httpRes)
    print("--------------------------------------------------------------------------------\r\n\r\n")
