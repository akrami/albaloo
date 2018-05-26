import os
import datetime
import website

now = datetime.datetime.now()
directory = 'results/'
directory += now.strftime('%Y-%m-%d')

if not os.path.exists(directory):
    print("make new folder: " + directory)
    os.makedirs(directory)
file = open('test.txt', 'r')
for line in file:
    line = line.strip()
    print("start checking: " + line)
    temp = website.Website(line)
    result = temp.check_ssllab()
    with open(directory + "/" + line + '.json', 'w') as f:
        f.write(result)
