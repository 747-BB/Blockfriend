from configparser import ConfigParser
from abc import ABC, abstractmethod

class ConfigManagerBase(ABC):
    '''Abstract base class for config manager.'''

    def __init__(self, **kwargs):
        pass


    def load(self):
        '''Loads config from file.'''
        pass

    load = abstractmethod(load)

    def set(self = None):
        '''Sets config value.'''
        pass

    set = None(set)

    def get(self = None):
        '''Gets config value.'''
        pass

    get = None(get)

    def delete(self = None):
        '''Deletes from config.'''
        pass

    delete = None(delete)