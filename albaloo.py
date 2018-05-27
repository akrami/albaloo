import os
import datetime
import website

now = datetime.datetime.now()
directory = 'results/'
directory += now.strftime('%Y-%m-%d')

if not os.path.exists(directory):
    print("[Main] New Directory: {0}".format(directory))
    os.makedirs(directory)
file = open('test.txt', 'r')
for line in file:
    line = line.strip()
    temp = website.Website(line)
    ip = temp.check_ip()
    print('[{0}] IP: {1}'.format(line, ip))
    print('[{0}] HTTPS REDIRECT: {1}'.format(line, temp.check_redirect()))
    print("[{0}] SSLLAB: Start ".format(line))
    result = temp.check_ssllab()
    print("[{0}] SSLLAB: Finished ".format(line))
    with open(directory + "/" + line + '.json', 'w') as f:
        f.write(result)
