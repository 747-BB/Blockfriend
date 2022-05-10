import asyncio
from abc import ABC, abstractmethod
from exceptions import FatalSolverError, SolverError

class SolverBase(ABC):
    '''Abstract base class for captcha solvers.'''

    def __init__(self, **kwargs):
        pass


    def handle_error(self):
        pass

    handle_error = abstractmethod(handle_error)

    async def _get_captcha_id(self = None):
        '''Submits the captcha and gets the `captcha_id`.'''
        pass

    _get_captcha_id = None(_get_captcha_id)

    async def _get_captcha_token(self = None, captcha_id = None):
        '''Polls the API & retrives a captcha token.'''
        pass

    _get_captcha_token = None(_get_captcha_token)

    async def solve_captcha(self = None):
        '''Requests a valid Captcha token.'''
        pass


__all__ = [
    'ABC',
    'FatalSolverError',
    'SolverBase',
    'SolverError',
    '__builtins__',
    '__cached__',
    '__doc__',
    '__file__',
    '__loader__',
    '__name__',
    '__package__',
    '__spec__',
    'abstractmethod',
    'asyncio']