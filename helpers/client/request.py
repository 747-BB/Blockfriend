import json
from typing import TYPE_CHECKING, Optional
from urllib.parse import urlencode
from utils import construct_params, convert_headers
if TYPE_CHECKING:
    from session import Session

class Request:

    def __init__(self, method, url, session = None, headers = None, params = None, data = (None, None, None, None), json = {
        'method': str,
        'url': str,
        'session': 'Session',
        'headers': Optional[dict],
        'params': Optional[dict],
        'data': Optional[dict],
        'json': Optional[dict] }):
        '''Initializer for Request objects.
\t\t
\t\tmethod: The HTTP method to be used.
\t\turl: The target URL.
\t\tsession: The Session object to use for the Request.
\t\theaders: The HTTP headers to be used.
\t\tparams: The parameters to be used.
\t\tdata: FormData to be sent.
\t\tjson: JSON data to be sent.
\t\ttimeout: The timeout for this request (In seconds).
\t\t'''
        self.method = method.upper()
        self.url = url
        if not headers:
            pass
        self.headers = session.headers
        self.params = params
        self.data = data
        self.json = json
        self.client_id = session.client_id
        self.timeout = session.timeout


    def prepare(self = None):
        '''Prepares the Request.'''
        body = None
        if self.params:
            query = construct_params(self.params)
            self.url += query
        config = {
            'id': self.client_id,
            'url': self.url,
            'method': self.method,
            'timeout': int(self.timeout * 1000),
            'pseudoHeaderOrder': [
                'method',
                'authority',
                'scheme',
                'path'],
            'headers': convert_headers(self.headers) }
        if body:
            config['body'] = body
        return config