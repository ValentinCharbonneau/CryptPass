class Cryption:

    def __init__(self):
        self.key = 'ff'

    def encrypt(self, target):
        if len(target) <= 63:
            fullTarget = hex(len(target.encode('utf-8').hex()))[2:]
            if len(fullTarget) !=2:
                fullTarget = '0'+fullTarget
            while len(fullTarget) < 128:
                fullTarget += target.encode('utf-8').hex()
            fullTarget = fullTarget[:128]
        return hex(int(self.key, 16) ^ int(fullTarget, 16))[2:]

    def decrypt(self, target):
        fullDecrypt = hex(int(self.key, 16) ^ int(target, 16))[2:]
        if len(fullDecrypt) == 127:
            fullDecrypt = '0' + fullDecrypt
        lenTarget = fullDecrypt[:2]
        resultCrypt = fullDecrypt[2:int(lenTarget, 16)+2]
        return bytes.fromhex(resultCrypt).decode('utf-8')

    def setKey(self, key):
        self.key = key
    
    def getKey(self):
        return self.key