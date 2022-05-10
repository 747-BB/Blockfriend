from proxy_manager_base import ProxyManagerBase
import __main__
import sys
import os

class ProxyManager(ProxyManagerBase):

    def __init__(self, **kwargs):
        self.proxy_list = []
        self.load()


    def load(self):
        '''Loads proxies from file.'''
        if getattr(sys, 'frozen', False):
            if os.name == 'posix':
                self.application_path = os.path.dirname(sys.argv[0])
            else:
                self.application_path = '.'
        else:
            self.application_path = os.path.abspath(os.curdir)


    def add(self = None, proxy_str = None):
        '''Adds a formatted proxy to proxy list.'''
        formatted_proxy = self.format_proxy(proxy_str)
        if not formatted_proxy:
            return None
        None.proxy_list.append(formatted_proxy)


    def format_proxy(self = None, proxy_str = None):
        '''Formats proxies for use in tls client'''
        if isinstance(proxy_str, str) and ':' not in proxy_str or proxy_str == 'ip:port:username:password\n':
            return None
        split_proxy = None.strip().split(':')
        if len(split_proxy) == 4:
            return f'''http://{split_proxy[2]}:{split_proxy[3]}@{split_proxy[0]}:{split_proxy[1]}'''
        if None(split_proxy) == 2:
            return f'''http://{split_proxy[0]}:{split_proxy[1]}'''