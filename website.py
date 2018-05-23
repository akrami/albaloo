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
        self.ssllab_result = 'ssllab result'
        self.ssllab_rating = 'ssllab rating'
        return True

    def analyze_ssllab(self):
        return True

    def get_ip(self):
        self.ip = '0.0.0.0'
        return True

    def check_redirect(self):
        self.redirect = True
        return True

    def check_hsts(self):
        self.hsts = True
        return True