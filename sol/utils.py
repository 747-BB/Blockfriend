from constants import LAUNCHPAD_PROGRAM, MONKELABS_PROGRAM, SOLANA_CMV2_PROGRAM, METADATA_PROGRAM_ID, TOKEN_PROGRAM_ID, SYSTEM_PROGRAM_ID, SYSVAR_INSTRUCTIONS, SLOTHASHES_PROGRAM_ID, SYSVAR_RECENT_BLOCKHASHES_PUBKEY, SYSVAR_CLOCK_PUBKEY, SYSVAR_RENT_PUBKEY, ASSOCIATED_TOKEN_ACCOUNT_PROGRAM_ID, CIVIC
from imports import *
from solana.system_program import create_account, CreateAccountParams
from spl.token.constants import MINT_LEN, TOKEN_PROGRAM_ID
from spl.token.instructions import initialize_mint, InitializeMintParams, create_associated_token_account, get_associated_token_address, mint_to, MintToParams, approve, ApproveParams
from solana.transaction import Transaction, TransactionInstruction, AccountMeta
from solana.publickey import PublicKey
from sol.state_worker import StateWorker
import numpy as np

async def get_blockhashes(client):
    await client.get_epoch_info()
    #block = <NODE:27>Unsupported Node type: 27

    block_no = block['result']['absoluteSlot']
    await client.get_block(block_no)
    #data = <NODE:27>Unsupported Node type: 27

    hashes = []
    return list(set(hashes))


async def get_proof(kp, client):
    tx = Transaction()
    ixs = [
        AccountMeta(PublicKey(kp.public_key), True, True, **('pubkey', 'is_writable', 'is_signer')),
        AccountMeta(PublicKey(kp.public_key), True, False, **('pubkey', 'is_writable', 'is_signer'))]
    ti = TransactionInstruction(b'\x02\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00', ixs, PublicKey('11111111111111111111111111111111'), **('data', 'keys', 'program_id'))
    tx.add(ti)
    block = client.get_recent_blockhash('confirmed')
    blockhash = Blockhash(block['result']['value']['blockhash'])
    tx.recent_blockhash = blockhash
    tx.fee_payer = PublicKey(kp.public_key)
    tx.sign(kp)
    return base64.b64encode(tx.serialize()).decode()


def get_auth_key(pda_buf):
    return PublicKey.find_program_address([
        bytes(np.array([
            pda_buf,
            (pda_buf & 65280) >> 8], np.uint8, **('dtype',))),
        b'auth',
        bytes(MONKELABS_PROGRAM)], MONKELABS_PROGRAM)


def get_uniq_pda(wallet, pda_buf):
    return PublicKey.find_program_address([
        bytes(np.array([
            pda_buf,
            (pda_buf & 65280) >> 8], np.uint8, **('dtype',))),
        bytes(wallet.public_key),
        bytes(MONKELABS_PROGRAM)], MONKELABS_PROGRAM)


def get_time_pda(wallet, pda_buf):
    return PublicKey.find_program_address([
        b'ltime',
        bytes(wallet.public_key),
        bytes(MONKELABS_PROGRAM)], MONKELABS_PROGRAM)


def get_network_token(wallet, gatekeeper_network):
    return PublicKey.find_program_address([
        bytes(wallet),
        b'gateway',
        bytes.fromhex('0000000000000000'),
        bytes(PublicKey(gatekeeper_network))], CIVIC)


def get_network_expire(gatekeeper_network):
    return PublicKey.find_program_address([
        bytes(gatekeeper_network),
        b'expire'], CIVIC)


def get_metadata_account(mint_key):
    return PublicKey.find_program_address([
        b'metadata',
        bytes(METADATA_PROGRAM_ID),
        bytes(PublicKey(mint_key))], METADATA_PROGRAM_ID)[0]


def get_wallet_limit(cmid, wallet):
    return PublicKey.find_program_address([
        b'wallet_limit',
        bytes(cmid),
        bytes(wallet)], LAUNCHPAD_PROGRAM)


def get_edition(mint_key):
    return PublicKey.find_program_address([
        b'metadata',
        bytes(METADATA_PROGRAM_ID),
        bytes(PublicKey(mint_key)),
        b'edition'], METADATA_PROGRAM_ID)[0]


def get_creator(cmid):
    return PublicKey.find_program_address([
        b'candy_machine',
        bytes(PublicKey(cmid))], SOLANA_CMV2_PROGRAM)


def get_launch_stages_info(cmid):
    return PublicKey.find_program_address([
        b'candy_machine',
        b'launch_stages',
        bytes(PublicKey(cmid))], LAUNCHPAD_PROGRAM)


def get_ata_for_mint(mint_key, buyer):
    return PublicKey.find_program_address([
        bytes(buyer),
        bytes(TOKEN_PROGRAM_ID),
        bytes(mint_key)], ASSOCIATED_TOKEN_ACCOUNT_PROGRAM_ID)


def get_token_wallet(wallet, mint_key):
    return PublicKey.find_program_address([
        bytes(wallet),
        bytes(TOKEN_PROGRAM_ID),
        bytes(PublicKey(mint_key))], ASSOCIATED_TOKEN_ACCOUNT_PROGRAM_ID)


def get_candy_machine_pda_nonce(config_pub_key_str):
    uuid = config_pub_key_str[:6]
    result = PublicKey.find_program_address([
        b'candy_machine',
        bytes(PublicKey(config_pub_key_str)),
        uuid.encode()], PublicKey(SOLANA_CMV2_PROGRAM))
    return (result[0], result[1])


async def get_minimum_balance_rent_exemption(client, account_size):
    await client.get_minimum_balance_for_rent_exemption(account_size)
    #resp = <NODE:27>Unsupported Node type: 27

    exemption_lamports = int(resp['result'])
    return exemption_lamports


def create_associated_token_account_instruction(associated_token_account, payer, wallet_address, token_mint_address):
    keys = [
        AccountMeta(payer, True, True, **('pubkey', 'is_signer', 'is_writable')),
        AccountMeta(associated_token_account, False, True, **('pubkey', 'is_signer', 'is_writable')),
        AccountMeta(wallet_address, False, False, **('pubkey', 'is_signer', 'is_writable')),
        AccountMeta(token_mint_address, False, False, **('pubkey', 'is_signer', 'is_writable')),
        AccountMeta(SYSTEM_PROGRAM_ID, False, False, **('pubkey', 'is_signer', 'is_writable')),
        AccountMeta(TOKEN_PROGRAM_ID, False, False, **('pubkey', 'is_signer', 'is_writable')),
        AccountMeta(SYSVAR_RENT_PUBKEY, False, False, **('pubkey', 'is_signer', 'is_writable'))]
    return TransactionInstruction(keys, ASSOCIATED_TOKEN_ACCOUNT_PROGRAM_ID, **('keys', 'program_id'))


def create_metadata_instruction(metadata_account, mint, mint_authority, payer, update_authority, txn_data):
    keys = [
        AccountMeta(metadata_account, False, True, **('pubkey', 'is_signer', 'is_writable')),
        AccountMeta(mint, False, False, **('pubkey', 'is_signer', 'is_writable')),
        AccountMeta(mint_authority, True, False, **('pubkey', 'is_signer', 'is_writable')),
        AccountMeta(payer, True, False, **('pubkey', 'is_signer', 'is_writable')),
        AccountMeta(update_authority, False, False, **('pubkey', 'is_signer', 'is_writable')),
        AccountMeta(SYSTEM_PROGRAM_ID, False, False, **('pubkey', 'is_signer', 'is_writable')),
        AccountMeta(SYSVAR_RENT_PUBKEY, False, False, **('pubkey', 'is_signer', 'is_writable'))]
    return TransactionInstruction(keys, METADATA_PROGRAM_ID, txn_data, **('keys', 'program_id', 'data'))


async def get_approval_instruction(self, user_account, purchase_token, amount):
    transfer_authority_keypair = Keypair()
    assoc_token_account_public_key = get_associated_token_address(user_account.public_key, purchase_token)
    approval_instruction = approve(ApproveParams(TOKEN_PROGRAM_ID, assoc_token_account_public_key, transfer_authority_keypair.public_key, user_account.public_key, amount, **('program_id', 'source', 'delegate', 'owner', 'amount')))
    return (approval_instruction, transfer_authority_keypair, assoc_token_account_public_key)


async def get_burn_instruction(self, user_account, purchase_token, amount):
    burn_authority_keypair = Keypair()
    assoc_token_account_public_key = get_associated_token_address(user_account.public_key, purchase_token)
    approval_instruction = approve(ApproveParams(TOKEN_PROGRAM_ID, assoc_token_account_public_key, burn_authority_keypair.public_key, user_account.public_key, amount, **('program_id', 'source', 'delegate', 'owner', 'amount')))
    return (approval_instruction, burn_authority_keypair)