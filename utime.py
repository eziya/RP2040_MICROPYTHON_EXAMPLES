import utime

# input current time 
print()
print("				YYYY MM DD HH mm SS")
date_time = (input('Enter current date & time: ')) + ' 0 0'
input_time = utime.mktime(list(map(int, tuple(date_time.split(' ')))))
print(input_time)

# time gap between input time and current time
time_delta = input_time - utime.time()
print(time_delta)

def timeNow():
    #return time based on current time & time delta
    return utime.localtime(utime.time() + time_delta)

while True:
    dateTime = timeNow()
    print('{:04d}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}'.format(dateTime[0], dateTime[1], dateTime[2], dateTime[3], dateTime[4], dateTime[5]))
    utime.sleep(1)