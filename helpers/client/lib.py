import ctypes
import json
import uuid
from ctypes import c_void_p, cdll
from typing import Tuple
from utils import get_library_path

class Lib:
    loaded = False
    lib = None

    def load(cls):
        '''Loads the client shared library.'''
        if cls.loaded:
            return None
        path = None()
        cls.lib = cdll.LoadLibrary(path)
        cls.lib.initClient.restype = c_void_p
        cls.lib.request.restype = c_void_p
        cls.lib.changeProxy.restype = c_void_p
        cls.lib.freePointer.argtypes = (c_void_p,)
        cls.lib.freePointer.restype = None
        cls.loaded = True

    load = classmethod(load)

    def new_client(cls = None, config = None):
        '''Initializes a new client with given configuration.'''
        client_id = str(uuid.uuid4())
        config['id'] = client_id
        dumped = json.dumps(config)
        if not cls.loaded:
            cls.load()
        ptr = cls.lib.initClient(dumped.encode('utf-8'))
        string = ctypes.cast(ptr, ctypes.c_char_p).value.decode('utf-8')
        cls.lib.freePointer(ptr)
        return (json.loads(string), client_id)

    new_client = None(new_client)

    def change_proxy(cls = None, config = None):
        '''Updates the HTTP Proxy for given client-config.'''
        dumped = json.dumps(config)
        ptr = cls.lib.changeProxy(dumped.encode('utf-8'))
        string = ctypes.cast(ptr, ctypes.c_char_p).value.decode('utf-8')
        cls.lib.freePointer(ptr)
        return string

    change_proxy = None(change_proxy)

    def request(cls = None, config = None):
        '''Sends given request to the DLL and returns the response.'''
        dumped = json.dumps(config)
        ptr = cls.lib.request(dumped.encode('utf-8'))
        string = ctypes.cast(ptr, ctypes.c_char_p).value.decode('utf-8')
        cls.lib.freePointer(ptr)
        return string

    request = None(request)