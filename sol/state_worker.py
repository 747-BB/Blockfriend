import asyncio
import time
import random
from typing import TYPE_CHECKING, Coroutine
if TYPE_CHECKING:
    from static.templates import State

class StateWorker:
    state: 'State' = None
    blockhashes: 'Blockhashes' = []
    last_state_fetch: int = 0
    last_block_fetch: int = 0
    lock = asyncio.Lock()

    async def get_state(cls = None, fetch_func = None, interval = classmethod):
        '''Returns a State that is `fresher` than given interval.'''
        pass

    get_state = None(get_state)

    async def get_hash(cls = None, fetch_func = None, client = classmethod, interval = (True,), log_errors = {
        'fetch_func': Coroutine,
        'client': any,
        'interval': int,
        'return': 'State' }):
        '''Returns a block that is `fresher` than given interval.'''
        pass

    get_hash = None(get_hash)