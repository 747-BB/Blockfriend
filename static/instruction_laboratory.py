import time
import json
import asyncio
import anchorpy
from abc import ABC, abstractmethod
from dataclasses import dataclass
import anchorpy
from sol.imports import *
from sol.state_worker import StateWorker
from templates import ModuleConfig, State
import logging
task_logger = logging.getLogger('task_logger')
task_logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
formatter = logging.Formatter('[%(asctime)s]%(message)s', '%Y/%m/%d %H:%M:%S', **('datefmt',))
ch.setFormatter(formatter)
task_logger.addHandler(ch)

class InstructionLaboratory:
    idl = anchorpy.Idl
    program = anchorpy.Program
    provider = anchorpy.Provider
    client = AsyncClient

    async def create(self = None, config = None):
        '''Creates an instance.'''
        pass

    create = None(create)

    async def fetch(self = None, target = None):
        """Fetches and parses config based on IDL account type (will be set as attribute 'cm') and returns standardized 'State' dataclass."""
        pass

    fetch = None(fetch)

    async def construct(self = None, wallet = None, **kw):
        '''Constructs and returns a ready-to-broadcast mint transaction.'''
        pass

    construct = None(construct)

    async def entrypoint(self, config, mint_config, task_id, rpc_client):
        '''Task start entry point. Handle all logic from construction to broadcast.'''
        await self.log_task_info(task_id, f'''Using rpc client: {rpc_client._provider.endpoint_uri}''')
        await self.wait_before_broadcast(mint_config, task_id)
        txids = None


    async def broadcast(self, transaction = None, signers = None, task_id = None, rpc_client = {
        'transaction': Transaction,
        'signers': list,
        'task_id': int }):
        '''Signs then broadcasts transaction onto the Solana Network and returns the RPC response (TXID)'''
        pass


    async def get_recent_blockhash(self):
        POLLING_INTERVAL = 20
        await StateWorker.get_hash(get_blockhashes, self.client, POLLING_INTERVAL, **('fetch_func', 'client', 'interval'))
        #block = <NODE:27>Unsupported Node type: 27

        return Blockhash(block)


    async def wait_until_live(self = None, task_id = None, delta = None, custom_timestamp = (0, 0)):
        '''Waits until minting is live, and returns latest State.'''
        POLLING_INTERVAL = 10
        await StateWorker.get_state(self.fetch, POLLING_INTERVAL, **('fetch_func', 'interval'))
        #state = <NODE:27>Unsupported Node type: 27

        go_live_date = custom_timestamp if custom_timestamp != 0 else state.go_live_date
        if not isinstance(go_live_date, int):
            await self.log_task_info(task_id, f'''Invalid or missing go_live_date, retrying in {POLLING_INTERVAL} seconds...''')
            await asyncio.sleep(POLLING_INTERVAL)
        if go_live_date - delta > time.time():
            time_left = go_live_date - time.time() - delta
            await self.log_task_info(task_id, f'''Minting starts in {int(time_left)} seconds, {state.items_redeemed}/{state.items_available} items sold.''')
            if time_left < POLLING_INTERVAL:
                await asyncio.sleep(time_left)
                return state
        return state
        await asyncio.sleep(POLLING_INTERVAL)


    async def wait_before_broadcast(self, mint_config, task_id):
        POLLING_INTERVAL = 10
        mode = mint_config.mode
        delta = int(mint_config.delta)
        custom_timestamp = int(mint_config.custom_timestamp)
        await self.log_task_info(task_id, 'Waiting for mint to start...')
        await self.wait_until_live(task_id, delta, custom_timestamp, **('delta', 'custom_timestamp'))
        #state = <NODE:27>Unsupported Node type: 27

        if mode.lower() == 'target':
            await self.log_task_info(task_id, f'''{round(state.items_redeemed / state.items_available, 2)}% sold. {state.items_redeemed}/{state.items_available} items sold.''')
            if state.items_redeemed / state.items_available >= float(mint_config.target_percentage):
                return None
            await None.sleep(1)
            await StateWorker.get_state(self.fetch, POLLING_INTERVAL, **('fetch_func', 'interval'))
            #state = <NODE:27>Unsupported Node type: 27


    async def spam_transaction(self, mint_config, task_id, rpc_client):
        '''Runs the SPAM mode with given config.'''
        tasks = []
        SPAN = int(mint_config.span)
        start_time = int(time.time())
        if int(time.time()) - start_time < SPAN:
            await self.construct(mint_config.wallet, **('wallet',))
            #(transaction, signers) = <NODE:27>Unsupported Node type: 27

            task = asyncio.create_task(self.broadcast(transaction, signers, task_id, rpc_client))
            tasks.append(task)


    async def spam_transaction2(self, mint_config, task_id, rpc_client):
        '''Runs the SPAM mode with given config.'''
        tasks = []
        SPAN = int(mint_config.span)
        await self.construct(mint_config.wallet, **('wallet',))
        #(transaction, signers) = <NODE:27>Unsupported Node type: 27

        start_time = int(time.time())
        if int(time.time()) - start_time < SPAN:
            task = asyncio.create_task(self.broadcast(transaction, signers, task_id, rpc_client))
            tasks.append(task)
            await asyncio.sleep(0)


    async def log_task_info(self, task_id, message):
        task_logger.info(f'''[Task {task_id:04.0f}] {message}''')
