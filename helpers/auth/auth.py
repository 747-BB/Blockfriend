import subprocess
import requests
import hashlib
import tempfile
import psutil
import base64
import json
import time
import uuid
import sys
import os
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Hash import SHA256
from Crypto.Signature import PKCS1_v1_5
from Crypto.PublicKey import RSA
from itertools import cycle
BANNED_PROCESSES = [
    'codecracker',
    'x96dbg',
    'de4dot',
    'pc-ret',
    'ILSpy',
    'x32dbg',
    'x64dbg',
    'x32_dbg',
    'x64_dbg',
    'titanHide',
    'scyllaHide',
    'ilspy',
    'simpleassemblyexplorer',
    'MegaDumper',
    'megadumper',
    'X64NetDumper',
    'x64netdumper',
    'PETools',
    'petools',
    'james',
    'ollydbg',
    'x32dbg',
    'x64dbg',
    'ida -',
    'charles',
    'dnspy',
    'httpanalyzer',
    'httpdebug',
    'fiddler',
    'wireshark',
    'mitmproxy',
    'mitmweb',
    'process hacker',
    'process hacker 2',
    'ghidra',
    'pc-ret',
    'de4dotmodded',
    'exeinfope',
    'codecracker',
    'x32dbg',
    'x64dbg',
    'ollydbg',
    'ida -',
    'charles',
    'dnspy',
    'simpleassembly',
    'peek',
    'httpanalyzer',
    'httpdebug',
    'fiddler',
    'wireshark',
    'windbg',
    'dumpcap',
    'http analyzer',
    'burp',
    'injector',
    'cheat engine',
    'cheatengine',
    'radare',
    'hopper disassembler',
    'lldb',
    'smartsniff',
    'vsjitdebugger',
    'frida',
    'httptoolkit',
    'http toolkit',
    'tcpdump',
    'paessler',
    'omnipeek',
    'windump',
    'tshark',
    'proxifier']
PUBLIC_KEY = '-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAnunwb3U3oELXCuc503rp\nXhbcyf5DUMN02G27olE5bb9/v9RZJd/E12hQ/+td3ODn0aWkNAqhMSAnHMJ5ZTA9\nkeyEHV7IzIqY7N/cgn+JwP0Y3hdfo8c3TsIScO2bjIKWv2migbQTq/KEfnO+Lkxc\n5mMUT9gxrs9m4C2WHpsSYRuwnXtocPQJ74DGGE6SQ3mJpVv8XB0OW2kKhGqQ7ED0\n5w8H5jBkPskAKDbOkEaombfdNfvuJDhjbPyzkm3fqmgRma819hYUUadH1sN49bpa\ncZK8sQlNlFnCR28sZJsDxAuewp0oaUobIhWcfD5gwyw7HkHrqbL7jkcdRmUAZhdw\nKwIDAQAB\n-----END PUBLIC KEY-----'
PUBLIC_KEY = RSA.importKey(PUBLIC_KEY)

def get_hwid():
    return get_string_md5(str(uuid.getnode()))


def xor_encrypt(data, key):
    return ''.join((lambda .0: pass)(zip(data, cycle(key))))


def encrypt_cbc(plaintext):
    iv = os.urandom(16)
    plaintext_padded = pad(plaintext.encode('utf8'), 16)
    aes = AES.new(b'\x88U\x86W\x85vD\x1c9\xb3\x93\xde\xf0\x9f\xe5\xe0', AES.MODE_CBC, iv)
    ciphertext = iv + aes.encrypt(plaintext_padded)
    return ciphertext.hex()


def decrypt_payload(ciphertext, xor_key):
    ciphertext = bytes.fromhex(ciphertext)
    aes = AES.new(b'MP\x01\xc53\xc2\x1e\x0e!+\xfc4\xa9,3\xff', AES.MODE_CBC, ciphertext[:16])
    plaintext = unpad(aes.decrypt(ciphertext[16:]), 16)
    return xor_encrypt(plaintext.decode('utf8'), xor_key)


def get_string_md5(data):
    return hashlib.md5(data.encode('utf8')).hexdigest()


def check_nerd_level():
    if json.dumps.__module__ != 'json' or json.loads.__module__ != 'json':
        return 1
    if None.md5.__module__ != '_hashlib' or hashlib.sha256.__module__ != '_hashlib':
        return 2
    if None.post.__module__ != 'requests.api':
        return 3
    if None.getnode.__module__ != 'uuid':
        return 4


def verify_message(message, signature, public_key):
    signature = bytes.fromhex(signature)
    digest = SHA256.new()
    digest.update(message.encode('utf-8'))
    verifier = PKCS1_v1_5.new(public_key)
    verified = verifier.verify(digest, signature)
    return verified


class AuthManager:

    def __init__(self, **kw):
        self.cm = kw.get('cm')
        license_key = self.cm.get('Authentication', 'licensekey')
        if not license_key:
            license_key = input('No license key is available, enter your license: ').strip()
            self.cm.set('Authentication', 'licensekey', license_key)
        self.is_authenticated = False
        self.license_key = license_key
        self.hashed_license = get_string_md5(license_key)
        self.hwid = get_hwid()
        self.last_checked = None
        self.authorization_header = 'e5b7109e32cbbcdadb8295e2b07625c2'
        if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS') or os.path.basename(sys.executable).lower().startswith('python'):
            self.authorization_header = '21a1e56f23a2aac9cf0005753b92633b'


    def authenticate(self):
        auth_headers = {
            'Authorization': self.authorization_header,
            'User-Agent': 'Blockfriend v1' }
        data = json.dumps({
            'license': self.license_key,
            'hwid': self.hwid,
            'type': check_nerd_level() })
        data = encrypt_cbc(data)


    def heartbeat(self):
        if self.last_checked and int(time.time()) - self.last_checked < 30:
            return (True, '0')
        auth_headers = {
            'Authorization': None.authorization_header,
            'User-Agent': 'Blockfriend v1' }
        data = json.dumps({
            'license': self.license_key,
            'hwid': self.hwid,
            'type': check_nerd_level() })
        data = encrypt_cbc(data)


    def log_auth_error(self, error_message):
        log_headers = {
            'Authorization': self.authorization_header,
            'User-Agent': 'Blockfriend v1' }
        data = json.dumps({
            'license': self.license_key,
            'hwid': self.hwid,
            'id': error_message })
        data = encrypt_cbc(data)


    def is_banned_process_running(self):
        return (False, '')


    def is_memory_dumped(self):
        if os.name == 'nt':
            tempdir = tempfile.gettempdir()
        return (False, '')


    def run_security_checks(self):
        (failed_process_check, process_name) = self.is_banned_process_running()
        if failed_process_check:
            self.log_auth_error(process_name)
            return False
        (is_dumped, dump_name) = None.is_memory_dumped()
        if is_dumped:
            self.log_auth_error(dump_name)
            return False
        (heartbeat_result, heartbeat_status_code) = None.heartbeat()
        if heartbeat_result or heartbeat_status_code not in ('0', '616C6C73'):
            self.log_auth_error(heartbeat_status_code)
            return False


    def security_check_loop(self):
        pass


    def kill_bot(self):
        sys.exit()