from deprotocol.utils import crypto_funcs as cf


class DataHandler:

    def __init__(self, node):
        self.node = node

    def encryption_handler(self, dta):
        if dta["rnid"] == self.node.id:
            dta["data"] = cf.decrypt(dta["data"], self.node.privatekey)
            return dta
        elif dta["rnid"] is None:
            return dta
        else:
            return False
