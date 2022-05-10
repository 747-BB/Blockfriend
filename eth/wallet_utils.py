import asyncio
import copy
import random
from typing import Tuple
CHAIN = 'ETH'

class EthWalletUtils:

    def __init__(self, **kw):
        (self.wm, self.cm, self.rm, self.am) = (kw.get('wm'), kw.get('cm'), kw.get('rm'), kw.get('am'))
        self.rpc_url = self.cm.get('ETH', 'RPC')


    def mint(self = None, user_input = None):
        pass