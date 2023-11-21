import machine
import onewire
import ds18x20
from utime import sleep

# 1-wire pin configuration
data = machine.Pin(0)
tempWire = onewire.OneWire(data)

# create sensor object
tempSensors = ds18x20.DS18X20(tempWire)

# scan devices
devices = tempSensors.scan()
print(len(devices), ' temperature sensors found!\n')

while True:
    print('Temp:', end=' ')
    tempSensors.convert_temp()
    sleep(1)
    
    for device in devices:
        t = tempSensors.read_temp(device)
        print('{:>6.2f}'.format(t), end=' ')
    print()
    


