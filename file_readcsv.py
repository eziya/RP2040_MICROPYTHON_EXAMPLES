import os

file_name = 'students.csv'

# open csv file
file = open(file_name, 'r')

# read lines
line = file.readline()
while line:    
    # split text
    items = line.split(',')
    
    for item in items:
        print(item, '\t', end='')
        
    print()
    
    line = file.readline()

# close file
file.close()