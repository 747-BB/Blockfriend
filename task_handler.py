import asyncio
import time
from typing import TYPE_CHECKING, List, Union
from sentry_sdk import capture_exception
from helpers import AsyncSession
if TYPE_CHECKING:
    from static.instruction_laboratory import InstructionLaboratory
    from static.templates import MintConfig, ModuleConfig

class MintException(Exception):
    pass


class Task:

    def __init__(self, module, config = None, mint_config = None, task_id = None, rpc_client = {
        'module': 'InstructionLaboratory',
        'config': 'ModuleConfig',
        'mint_config': 'MintConfig',
        'task_id': int }):
        self.Module = module
        self.config = config
        self.mint_config = mint_config
        self.task_id = task_id
        self.rpc_client = rpc_client



class TaskHandler:

    def __init__(self, **kw):
        self.cm = kw.get('cm')
        self.loop = asyncio.get_event_loop()
        self.session = AsyncSession()


    def run(self = None, tasks = None):
        '''Runs given tasks in the event loop.'''
        self.loop.run_until_complete(self.run_tasks(tasks))


    def get_jobs(self = None, tasks = None):
        '''Returns a list of Jobs from given Tasks.'''
        jobs = []
        return jobs


    async def run_tasks(self = None, tasks = None):
        '''Converts given tasks to jobs, and executes them.'''
        mint_jobs = self.get_jobs(tasks)
        evaluation_jobs = []


    async def evaluate_result(self = None, result = None):
        '''Evaluates the given TaskResult.'''
        if isinstance(result, Exception):
            print('[ERROR]', str(result))
            capture_exception(result)
        elif isinstance(result, list):
            txids = result
        elif isinstance(result, str):
            txid = result


    async def log_result(self, key = None, result = None, status = None, timestamp = {
        'key': str,
        'result': Union[(str, Exception)],
        'status': str,
        'timestamp': int }):
        '''POST tx to server logs.'''
        url = 'https://blockfriend.net/txs/log'
        payload = {
            'key': key,
            'result': result,
            'status': status,
            'timestamp': timestamp }
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded' }
        if not self.session.initialized:
            await self.session.init()
        await self.session.post(url, payload, headers, **('json', 'headers'))