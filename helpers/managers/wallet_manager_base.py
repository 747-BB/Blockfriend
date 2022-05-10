from abc import ABC, abstractmethod

class WalletManagerBase(ABC):
    '''Abstract base class for wallet manager.'''

    def __init__(self, **kwargs):
        pass


    def set_key(self = None):
        '''Lets user choose an encryption key for their wallet file.'''
        pass

    set_key = None(set_key)

    def get_key(self = None):
        '''Returns encryption key'''
        pass

    get_key = None(get_key)

    def get_path(self = None):
        '''Returns path of Wallet Directory'''
        pass

    get_path = None(get_path)

    def instansiate(self, filename):
        pass

    instansiate = abstractmethod(instansiate)

    def read(self = None):
        '''Reads wallets from file.'''
        pass

    read = None(read)

    def save(self):
        pass

    save = abstractmethod(save)

    def encrypt(self = None, data = None):
        pass

    encrypt = None(encrypt)

    def decrypt(self = None, data = None):
        pass

    decrypt = None(decrypt)

    def add(self = None, chain = None, entry = abstractmethod):
        '''Adds wallet.'''
        pass

    add = None(add)

    def remove(self = None, chain = None, entry = abstractmethod):
        '''Removes wallet.'''
        pass

    remove = None(remove)

    def update(self = None, chain = None, old = abstractmethod, new = {
        'chain': str,
        'old': dict,
        'new': dict,
        'return': dict }):
        '''Updates wallet.'''
        pass

    update = None(update)