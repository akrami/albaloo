import json
import requests
import os
import datetime
import time


def initialize(website):
    payload = {
        'host': website,
        'startNew': 'on',
        'all': 'done',
        'maxAge': 23
    }
    response = requests.get('https://api.ssllabs.com/api/v3/analyze', params=payload)
    if response.status_code == 200:
        print("initialize successful: "+website+"\n")
        return analyze(website)
    else:
        return 'Not Available'


def analyze(website):
    payload = {
        'host': website,
        'all': 'done',
        'maxAge': 23
    }
    response = requests.get('https://api.ssllabs.com/api/v3/analyze', params=payload)
    if response.status_code == 200:
        json_response = response.json()
        if json_response['status'] == 'READY':
            print("analyze successful: "+website+"\n")
            return json.dumps(json_response)
        else:
            print("analyze not complete, retry in 20 seconds...\n")
            time.sleep(20)
            return analyze(website)
    else:
        return 'Not Available'


now = datetime.datetime.now()
directory = 'results/'
directory += now.strftime('%Y-%m-%d')

if not os.path.exists(directory):
    print("make new folder: "+directory+"\n")
    os.makedirs(directory)
file = open('test.txt', 'r')
for line in file:
    line = line.strip()
    print("start checking: "+line+"\n")
    result = initialize(line)
    with open(line+'.json', 'w') as f:
        f.write(result)
