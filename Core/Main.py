import Core.Dic as Dic
import Core.Connect as Connect
import Core.Cryption as Cryption
import Core.Commands as Commands
import getpass

# To use ASCII special characters on Windows
import os
if os.name == 'nt':
    from ctypes import windll
    k = windll.kernel32
    k.SetConsoleMode(k.GetStdHandle(-11), 7)

class Main:

    def __init__(self):
        self.dictionnary = Dic.Dic()
        self.command = Commands.Commands(self.dictionnary, self)

        self.key = ''
        self.auth = ''

    def start(self):
        self.dictionnary = Dic.Dic()
        self.command = Commands.Commands(self.dictionnary, self)

        appWasInit = False
        if self.dictionnary.load():
            if self.dictionnary.get('__CryptPassMagicKey__'):
                appWasInit = True
        
        if appWasInit:
            self._launchApp()
        else:
            self._initApp()

    def _launchApp(self):
        connection = Connect.Connect()
        connection.setKey(self.dictionnary.get('__CryptPassMagicKey__'))
        attempt = 0

        # Authentication
        while connection.connect() == False:
            os.system('cls||clear')
            if attempt > 0:
                print('Wrong password\n')
            connection.askIdentifier()
            attempt+=1
        del(attempt)

        self.key = connection.getPasswordHash()
        self.auth = connection.getDoubleHashPassword()

        self.dictionnary.decryptPlatforms(self.key)

        os.system('cls||clear')
        print('\n\n\t###\tCryptPass\t###\n')

        self.command.help()
        self.command.input()

    def _initApp(self):
        attempt = 0
        newAuth = Connect.Connect()
        while newAuth.connect() == False:
            os.system('cls||clear')
            print('\n\n\t###\tWelcome to CryptPass\t###\n')
            print('\nThis application is a password manager\nNow we will initialize it')
            print('\nTo begin, you must choice a password to unlock this application\n')
            if attempt > 0:
                print('\nYou dont write the same password\n')

            newAuth.askIdentifier('Your password : ')
            newAuth.setKey(newAuth.getDoubleHashPassword())
            newAuth.askIdentifier('Confirm password : ')

            attempt+=1
        del(attempt)

        self.dictionnary.set('__CryptPassMagicKey__', newAuth.getDoubleHashPassword())
        self.dictionnary.save()

        os.system('cls||clear')
        getpass.getpass('Password has been registered, press \'Enter\' to start')
        self.start()

    def getKey(self):
        return self.key

    def getAuth(self):
        return self.auth



