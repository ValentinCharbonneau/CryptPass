import Core.Dic as Dic
import Core.Connect as Connect
import Core.Cryption as Cryption
import os
import sys
import getpass

class Commands:

    def __init__(self, dic, parent):
        self.commands = [
            'help', 'list', 'see', 'add', 'modify', 'remove', 'changepwd', 'reset', 'clear', 'exit'
        ]
        self.dic = dic
        self.parent = parent

    def input(self):
        command = input('CryptPass>>> ').split(' ')
        if self._has(command[0].lower()):
            getattr(self, command[0].lower())(command[1:])
        else:
            print('Error: invalid command')
        self.input()

    # Differents commands
    def help(self, param = []):
        print("\n\nCommands available\n\n"
                + "\tHELP : print this message\n"
                + "\tLIST : print all platforms for which you have a registered password\n"
                + "\tSEE {platform} : print your password for platform\n"
                + "\tADD {platform} {password} : add new platform with its password\n"
                + "\tMODIFY {platform} {password} : modify password of platform\n"
                + "\tREMOVE {platform} : remove platform and its password\n"
                + "\tCHANGEPWD : change your password to unlock this application\n"
                + "\tRESET : deletes all passwords and reset this application\n"
                + "\tCLEAR : clear this screen\n"
                + "\tEXIT : close this application\n\n")

    def list(self, param = []):
        print('\n')
        counter = 0
        for platform in self.dic.listAll():
            print('\t- '+platform)
            counter+=1
        if counter == 0:
            print('\tNo password registered\n\tUse \'HELP\' command to see how use this application')
        print('\n')

    def see(self, param):
        if len(param) == 1 and self.dic.get(param[0]) != False:
            crypt = Cryption.Cryption()
            crypt.setKey(self.parent.getKey())
            print(param[0] + ' : ' + crypt.decrypt(self.dic.get(param[0])))
            getpass.getpass('Press \'Enter\'')
            self._clearLastLine()
            self._clearLastLine()
        else:
            print('Error: invalid argument')

    def add(self, param):
        if len(param) == 2:
            if self.dic.get(param[0]) == False:
                if len(param[0]) <= 63 and len(param[1]) <= 63:
                    crypt = Cryption.Cryption()
                    crypt.setKey(self.parent.getKey())
                    self.dic.set(param[0], crypt.encrypt(param[1]))
                    self._clearLastLine()
                    self.dic.save(crypt.getKey())
                    print('Password has been registered')
                else:
                    print('Error: platforms names and passwords cannot exceed 63 characters')
            else:
                print('Error: a password is already registered for this platform')
        else:
            print('Error: invalid argument')

    def modify(self, param):
        if len(param) == 2:
            if self.dic.get(param[0]) != False:
                if len(param[0]) <= 63 and len(param[1]) <= 63:
                    crypt = Cryption.Cryption()
                    crypt.setKey(self.parent.getKey())
                    self.dic.set(param[0], crypt.encrypt(param[1]))
                    self._clearLastLine()
                    self.dic.save(crypt.getKey())
                    print('Password has been modified')
                else:
                    print('Error: platforms names and passwords cannot exceed 63 characters')
            else:
                print('Error: no password registered for this platform')
        else:
            print('Error: invalid argument')

    def remove(self, param):
        if len(param) == 1:
            if self.dic.remove(param[0]):
                self.dic.save(self.parent.getKey())
                print('Platform \''+param[0]+'\' and its password has been removed')
            else:
                print('Error: no password registered for this platform')
        else:
            print('Error: invalid argument')

    def changepwd(self, param = []):
        auth = Connect.Connect()
        auth.setKey(self.parent.getAuth())
        attempt = 0
        while auth.connect() == False:
            os.system('cls||clear')
            if attempt > 0:
                print('Wrong password\n')
            auth.askIdentifier('Actual password : ')
            attempt+=1

        attempt = 0
        newAuth = Connect.Connect()
        while newAuth.connect() == False or newAuth.getDoubleHashPassword() == self.parent.getAuth():
            os.system('cls||clear')
            if newAuth.getDoubleHashPassword() == self.parent.getAuth():
                print('You dont change your password with your actual password\n')
            elif attempt > 0:
                print('You dont write the same password\n')

            newAuth.askIdentifier('New password : ')
            newAuth.setKey(newAuth.getDoubleHashPassword())
            newAuth.askIdentifier('Confirm password : ')

            attempt+=1
        del(attempt)
        
        self.dic.set('__CryptPassMagicKey__', newAuth.getDoubleHashPassword())
        crypt = Cryption.Cryption()
        crypt.setKey(self.parent.getKey())
        newCrypt = Cryption.Cryption()
        newCrypt.setKey(newAuth.getPasswordHash())
        for platform in self.dic.listAll():
            self.dic.set(platform, newCrypt.encrypt(crypt.decrypt(self.dic.get(platform))))
        self.dic.encryptPlatforms(newAuth.getPasswordHash())
        self.dic.save()

        os.system('cls||clear')
        getpass.getpass('Password has been changed, press \'Enter\' to restart')
        self._restart()

    def reset(self, param = []):
        os.system('cls||clear')

        auth = Connect.Connect()
        auth.askIdentifier()
        auth.setKey(self.parent.getAuth())

        if auth.connect():
            os.remove("passwords.crypt")
            os.system('cls||clear')
            getpass.getpass('Application was reset, press \'Enter\' to start')
            self._restart()
        else:
            print('Wrong password')
            getpass.getpass('Press \'Enter\'')
            os.system('cls||clear')

    def exit(self, param = []):
        os.system('cls||clear')
        sys.exit()

    def clear(self, param = []):
        os.system('cls||clear')

    # Private methods
    def _has(self, method):
        return method in self.commands

    def _clearLastLine(self):
        sys.stdout.write("\033[A") #back to previous line
        sys.stdout.write("\033[K") #clear line
    
    def _restart(self):
        self.parent.start()

    