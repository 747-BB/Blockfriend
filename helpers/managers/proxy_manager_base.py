from abc import ABC, abstractmethod

class ProxyManagerBase(ABC):
    '''Abstract base class for proxy manager.'''

    def __init__(self, **kwargs):
        pass


    def load(self):
        '''Loads proxies from file.'''
        pass

    load = abstractmethod(load)

    def add(self):
        '''Adds a formatted proxy to proxy list.'''
        pass

    add = abstractmethod(add)

    def format_proxy(self):
        '''Formats proxies for use in tls client'''
        pass

    format_proxy = abstractmethod(format_proxy)