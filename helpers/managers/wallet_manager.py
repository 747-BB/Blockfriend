from wallet_manager_base import WalletManagerBase
import os
import sys
import base64
import hashlib
import json
from cryptography.fernet import Fernet
WALLET_FILE_TEMPLATE = {
    'SOL': [],
    'ETH': [] }

class WalletManager(WalletManagerBase):
    '''Universal Wallet Manager.'''

    def __init__(self, **kwargs):
        self.application_path = self.get_path()
        self.is_instansiated = os.path.isfile(f'''{self.application_path}/{self.filename}''')
        self.decryption_key = self.get_key()
        self.fernet = Fernet(self.decryption_key)
        if not self.is_instansiated:
            self.instansiate(self.filename, **('filename',))
        is_decrypted = False


    def verify_password(self, password):
        return base64.urlsafe_b64encode(hashlib.md5(password.encode()).hexdigest().encode()) == self.decryption_key


    def set_key(self = None):
        print('Welcome to Blockfriend. We recognize this as your first run of the program.\nYou must now specify an encryption key for your wallet file. Do NOT lose or forget this key, we can not stress this enough.')
        k1 = input('Please specify an encryption key: ')
        k2 = input('Please re-enter your encryption key: ')
        if k1 == k2:
            print(f'''You have used: {k1} as your encryption key''')
            input('Press Enter to continue.')
            return k1
        None("Your inputs didn't match. Please try again.", '\n\n', **('end',))


    def get_key(self):
        if not self.is_instansiated:
            decryption_key = self.set_key()
        else:
            decryption_key = input('Please enter your encryption key: ')
        return base64.urlsafe_b64encode(hashlib.md5(decryption_key.encode()).hexdigest().encode())


    def get_path(self = None):
        if getattr(sys, 'frozen', False):
            if os.name == 'posix':
                return os.path.dirname(sys.argv[0])
            return None
        return os.path.abspath(os.curdir)


    def instansiate(self = None, filename = None):
        """Instansiate wallet file if it doesn't exist."""
        if not self.is_instansiated:
            self.wallets = WALLET_FILE_TEMPLATE
            self.save()


    def read(self = None):
        '''Reads wallets from file.'''
        with open(f'''{self.application_path}/{self.filename}''', 'rb') as f:
            data = f.read()
            None(None, None, None)


    def save(self):
        '''Saves wallets to file (encrypted).'''
        with open(f'''{self.application_path}/{self.filename}''', 'wb') as f:
            f.write(self.encrypt(json.dumps(self.wallets)))
            None(None, None, None)


    def encrypt(self = None, data = None):
        '''Encrypts wallet file data using the Fernet algorithm'''
        return self.fernet.encrypt(data.encode())


    def decrypt(self = None, data = None):
        '''Decrypts wallet file data using the Fernet algorithm'''
        return self.fernet.decrypt(data).decode()


    def add(self = None, chain = None, entry = None):
        '''Adds wallet.'''
        return self.wallets[chain].append(entry)


    def remove(self = None, chain = None, entry = None):
        '''Removes wallet.'''
        idx = self.wallets[chain].index(entry)
        del self.wallets[chain][idx]
        return self.save()


    def update(self = None, chain = None, old = None, new = {
        'chain': str,
        'old': dict,
        'new': dict,
        'return': dict }):
        '''Updates wallet.'''
        idx = self.wallets[chain].index(old)
        self.wallets[chain][idx] = new
        return self.save()


    def set_new_password(self = None, user_input = None):
        old = user_input.get('old_password')
        new = user_input.get('new_password')
        confirm = user_input.get('new_password_confirm')
        old = base64.urlsafe_b64encode(hashlib.md5(old.encode()).hexdigest().encode())
        if old == self.decryption_key:
            if new == confirm:
                self.wallets = self.read()
                self.decryption_key = base64.urlsafe_b64encode(hashlib.md5(confirm.encode()).hexdigest().encode())
                self.fernet = Fernet(self.decryption_key)
                self.save()
                print(f'''Succesfully set new password to {confirm}!''')
            else:
                print('Unable to confirm new password, please try again...')
        else:
            print('Incorrect old password, please try again...')