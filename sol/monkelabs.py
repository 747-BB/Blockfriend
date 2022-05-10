from imports import *
from bs4 import BeautifulSoup
import requests
import json
import os
import re
import numpy as np

def get_monkelabs_script_url(mint_url = (None,)):
    response = requests.get(mint_url)
    if response.status_code != 200:
        print('Failed to fetch html, received error:', response, status_code)
        return None
    monke_html = None.text
    soup = BeautifulSoup(monke_html, 'html.parser')
    script_elements = soup.find_all('script')
    script_file_name = os.path.basename(script_src)
    if re.match('2\\.\\w+\\.chunk\\.js', script_file_name):
        return f'''{mint_url}{script_src}'''


def parse_monkelabs_script(script_url = (None,)):
    response = requests.get(script_url)
    if response.status_code != 200:
        print('Failed to fetch script, received error:', response, status_code)
        return None
    script_source = None.text
    search_result = re.search('\\((\\{NODE_ENV:"production",.*?\\})\\)', script_source)
    if not search_result:
        print('Unable to find mint config in script source.')
        return None
    return None.group(1)


def js_object_to_json(object_string):
    object_string = re.sub('(\\{|,)(\\w+):', '\\1"\\2":', object_string)
    object_string = re.sub('(?<=\\{|,)("\\w+":)([^"].*?)(?=,|\\})', '\\1"\\2"', object_string)


def get_monkelabs_config(mint_url = (None,)):
    if mint_url[-1] == '/':
        mint_url = mint_url[:-1]
    script_url = get_monkelabs_script_url(mint_url, **('mint_url',))
    if not script_url:
        return { }
    config_string = None(script_url, **('script_url',))
    if not config_string:
        return { }
    config_json = None(config_string)
    if not config_json:
        return { }
    mint_config = {
        'pda_buf': None(config_json.get('REACT_APP_PDA_BUFFER')),
        'price': config_json.get('REACT_APP_PRICE'),
        'index_cap': config_json.get('REACT_APP_INDEX_CAP'),
        'index_key': config_json.get('REACT_APP_INDEX_KEY'),
        'wl_key': config_json.get('REACT_APP_WHITELIST_KEY'),
        'primary_wallet': config_json.get('REACT_APP_PRIMARY_WALLET'),
        'config_key': config_json.get('REACT_APP_CONFIG_KEY'),
        'timeout': config_json.get('REACT_APP_CONFIG_TIMEOUT'),
        'go_live_date': config_json.get('REACT_APP_CANDY_START_DATE') }
    return mint_config


class Monkelabs(InstructionLaboratory):

    def __init__(self):
        self.client = AsyncClient
        self.provider = anchorpy.Provider
        self.cm = None
        (self.free_mint, self.active, self.soldout) = ((True, False), (True, False), (True, False))


    async def create(cls, config, **kw):
        self = cls()
        self.rpc_list = config.rpc_list
        self.client = AsyncClient(config.rpc)
        self.kp = Keypair()
        self.target = config.target
        await self.fetch()
        #self.cm = <NODE:27>Unsupported Node type: 27

        return self

    create = classmethod(create)

    async def get_minted_quantity(self = None, address = None):
        await client.get_account_info(address)
        #data = <NODE:27>Unsupported Node type: 27

        account_data = base64.b64decode(data.get('result').get('value').get('data')[0])
        return (account_data[1] << 8) + account_data[0]


    async def fetch(self = None):
        data = get_monkelabs_config(self.target)
        if not data:
            print('Unable to scrape config from mint url.')
            return None
        await None.handle()
        await self.get_minted_quantity(PublicKey(data.get('config_key')))
        return MonkelabsState(data.get('pda_buf'), data.get('price'), data.get('index_cap'), data.get('index_key'), data.get('wl_key'), data.get('primary_wallet'), data.get('config_key'), data.get('timeout'), int(data.get('go_live_date')), int(data.get('index_cap')), <NODE:27>Unsupported Node type: 27
, **('pda_buf', 'price', 'index_cap', 'index_key', 'wl_key', 'primary_wallet', 'config_key', 'timeout', 'go_live_date', 'items_available', 'items_redeemed'))


    async def handle(self):
        pass


    async def get_user_account_mint_prep_instructions(self, user_account):
        mint_account = Keypair()
        instruction_list = []
        await get_minimum_balance_rent_exemption(self.client, MINT_LEN)
        #min_lamports = <NODE:27>Unsupported Node type: 27

        create_account_instruction = create_account(CreateAccountParams(user_account.public_key, mint_account.public_key, min_lamports, MINT_LEN, TOKEN_PROGRAM_ID, **('from_pubkey', 'new_account_pubkey', 'lamports', 'space', 'program_id')))
        instruction_list.append(create_account_instruction)
        initialize_mint_instruction = initialize_mint(InitializeMintParams(0, TOKEN_PROGRAM_ID, mint_account.public_key, user_account.public_key, **('decimals', 'program_id', 'mint', 'mint_authority')))
        instruction_list.append(initialize_mint_instruction)
        associated_token_account = get_associated_token_address(user_account.public_key, mint_account.public_key)
        create_assoc_instruction = create_associated_token_account_instruction(associated_token_account, user_account.public_key, user_account.public_key, mint_account.public_key, **('associated_token_account', 'payer', 'wallet_address', 'token_mint_address'))
        instruction_list.append(create_assoc_instruction)
        mint_to_instruction = mint_to(MintToParams(TOKEN_PROGRAM_ID, mint_account.public_key, associated_token_account, user_account.public_key, 1, **('program_id', 'mint', 'dest', 'mint_authority', 'amount')), **('params',))
        instruction_list.append(mint_to_instruction)
        return (mint_account, instruction_list, associated_token_account, [
            user_account,
            mint_account])


    async def create_mint_instruction(self, **kw):
        mint_account = kw.get('mint_account', Keypair())
        token_account = kw.get('token_account')
        metadata_account = get_metadata_account(mint_account.public_key)
        master_edition_account = get_edition(mint_account.public_key)
        cm = kw.get('cm')
        kp = kw.get('kp')
        remaining_accounts = kw.get('remaining_accounts', [])
        auth_key = get_auth_key(cm.pda_buf)[0]
        uniq_pda = get_uniq_pda(kp, cm.pda_buf)[0]
        time_pda = get_time_pda(kp, cm.pda_buf)[0]
        ixs = [
            AccountMeta(kp.public_key, True, True, **('pubkey', 'is_writable', 'is_signer')),
            AccountMeta(time_pda, True, False, **('pubkey', 'is_writable', 'is_signer')),
            AccountMeta(SYSTEM_PROGRAM_ID, False, False, **('pubkey', 'is_writable', 'is_signer'))]
        ti = TransactionInstruction(bytes(np.array([
            14], np.uint8, **('dtype',))), ixs, MONKELABS_PROGRAM, **('data', 'keys', 'program_id'))
        ixs = [
            AccountMeta(PublicKey(cm.index_key), True, False, **('pubkey', 'is_writable', 'is_signer')),
            AccountMeta(PublicKey(cm.primary_wallet), True, False, **('pubkey', 'is_writable', 'is_signer')),
            AccountMeta(PublicKey('mnKzuL9RMtR6GeSHBfDpnQaefcMsiw7waoTSduKNiXM'), True, False, **('pubkey', 'is_writable', 'is_signer')),
            AccountMeta(kp.public_key, True, True, **('pubkey', 'is_writable', 'is_signer')),
            AccountMeta(PublicKey(cm.wl_key), True, False, **('pubkey', 'is_writable', 'is_signer')),
            AccountMeta(token_account, True, False, **('pubkey', 'is_writable', 'is_signer')),
            AccountMeta(SYSTEM_PROGRAM_ID, False, False, **('pubkey', 'is_writable', 'is_signer')),
            AccountMeta(metadata_account, True, False, **('pubkey', 'is_writable', 'is_signer')),
            AccountMeta(mint_account.public_key, True, False, **('pubkey', 'is_writable', 'is_signer')),
            AccountMeta(METADATA_PROGRAM_ID, False, False, **('pubkey', 'is_writable', 'is_signer')),
            AccountMeta(SYSVAR_RENT_PUBKEY, False, False, **('pubkey', 'is_writable', 'is_signer')),
            AccountMeta(auth_key, True, False, **('pubkey', 'is_writable', 'is_signer')),
            AccountMeta(TOKEN_PROGRAM_ID, False, False, **('pubkey', 'is_writable', 'is_signer')),
            AccountMeta(uniq_pda, True, False, **('pubkey', 'is_writable', 'is_signer')),
            AccountMeta(time_pda, True, False, **('pubkey', 'is_writable', 'is_signer')),
            AccountMeta(master_edition_account, True, False, **('pubkey', 'is_writable', 'is_signer')),
            AccountMeta(PublicKey(cm.config_key), True, False, **('pubkey', 'is_writable', 'is_signer')),
            AccountMeta(SYSVAR_INSTRUCTIONS, False, False, **('pubkey', 'is_writable', 'is_signer')),
            AccountMeta(PublicKey('7FHzVCP9eX6zmZjw3qwvmdDMhSvCkLxipQatAqhtbVBf'), False, False, **('pubkey', 'is_signer', 'is_writable'))]
        mi = TransactionInstruction(bytes(np.array([
            9], np.uint8, **('dtype',))), ixs, MONKELABS_PROGRAM, **('data', 'keys', 'program_id'))
        return [
            ti,
            mi]


    async def construct(self = None, wallet = None, **kw):
        transaction = Transaction()
        await self.get_user_account_mint_prep_instructions(wallet)
        #(mint_account, account_create_instructions, token_account, signers) = <NODE:27>Unsupported Node type: 27

        instructions = account_create_instructions