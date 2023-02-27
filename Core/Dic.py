import os.path
from os import path
import pickle
import Core.Cryption as Cryption

class Dic:

    def __init__(self):
        self.array = {}
        self.cryptPlatform = True
        self.path = os.getcwd() + "/passwords.crypt"

    def load(self):
        if path.exists(self.path):
            fil = open(self.path, "rb")
            self.array = pickle.load(fil)
            fil.close()

        return path.exists(self.path + "/passwords.crypt")

    def save(self, key = None):
        decrypt = False
        if self.cryptPlatform == False and key != None:
            self.encryptPlatforms(key)
            decrypt = True
        elif self.cryptPlatform == False and key == None:
            return False
        fil = open(self.path + "/passwords.crypt", "wb")
        pickle.dump(self.array, fil)
        fil.close()
        if decrypt:
            self.decryptPlatforms(key)

    def decryptPlatforms(self, key):
        crypt = Cryption.Cryption()
        crypt.setKey(key)
        result = {}
        if '__CryptPassMagicKey__' in self.array:
            result['__CryptPassMagicKey__'] = self.array['__CryptPassMagicKey__']
        for platform in self.listAll():
            result[crypt.decrypt(platform)] = self.array[platform]
        self.array = result
        self.cryptPlatform = False

    def encryptPlatforms(self, key):
        crypt = Cryption.Cryption()
        crypt.setKey(key)
        result = {}
        if '__CryptPassMagicKey__' in self.array:
            result['__CryptPassMagicKey__'] = self.array['__CryptPassMagicKey__']
        for platform in self.listAll():
            result[crypt.encrypt(platform)] = self.array[platform]
        self.array = result
        self.cryptPlatform = True


    def listAll(self):
        result = self.array
        if '__CryptPassMagicKey__' in result:
            result = {key: result[key] for key in result if key != "__CryptPassMagicKey__"}
        return [*result]

    def get(self, key):
        if key in self.array:
            return self.array[key]
        return False

    def set(self, key, value):
        self.array[key] = value

    def remove(self, key):
        if key in self.array:
            del self.array[key]
            return True
        return False

    