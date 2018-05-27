import json
import time
import socket
import requests
import re
from termcolor import colored


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

    def check_ssllab(self, verbose=True):
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
            if verbose:
                print("[{0}] SSLLAB: Connection Error! retry in 20 seconds...".format(colored(self.address, 'green')))
            time.sleep(20)
            return self.check_ssllab(verbose)
        except TimeoutError:
            if verbose:
                print("[{0}] SSLLAB: Timeout Error! retry in 20 seconds...".format(colored(self.address, 'green')))
            time.sleep(20)
            return self.check_ssllab(verbose)
        else:
            if response.status_code == 200:
                if verbose:
                    print("[{0}] SSLLAB: Initiated!".format(colored(self.address, 'green')))
                return self.__analyze_ssllab(verbose)
            else:
                return 'Not Available'

    def __analyze_ssllab(self, verbose=True):
        payload = {
            'host': self.address,
            'all': 'done',
            'maxAge': 23
        }
        try:
            response = requests.get('https://api.ssllabs.com/api/v3/analyze', params=payload)
        except requests.exceptions.ConnectionError:
            if verbose:
                print("[{0}] SSLLAB: Connection Error! retry in 20 seconds...".format(colored(self.address, 'green')))
            time.sleep(20)
            return self.__analyze_ssllab(verbose)
        except TimeoutError:
            if verbose:
                print("[{0}] SSLLAB: Timeout Error! retry in 20 seconds...".format(colored(self.address, 'green')))
            time.sleep(20)
            return self.__analyze_ssllab(verbose)
        else:
            if response.status_code == 200:
                json_response = response.json()
                if json_response['status'] == 'READY':
                    if verbose:
                        print("[{0}] SSLLAB: Analyze Successful!".format(colored(self.address, 'green')))
                    self.ssllab_result = json.dumps(json_response)
                    return self.ssllab_result
                elif json_response['status'] == 'ERROR':
                    if verbose:
                        print("[{0}] SSLLAB: Analyze Failed!".format(colored(self.address, 'green')))
                    return json_response['statusMessage']
                else:
                    if verbose:
                        print("[{0}] SSLLAB: Status: {1}".format(colored(self.address, 'green'), json_response['status']))
                    time.sleep(20)
                    return self.__analyze_ssllab(verbose)
            else:
                return 'Not Available'

    def check_ip(self, verbose=True):
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

    def check_redirect(self, verbose=True):
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

    def check_hsts(self, verbose=True):
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
