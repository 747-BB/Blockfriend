from time import sleep
import requests
from bs4 import BeautifulSoup as bs
from web3 import HTTPProvider, Web3

class ETH:

    def __init__(self, taskData):
        self.running = True
        self.taskData = taskData
        self.m_web3 = Web3(HTTPProvider(self.taskData.get('rpc_url1')))
        if not self.taskData.get('rpc_url1'):
            pass
        self.web3 = Web3(HTTPProvider(self.taskData.get('rpc_url2')))
        self.tryCount = 0
        print(f'''Minting {self.taskData.get('contract_address')} for {self.taskData.get('mint_price')}''')
        if not self.taskData.get('mint_data'):
            print('Using ABI')
            self.contract = self.m_web3.eth.contract(self.taskData.get('abi'), self.taskData.get('contract_address'), **('abi', 'address'))
            if len(self.taskData.get('mint_parameters')) > 0:
                transaction = self.contract.methods[self.taskData.get('mint_function')]
            else:
                transaction = self.contract.functions[self.taskData.get('mint_function')]
        else:
            transaction = self.taskData.get('mint_data')


    async def mint(self, private_key):
        tryCount = 0
        transaction = None
        print(f'''Minting {self.taskData.get('contract_address')} for {self.taskData.get('mint_price')} ETH''')


    async def estimateGas(self = None, transaction = None, account = None, price = {
        'return': str }):
        gas_estimate = self.web3.eth.estimateGas({
            'to': self.taskData.get('contract_address'),
            'data': self.taskData.get('mint_data') if self.taskData.get('mint_data') else transaction.encodedABI(),
            'from': account,
            'value': price })
        print(f'''Gas Estimate: {gas_estimate}''')
        return gas_estimate


    async def getPendingTxs(self = None, address = None, page = None):
        [
            None,
            None]
        maxAttempts = 5