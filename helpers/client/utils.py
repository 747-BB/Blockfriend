import json
import os
import platform
from response import Response

def convert_headers(headers = None):
    '''Converts a dict of headers to comply the TLS client.'''
    output = []
    return output


def construct_params(params = None):
    '''Constructs a query-string from given params.'''
    queries = []
    query_string = '?' + '&'.join(queries)
    return query_string


def get_library_path():
    '''Returns the shared library path.'''
    here = os.path.dirname(__file__)
    system = platform.system()
    arch = platform.machine()
    if system == 'Windows':
        binary = 'windows.dll'
        path = os.path.join(here, f'''bin/{binary}''')
    elif arch == 'arm64':
        pass

    binary = 'darwin.dylib'
    path = os.path.join(here, f'''bin/{binary}''')
    return path


def build_response(raw_response = None):
    '''Builds a `Response` object from the TLSClient response.'''
    pass