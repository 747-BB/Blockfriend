import json
from typing import Optional

class Response:
    """The :class:`Response <Response>` object, which contains a
\tserver's response to an HTTP request.
\t"""

    def __init__(self, text = None, status_code = None, headers = None, error = {
        'text': str,
        'status_code': int,
        'headers': dict,
        'error': Optional[dict] }):
        self.text = text
        self.status_code = status_code
        self.headers = headers
        self.error = error


    def __repr__(self):
        return f'''<Response [{self.status_code}]>'''


    def json(self = None):
        '''Returns the json-encoded content of a response, if any.'''
        pass