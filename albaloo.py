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
        print("initialize successful: "+website)
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
            print("analyze successful: "+website)
            return json.dumps(json_response, sort_keys=False, indent=4)
        elif json_response['status'] == 'ERROR':
            print("analyze failed: "+website)
            return json_response['statusMessage']
        else:
            print("analyze "+website+", status: "+json_response['status']+", retry in 20 seconds...")
            time.sleep(20)
            return analyze(website)
    else:
        return 'Not Available'


now = datetime.datetime.now()
directory = 'results/'
directory += now.strftime('%Y-%m-%d')

if not os.path.exists(directory):
    print("make new folder: "+directory)
    os.makedirs(directory)
file = open('test.txt', 'r')
for line in file:
    line = line.strip()
    print("start checking: "+line)
    result = initialize(line)
    with open(directory+"/"+line+'.json', 'w') as f:
        f.write(result)
