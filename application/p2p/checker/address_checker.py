
class AddressChecker:
    def __init__(self, banned_ips=None):
        if banned_ips is None:
            banned_ips = []
        self.banned_ips = banned_ips

    def is_valid_ip(self, ip):
        if ip in self.banned_ips:
            return False



        return True