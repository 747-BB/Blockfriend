import base64
import hashlib
import json
import os
import sys
from typing import Optional
from release_manager_base import ReleaseManagerBase
RELEASE_FILE_TEMPLATE = {
    'SOL': [],
    'ETH': [] }

class ReleaseManager(ReleaseManagerBase):
    '''Universal Release Manager.'''

    def __init__(self, **kwargs):
        self.application_path = self.get_path()
        self.is_instansiated = os.path.isfile(f'''{self.application_path}/{self.filename}''')
        if not self.is_instansiated:
            self.instansiate(self.filename, **('filename',))
        self.releases = self.read()


    def get_path(self = None):
        if getattr(sys, 'frozen', False):
            if os.name == 'posix':
                return os.path.dirname(sys.argv[0])
            return None
        return os.path.abspath(os.curdir)


    def instansiate(self = None, filename = None):
        """Instansiate releases file if it doesn't exist."""
        if not self.is_instansiated:
            self.releases = RELEASE_FILE_TEMPLATE
            self.save()


    def read(self = None):
        '''Reads releases from file.'''
        pass


    def save(self):
        '''Saves releases to file.'''
        with open(f'''{self.application_path}/{self.filename}''', 'w') as f:
            json.dump(self.releases, f, 4, **('indent',))
            None(None, None, None)


    def add(self = None, chain = None, entry = None):
        '''Adds release.'''
        return self.releases[chain].append(entry)


    def remove(self = None, chain = None, entry = None):
        '''Removes release.'''
        idx = self.releases[chain].index(entry)
        del self.releases[chain][idx]
        return self.save()


    def update(self = None, chain = None, old = None, new = {
        'chain': str,
        'old': dict,
        'new': dict,
        'return': dict }):
        '''Updates release.'''
        idx = self.releases[chain].index(new)
        self.releases[chain][idx] = new
        return self.save()


    def get(self = None, chain = None, name = None):
        '''Returns the release matching given chain & name.'''
        pass