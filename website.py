import json
from time import sleep
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
        except requests.exceptions.ConnectionError:
            sleep(20)
            return self.check_ssllab()
        except TimeoutError:
            sleep(20)
            return self.check_ssllab()
        else:
            if response.status_code == 200:
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
        except requests.exceptions.ConnectionError:
            sleep(20)
            return self.__analyze_ssllab()
        except TimeoutError:
            sleep(20)
            return self.__analyze_ssllab()
        else:
            if response.status_code == 200:
                json_response = response.json()
                if json_response['status'] == 'READY':
                    self.ssllab_result = json.dumps(json_response)
                    return self.ssllab_result
                elif json_response['status'] == 'ERROR':
                    return json_response['statusMessage']
                else:
                    sleep(20)
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
        if re.match(r'^https://', self.address):
            host = self.address
        elif re.match(r'^http://', self.address):
            host = self.address.replace('http://', 'https://')
        else:
            host = 'https://{0}'.format(self.address)
        try:
            response = requests.get(host)
        except ConnectionError:
            self.hsts = False
        except requests.exceptions.SSLError:
            self.hsts = False
        else:
            self.hsts = True if 'strict-transport-security' in response.headers else False
        finally:
            return self.hsts
