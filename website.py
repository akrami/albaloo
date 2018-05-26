import json
import time

import requests


class Website:
    """
    Website class
    """

    def __init__(self, address):
        self.address = address
        self.ssllab_result = ''
        self.ssllab_rating = ''
        self.ip = '0.0.0.0'
        self.redirect = False
        self.hsts = False

    def check_ssllab(self):
        payload = {
            'host': self.address,
            'startNew': 'on',
            'all': 'done',
            'maxAge': 23
        }
        response = requests.get('https://api.ssllabs.com/api/v3/analyze', params=payload)
        if response.status_code == 200:
            print("initialize successful: " + self.address)
            return self.__analyze_ssllab()
        else:
            return 'Not Available'

    def __analyze_ssllab(self):
        payload = {
            'host': self.address,
            'all': 'done',
            'maxAge': 23
        }
        response = requests.get('https://api.ssllabs.com/api/v3/analyze', params=payload)
        if response.status_code == 200:
            json_response = response.json()
            if json_response['status'] == 'READY':
                print("analyze successful: " + self.address)
                return json.dumps(json_response, sort_keys=False, indent=4)
            elif json_response['status'] == 'ERROR':
                print("analyze failed: " + self.address)
                return json_response['statusMessage']
            else:
                print("analyze " + self.address + ", status: " + json_response['status'] + ", retry in 20 seconds...")
                time.sleep(20)
                return self.__analyze_ssllab()
        else:
            return 'Not Available'

    def get_ip(self):
        self.ip = '0.0.0.0'
        return True

    def check_redirect(self):
        self.redirect = True
        return True

    def check_hsts(self):
        self.hsts = True
        return True