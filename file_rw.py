import os

# file read & write test
FILE_NAME = 'number_data.log'

def exists(path):
    try:
        os.stat(path)
        return True
    except Exception:
        return False
    
def checkLastNumber(fileName):
    file = open(fileName, 'r')
    line = file.readline()
    
    while line:
        count = int(line)
        # remove space and new line character
        print(line.strip())
        line = file.readline()
    
    file.close()
    
    return count

if exists(FILE_NAME):
    count = checkLastNumber(FILE_NAME)
else:
    count = 0
    
# open file as append mode    
file = open(FILE_NAME, 'a')
count += 1
print('Add number: ', count)
file.write(str(count) + '\n')
file.close()
