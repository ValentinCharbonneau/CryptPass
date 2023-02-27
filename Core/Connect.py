import getpass
import hashlib

class Connect:

    def __init__(self):
        self.hashPassword = ''
        self.doubleHashPassword = ''
        self.key = 'ff'

    def askIdentifier(self, message = 'Password : '):
        hasher = hashlib.sha3_512()
        hasher.update(getpass.getpass(message).encode('utf-8'))
        pwd = hasher.digest()
        self.hashPassword = pwd.hex()
        
        hasher = hashlib.sha3_512()
        hasher.update(pwd)
        self.doubleHashPassword = hasher.hexdigest()

    def connect(self):
        return self.doubleHashPassword == self.key

    def getPasswordHash(self):
        return self.hashPassword

    def getDoubleHashPassword(self):
        return self.doubleHashPassword

    def setKey(self, key):
        self.key = key
