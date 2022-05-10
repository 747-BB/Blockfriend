from abc import ABC, abstractmethod

class ReleaseManagerBase(ABC):
    '''Abstract base class for release manager.'''

    def __init__(self, **kwargs):
        pass


    def get_path(self = None):
        '''Returns path of Main Directory'''
        pass

    get_path = None(get_path)

    def instansiate(self, filename):
        pass

    instansiate = abstractmethod(instansiate)

    def read(self = None):
        '''Reads releases from file.'''
        pass

    read = None(read)

    def save(self):
        pass

    save = abstractmethod(save)

    def add(self = None, chain = None, entry = abstractmethod):
        '''Adds release.'''
        pass

    add = None(add)

    def remove(self = None, chain = None, entry = abstractmethod):
        '''Removes release.'''
        pass

    remove = None(remove)

    def update(self = None, chain = None, old = abstractmethod, new = {
        'chain': str,
        'old': dict,
        'new': dict,
        'return': dict }):
        '''Updates release.'''
        pass

    update = None(update)