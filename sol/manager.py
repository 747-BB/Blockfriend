from imports import *
from solana.rpc.core import RPCException
from solana.system_program import TransferParams, transfer
from spl.token._layouts import MINT_LAYOUT, ACCOUNT_LAYOUT
from itertools import islice
_COEFFICIENT = 0.99

def split_array(it, size):
    it = iter(it)
    return None((lambda : tuple(islice(it, size))), ())


class Distributor:

    def __init__(self, **kw):
        self.parent = kw.get('parent')
        self.children_web = kw.get('children')
        self.client = kw.get('client')


    def get_empty_accounts(self = None, wallet = None):
        print(f'''Fetching tokens for {wallet.public_key}''')
        response = self.client.get_token_accounts_by_owner(wallet.public_key, TokenAccountOpts(TOKEN_PROGRAM_ID, **('program_id',)))
        return (lambda .0 = None: [ PublicKey(token.get('pubkey')) for token in .0 if int(self.client.get_token_account_balance(token.get('pubkey'))['result'].get('value').get('amount')) == 0 ])(response['result'].get('value'))


    def close_accounts(self = None, wallet = None, accounts = None):
        i = 0
        if len(accounts) > 0:
            transaction = Transaction()
            for account in accounts:
                params = spl_token.CloseAccountParams(TOKEN_PROGRAM_ID, accounts.pop(), wallet.public_key, wallet.public_key, **('program_id', 'account', 'dest', 'owner'))
                instruction = spl_token.close_account(params)
                transaction = transaction.add(instruction)
                i += 1
                print(f'''Closing {i} accounts on {wallet.public_key}''')
                i = 0
                [ f'''Closing {i} accounts on {wallet.public_key}''' ]
            self.client.send_transaction(transaction, wallet)


    def get_tokens(self = None, wallet = None):
        print(f'''Fetching tokens from {wallet.public_key}''')
    # WARNING: Decompyle incomplete


    def create_associated_token_account_instruction(self, associated_token_account = None, payer = None, wallet_address = None, token_mint_address = {
        'associated_token_account': PublicKey,
        'payer': PublicKey,
        'wallet_address': PublicKey,
        'token_mint_address': PublicKey }):
        keys = [
            AccountMeta(payer, True, True, **('pubkey', 'is_signer', 'is_writable')),
            AccountMeta(associated_token_account, False, True, **('pubkey', 'is_signer', 'is_writable')),
            AccountMeta(wallet_address, False, False, **('pubkey', 'is_signer', 'is_writable')),
            AccountMeta(token_mint_address, False, False, **('pubkey', 'is_signer', 'is_writable')),
            AccountMeta(SYSTEM_PROGRAM_ID, False, False, **('pubkey', 'is_signer', 'is_writable')),
            AccountMeta(TOKEN_PROGRAM_ID, False, False, **('pubkey', 'is_signer', 'is_writable')),
            AccountMeta(SYSVAR_RENT_PUBKEY, False, False, **('pubkey', 'is_signer', 'is_writable'))]
        return TransactionInstruction(keys, ASSOCIATED_TOKEN_ACCOUNT_PROGRAM_ID, **('keys', 'program_id'))


    def get_transfer_token_instruction(self = None, sender = None, receiver = None, token_account = {
        'sender': Keypair,
        'receiver': Keypair,
        'token_account': PublicKey }):
        transaction = Transaction()
        token_pda_address = spl_token.get_associated_token_address(sender.public_key, token_account)
        associated_token_account = spl_token.get_associated_token_address(receiver.public_key, token_account)
        associated_token_account_info = self.client.get_account_info(associated_token_account)
        account_info = associated_token_account_info['result']['value']
        if account_info is not None:
            account_state = ACCOUNT_LAYOUT.parse(base64.b64decode(account_info['data'][0])).state
        else:
            account_state = 0
        if account_state == 0:
            associated_token_account_ix = self.create_associated_token_account_instruction(associated_token_account, sender.public_key, receiver.public_key, token_account, **('associated_token_account', 'payer', 'wallet_address', 'token_mint_address'))
            transaction = transaction.add(associated_token_account_ix)
        params = spl_token.TransferParams(TOKEN_PROGRAM_ID, token_pda_address, associated_token_account, sender.public_key, [], 1, **('program_id', 'source', 'dest', 'owner', 'signers', 'amount'))
        transaction = transaction.add(spl_token.transfer(params))
        return transaction


    def transfer_token(self = None, sender = None, receiver = None, token_account = {
        'sender': Keypair,
        'receiver': Keypair,
        'token_account': PublicKey }):
        pass


    def transfer_solana(self = None, sender = None, receivers = None, amount = {
        'sender': Keypair,
        'receivers': list,
        'amount': float }):
        pass