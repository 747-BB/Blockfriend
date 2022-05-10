from lib import Lib
from request import Request
from response import Response
from utils import build_response

class Session:

    def __init__(self = None, fingerprint = None, timeout = None, proxy = ('chrome83', 20, None, False), debug = {
        'fingerprint': str,
        'timeout': int,
        'proxy': str,
        'debug': bool }):
        '''Initializer for Session objects.

\t\tfingerprint: The JA3 fingerprint to be used.
\t\ttimeout: The timeout for each request (In seconds).
\t\tdebug: Whether or not to debug Request & Response.
\t\t'''
        self.lib = Lib()
        self.fingerprint = fingerprint
        self.timeout = timeout
        self.proxy = proxy
        self.debug = debug
        self.headers = { }
        config = {
            'type': 'preset',
            'preset': self.fingerprint }
        if self.proxy:
            config['proxy'] = self.proxy
        (response, self.client_id) = self.lib.new_client(config)
        if not response.get('Success'):
            raise Exception('Error creating Session')


    def request(self = None, method = None, url = None, **kwargs):
        '''Constructs a `Request` and sends it.'''
        pass


    def change_proxy(self = None, proxy = None):
        """Changes this client's selected proxy.
\t\t
\t\tProxy should be in format: http://username:password@ip:port
\t\t"""
        config = {
            'id': self.client_id,
            'proxy': proxy }
        self.lib.change_proxy(config)


    def get(self = None, url = None, **kwargs):
        '''Sends a GET request.'''
        pass


    def options(self = None, url = None, **kwargs):
        '''Sends a OPTIONS request.'''
        pass


    def head(self = None, url = None, **kwargs):
        '''Sends a HEAD request.'''
        pass


    def post(self = None, url = None, **kwargs):
        '''Sends a POST request.'''
        pass


    def put(self = None, url = None, **kwargs):
        '''Sends a PUT request.'''
        pass


    def patch(self = None, url = None, **kwargs):
        '''Sends a PATCH request.'''
        pass


    def delete(self = None, url = None, **kwargs):
        '''Sends a DELETE request.'''
        pass


    def send(self = None, request = None):
        '''Sends given `Request`.'''
        config = request.prepare()
        raw_response = self.lib.request(config)
        response = build_response(raw_response)
        return response