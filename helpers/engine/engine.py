import os
import sys
import time
import json
import psutil
import asyncio
import requests
import functools
import subprocess
from itertools import cycle
from utils import get_engine_path
PAYLOAD_KEY = [
    87,
    77,
    7,
    157,
    21,
    37,
    102,
    29,
    29,
    180,
    114,
    69,
    6,
    53,
    228,
    83,
    159,
    201,
    165,
    98,
    203,
    238,
    246,
    102,
    0,
    7,
    64,
    224,
    161,
    85,
    186,
    250,
    29,
    208,
    244,
    54,
    31,
    151,
    19,
    74,
    178,
    210,
    74,
    65,
    28,
    208,
    228,
    10,
    23,
    198,
    3,
    215,
    19,
    140,
    79,
    158,
    118,
    85,
    245,
    164,
    42,
    69,
    148,
    71]

def xor_encrypt(data, key):
    return bytes((lambda .0: [ a ^ b for a, b in .0 ])(zip(data, cycle(key)))).hex()


def encrypt_payload(payload):
    ciphertext = xor_encrypt(json.dumps(payload).encode('utf8'), PAYLOAD_KEY)
    return {
        'Ciphertext': ciphertext }


class Engine:
    am = None
    engine_port = 6824
    initialized = False
    engine_process = None
    restart_in_progress = False

    def __init__(cls, am, pm = (None, None)):
        if cls.initialized and am is not None:
            cls.update(am, pm)
            cls.start()


    def update(cls, am, pm):
        cls.am = am
        cls.pm = pm

    update = classmethod(update)

    def start(cls, prompt_exit = (True,)):
        '''Initializes the engine connection.'''
        if cls.restart_in_progress:
            return None
        cls.initialized = None
        cls.restart_in_progress = True
        del cls.engine_process
        cls.close_existing()

    start = classmethod(start)

    def initialize_settings(cls):
        payload = {
            'Proxies': cls.pm.proxy_list }
        response = None

    initialize_settings = classmethod(initialize_settings)

    async def start_task(cls = None, config = None):
        response = None

    start_task = None(start_task)

    async def prefetch_cm(cls = None, config = None):
        response = None

    prefetch_cm = None(prefetch_cm)

    #def close_existing():