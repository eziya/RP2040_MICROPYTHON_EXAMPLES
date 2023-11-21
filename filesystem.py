import os
import time

# check filesystem
stats = os.statvfs("/")

block_size = stats[0]
total_block = stats[2]
free_block = stats[3]

print("Disk Space: ", block_size * total_block / 1024, "kB")
print("Free Space: ", block_size * free_block / 1024, "kB")

# list files
file_list = os.listdir()

for file in file_list:
    print('{0:<30}'.format(file), end='')
    
    # read file info
    info = os.stat(file)
    m_time = time.localtime(info[7])
    
    if info[0] == 0x8000:
        print('FILE: ', end='')
    elif info[0] == 0x4000:
        print('DIR: ', end='')
    
    # print file info
    print('{0:04d}-{1:02d}-{2:02d} {3:02d}:{4:02d}:{5:02d}'
          .format(m_time[0], m_time[1], m_time[2],
                  m_time[3], m_time[4], m_time[5]), end='')
    
    # print file size
    if info[0] == 0x8000:
        print(', SIZE: ', end='')
        print(info[6])
    elif info[0] == 0x4000:
        print()


        