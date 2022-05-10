from config_manager_base import ConfigManagerBase
from configparser import ConfigParser
import __main__
import sys
import os
CONFIG_FILE_TEMPLATE = {
    'Authentication': [
        ('LicenseKey', '')],
    'General': [
        ('WalletFile', 'wallets.json'),
        ('ReleaseFile', 'releases.json')],
    'Captchas': [
        ('2captcha', ''),
        ('capmonster', ''),
        ('anticaptcha', '')],
    'Webhooks': [
        ('SuccessWebhook', ''),
        ('ErrorWebhook', '')],
    'SOL': [
        ('RPC', 'https://solana-api.projectserum.com')],
    'ETH': [
        ('RPC', 'https://')] }

class ConfigManager(ConfigManagerBase):

    def __init__(self, **kwargs):
        self.config = ConfigParser()
        self.load()


    def load(self):
        '''Loads config from file.'''
        if getattr(sys, 'frozen', False):
            if os.name == 'posix':
                self.application_path = os.path.dirname(sys.argv[0])
            else:
                self.application_path = '.'
        else:
            self.application_path = os.path.abspath(os.curdir)


    def set(self = None, section = None, key = None, value = {
        'section': str,
        'key': str,
        'value': any }):
        '''Sets config value.'''
        self.config.set(section, key, value)
        with open(f'''{self.application_path}/config.ini''', 'w') as configfile:
            self.config.write(configfile)
            None(None, None, None)


    def get(self = None, section = None, key = None, data_type = (None,)):
        '''Gets config value.'''
        if data_type in (str, None):
            return self.config.get(section, key)
        return None.config.__getattribute__(f'''get{data_type.__name__}''')(section, key)


    def delete(self = None):
        '''Deletes from config.'''
        raise NotImplementedError()