import asyncio
import copy
import random
from concurrent.futures import ThreadPoolExecutor
from functools import partial
from typing import Tuple
from sentry_sdk import capture_exception
from helpers import Session
from helpers.civic_worker import CivicWorker
from menu_handler import clear_screen
from modules import _MODULES
from static.templates import MintConfig
from task_handler import Task, TaskHandler
from imports import *
from manager import Distributor
from helpers.engine import Engine
CHAIN = 'SOL'

class SolWalletUtils:

    def __init__(self, **kw):
        (self.wm, self.cm, self.rm, self.am, self.pm) = (kw.get('wm'), kw.get('cm'), kw.get('rm'), kw.get('am'), kw.get('pm'))
        self.set_rpc_urls()


    def set_rpc_urls(self):
        self.rpc_clients = []
        self.rpc_list = (lambda .0: [ rpc_url.strip() for rpc_url in .0 ])(self.cm.get(CHAIN, 'rpc').split(','))
        self.rpc_url = self.rpc_list[0]
        self.client = Client(self.rpc_url)


    def find_wallet(self = None, public_key = None):
        '''Finds a desired keypair'''
        pass


    def setup_release(self = None, user_input = None):
        target = user_input.get('target').strip()
        release_type = user_input.get('release_type')


    def start_release(self = None, user_input = None):
        release_name = None
        release = self.rm.get(CHAIN, release_name)
        if not release:
            print(f'''SOL release `{release_name}` not found.''')
            return None
        program_id = None.get('Program')
        module = _MODULES[CHAIN][program_id]
        config_kwargs = release.get('Config')
        config_kwargs['rpc'] = self.rpc_url
        config_kwargs['proxy_list'] = self.pm.proxy_list
        config_kwargs['rpc_list'] = self.rpc_list
    # WARNING: Decompyle incomplete


    async def start_congest(self, release, module, options, config):
        selected_wallets = []
        wallet_pkey = base58.b58encode(wallet.secret_key).decode('utf8')
        selected_wallets.append(wallet_pkey)
        if len(selected_wallets) == 0:
            print('[ERROR] No wallets were selected for this release, please recreate it and try again.')
            return None
        kws = None.copy()
        kws['wallet'] = selected_wallets[0]
    # WARNING: Decompyle incomplete


    def start_normal(self, task_handler, release, module, options, config, release_name):
        tasks = []
        task_id = 1
        tasks_per_wallet = int(options.get('tasks_per_wallet', 1))
        rpc_clients_len = len(self.rpc_clients)
        kws = options.copy()
        kws['wallet'] = wallet


    def transact(self = None, user_input = None):
        action = None
        master = (lambda .0 = None: [ Keypair(w['PrivateKey'][:32]) for w in .0 if str(Keypair(w['PrivateKey'][:32]).public_key) == str(user_input.get('master_wallet')) ])(self.wm.wallets[CHAIN])[0]
        children = []
        distributor = Distributor(master, children, self.client, **('parent', 'children', 'client'))
        if action == 'Transfer SOL to Master':
            distributor.transfer_solana(child, [
                distributor.parent], amount, **('sender', 'receivers', 'amount'))
        elif action == 'Transfer SOL from Master':
            transfer_amount = user_input.get('transfer_amount', 0)
            amount = float(transfer_amount)
            distributor.transfer_solana(distributor.parent, distributor.children_web, amount, **('sender', 'receivers', 'amount'))
        elif action == 'Transfer NFTs to Master':
            print('Transferring NFTs to Master')
        elif action == 'Transfer NFTs from Master':
            destination = (lambda .0 = None: [ Keypair(w['PrivateKey'][:32]) for w in .0 if str(Keypair(w['PrivateKey'][:32]).public_key) == user_input.get('addresses') ])(self.wm.wallets[CHAIN])[0]
            tokens = distributor.get_tokens(master)


    def create_wallets_sol(self = None, user_input = None):
        quantity = int(user_input.get('quantity', 0))
        new_addresses = [
            [
                'Wallet Name',
                'Wallet Address']]
        self.wm.save()
        print(tabulate(new_addresses, 'firstrow', 'fancy_grid', **('headers', 'tablefmt')))


    def import_wallets_sol(self = None, user_input = None):
        new_addresses = [
            [
                'Wallet Name',
                'Wallet Address']]


    def show_wallets_sol(self = None, user_input = None):
        wallets = [
            [
                'Nickname',
                'Wallet Address']]
        print(tabulate(wallets, 'firstrow', 'fancy_grid', **('headers', 'tablefmt')))


    #def refresh_table(self = None, result = None, table = None):