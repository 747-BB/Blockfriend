import requests
import platform
import sys
import os

class AutoUpdater:

    def __init__(self, **kwargs):
        self.am = kwargs.get('am')
        self.current_platform = platform.system().lower()
        if getattr(sys, 'frozen', False):
            if os.name == 'posix':
                self.application_path = os.path.dirname(sys.argv[0])
            else:
                self.application_path = '.'
        else:
            self.application_path = os.path.abspath(os.curdir)


    def check_for_update(self, current_build_number):
        print('[AutoUpdater] Checking for update...')
        headers = {
            'Authorization': self.am.authorization_header,
            'User-Agent': 'Blockfriend v1' }
        data = {
            'license': self.am.license_key,
            'hwid': self.am.hwid,
            'platform': self.current_platform }


    def download_bot(self, build_number):
        headers = {
            'User-Agent': 'BlockFriend Updater' }
        params = {
            'platform': self.current_platform,
            'license': self.am.license_key }
        file_name = f'''BlockFriend_b{build_number}.exe''' if self.current_platform == 'windows' else f'''BlockFriend_b{build_number}'''
        dest_path = f'''{self.application_path}/{file_name}'''
        download_link = f'''https://blockfriend.net/api/download/{file_name}'''
        print('[AutoUpdater] Initiating download for:', file_name)