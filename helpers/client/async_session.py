import asyncio
import functools
from lib import Lib
from request import Request
from response import Response
from utils import build_response

class AsyncSession:

    def __init__(self = None, fingerprint = None, timeout = None, proxy = ('chrome83', 20, None, False), debug = {
        'fingerprint': str,
        'timeout': int,
        'proxy': str,
        'debug': bool }):
        '''Initializer for AsyncSession objects.

\t\tfingerprint: The JA3 fingerprint to be used.
\t\ttimeout: The timeout for each request (In seconds).
\t\tdebug: Whether or not to debug Request & Response.
\t\t'''
        self.lib = Lib()
        self.fingerprint = fingerprint
        self.timeout = timeout
        self.proxy = proxy
        self.debug = debug
        self.initialized = False
        self.headers = { }


    async def init(self):
        '''Initializes the AsyncSession connection.'''
        config = {
            'type': 'preset',
            'preset': self.fingerprint }
        if self.proxy:
            config['proxy'] = self.proxy
        loop = asyncio.get_running_loop()
        await loop.run_in_executor(None, functools.partial(self.lib.new_client, config))
        #(response, self.client_id) = <NODE:27>Unsupported Node type: 27

        if response.get('Success'):
            self.initialized = True
        else:
            raise Exception('Error creating Session')


    async def change_proxy(self = None, proxy = None):
        """Changes this client's selected proxy.
\t\t
\t\tProxy should be in format: http://username:password@ip:port
\t\t"""
        config = {
            'id': self.client_id,
            'proxy': proxy }
        loop = asyncio.get_running_loop()
        await loop.run_in_executor(None, functools.partial(self.lib.change_proxy), config)


    async def request(self = None, method = None, url = None, **kwargs):
        '''Constructs a `Request` and sends it.'''
        if not self.initialized:
            raise Exception('This AsyncSession has not been initialized.')


    async def get(self = None, url = None, **kwargs):
        '''Sends a GET request.'''
        pass


    async def options(self = None, url = None, **kwargs):
        '''Sends a OPTIONS request.'''
        pass


    async def head(self = None, url = None, **kwargs):
        '''Sends a HEAD request.'''
        pass


    async def post(self = None, url = None, **kwargs):
        '''Sends a POST request.'''
        pass


    async def put(self = None, url = None, **kwargs):
        '''Sends a PUT request.'''
        pass


    async def patch(self = None, url = None, **kwargs):
        '''Sends a PATCH request.'''
        pass


    async def delete(self = None, url = None, **kwargs):
        '''Sends a DELETE request.'''
        pass


    async def send(self = None, request = None):
        '''Sends given `Request`.'''
        config = request.prepare()
        loop = asyncio.get_running_loop()
        await loop.run_in_executor(None, functools.partial(self.lib.request, config))
        #raw_response = <NODE:27>Unsupported Node type: 27

        response = build_response(raw_response)
        return response