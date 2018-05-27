import json
import time
import socket
import requests
import re


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
        """
        Check SSLLAB Result and Score
        :return: json or error
        """
        payload = {
            'host': self.address,
            'startNew': 'on',
            'all': 'done',
            'maxAge': 23
        }
        try:
            response = requests.get('https://api.ssllabs.com/api/v3/analyze', params=payload)
        except ConnectionError:
            print("[{0}] SSLLAB: Connection Error! retry in 20 seconds...".format(self.address))
            time.sleep(20)
            return self.check_ssllab()
        else:
            if response.status_code == 200:
                print("[{0}] SSLLAB: Initiated!".format(self.address))
                return self.__analyze_ssllab()
            else:
                return 'Not Available'

    def __analyze_ssllab(self):
        payload = {
            'host': self.address,
            'all': 'done',
            'maxAge': 23
        }
        try:
            response = requests.get('https://api.ssllabs.com/api/v3/analyze', params=payload)
        except ConnectionError:
            print("[{0}] SSLLAB: Connection Error! retry in 20 seconds...".format(self.address))
            time.sleep(20)
            return self.__analyze_ssllab()
        else:
            if response.status_code == 200:
                json_response = response.json()
                if json_response['status'] == 'READY':
                    print("[{0}] SSLLAB: Analyze Successful!".format(self.address))
                    return json.dumps(json_response, sort_keys=False, indent=4)
                elif json_response['status'] == 'ERROR':
                    print("[{0}] SSLLAB: Analyze Failed!".format(self.address))
                    return json_response['statusMessage']
                else:
                    print("[{0}] SSLLAB: Status: {1}".format(self.address, json_response['status']))
                    time.sleep(20)
                    return self.__analyze_ssllab()
            else:
                return 'Not Available'

    def check_ip(self):
        """
        Get Website IP
        :return: string
        """
        try:
            self.ip = socket.gethostbyname(self.address)
        except socket.gaierror:
            self.ip = "Not Found"
        finally:
            return self.ip

    def check_redirect(self):
        """
        is http redirected to https
        :return: boolean
        """
        if re.match(r'^https://', self.address):
            host = self.address.replace('https://', 'http://')
        elif re.match(r'^http://', self.address):
            host = self.address
        else:
            host = 'http://{0}'.format(self.address)
        try:
            response = requests.get(host)
        except ConnectionError:
            self.redirect = False
        else:
            self.redirect = True if re.match(r'^https://', response.url) else False
        finally:
            return self.redirect

    def check_hsts(self):
        """
        check if hsts is available on ssl
        :return: boolean
        """
        self.hsts = True
        return True
