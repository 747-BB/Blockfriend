from imports import *
import urllib.parse as urllib
import random
import json

def format_selected_traits(trait_list):
    result = { }
    if trait_type not in result:
        result[trait_type] = []
    result[trait_type].append(trait_value)
    return result


class MagicEdenSniper(InstructionLaboratory):
    session: AsyncSession = None

    def __init__(self):
        self.client = AsyncClient
        self.session = self.get_session()
        self.proxy_list = []


    def get_session(cls):
        if not cls.session:
            cls.session = AsyncSession()
        return cls.session

    get_session = classmethod(get_session)

    async def create(cls, config, **kw):
        self = cls()
        self.rpc_list = config.rpc_list
        self.client = AsyncClient(config.rpc)
        self.proxy_list = config.proxy_list
        return self

    create = classmethod(create)

    async def entrypoint(self, config, mint_config, task_id, rpc_client):
        await self.log_task_info(task_id, f'''Using rpc client: {rpc_client._provider.endpoint_uri}''')
        await self.wait_until_match(config, mint_config, task_id)
        #matched_listing = <NODE:27>Unsupported Node type: 27

        await self.log_task_info(task_id, f'''Generating tx for listing: {matched_listing.get('title')} | {matched_listing.get('price')} SOL''')
        order_result = None


    async def broadcast(self, raw_tx_bytes, mint_config, task_id, rpc_client):
        msg = Message.deserialize(raw_tx_bytes)
        tx = Transaction.populate(msg, [])
        await rpc_client.get_recent_blockhash('confirmed')
        #blockhash_response = <NODE:27>Unsupported Node type: 27

        blockhash = Blockhash(blockhash_response['result']['value']['blockhash'])
        tx.recent_blockhash = blockhash
        tx.fee_payer = mint_config.wallet.public_key
        tx.sign(mint_config.wallet)
        await rpc_client.send_raw_transaction(tx.serialize(), TxOpts(True, **('skip_preflight',)), **('opts',))
        #res = <NODE:27>Unsupported Node type: 27

        await self.log_task_info(task_id, f'''Broadcasted: {res.get('result', None)}''')
        return res.get('result', None)


    async def wait_until_match(self, config, mint_config, task_id):
        collection_symbol = config.target
        monitor_delay = int(mint_config.monitor_delay) / 1000
        max_price = float(mint_config.max_price)
        selected_traits = format_selected_traits(mint_config.selected_traits)
        await self.log_task_info(task_id, 'Checking recent listings...')
    # WARNING: Decompyle incomplete


    async def check_recent_listings(self = None, collection_symbol = None, max_price = None, selected_traits = {
        'collection_symbol': str,
        'max_price': float,
        'selected_traits': dict }):
        await self.get_collection_listings(collection_symbol)
        #recent_listings = <NODE:27>Unsupported Node type: 27



    def check_listing_critera(self = None, listing = None, max_price = None, selected_traits = {
        'max_price': float,
        'selected_traits': dict }):
        listing_price = listing.get('price')
        if listing_price > max_price:
            return False
        if not None:
            return True
        trait_matches = None
        listing_traits = listing.get('attributes')
        return False


    async def get_collection_listings(self, collection_symbol):
        if not self.session.initialized:
            await self.session.init()
        headers = {
            'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="96", "Google Chrome";v="96"',
            'accept': 'application/json, text/plain, */*',
            'content-type': 'application/json',
            'sec-ch-ua-mobile': '?0',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36',
            'sec-ch-ua-platform': '"macOS"',
            'origin': 'https://magiceden.io',
            'sec-fetch-site': 'same-site',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            'referer': 'https://magiceden.io/',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'da-DK,da;q=0.9,en-US;q=0.8,en;q=0.7' }
        q_value = {
            '$match': {
                'collectionSymbol': collection_symbol },
            '$sort': {
                'createdAt': -1 },
            '$skip': 0,
            '$limit': 20 }
        params = {
            'q': urllib.parse.quote(json.dumps(q_value)) }
        url = 'https://api-mainnet.magiceden.io/rpc/getListedNFTsByQuery'
        await self.session.get(url, headers, params, **('headers', 'params'))
        #response = <NODE:27>Unsupported Node type: 27

        if response.status_code != 200:
            if response.status_code == None:
                raise Exception('Unable to fetch collection listings, connection timed out.')
            if response.status_code == 429:
                if len(self.proxy_list) > 0:
                    await self.session.change_proxy(random.choice(self.proxy_list))
                raise Exception('Rotated proxy, unable to fetch collection listings due to rate limit.')
            raise Exception(f'''Unable to fetch collection listings, received status: {response.status_code}''')
        response_json = None.json()
        recent_listings = response_json.get('results')
        return recent_listings


    async def get_buy_now_instructions(self, listing, mint_config):
        [
            None,
            None]
        if not self.session.initialized:
            await self.session.init()
        headers = {
            'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="96", "Google Chrome";v="96"',
            'accept': 'application/json, text/plain, */*',
            'content-type': 'application/json',
            'sec-ch-ua-mobile': '?0',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36',
            'sec-ch-ua-platform': '"macOS"',
            'origin': 'https://magiceden.io',
            'sec-fetch-site': 'same-site',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            'referer': 'https://magiceden.io/',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'da-DK,da;q=0.9,en-US;q=0.8,en;q=0.7' }
        params = {
            'buyer': mint_config.wallet.public_key,
            'seller': listing.get('owner'),
            'auctionHouseAddress': listing.get('v2').get('auctionHouseKey'),
            'tokenMint': listing.get('mintAddress'),
            'tokenATA': listing.get('id'),
            'price': listing.get('price'),
            'sellerReferral': listing.get('v2').get('sellerReferral'),
            'sellerExpiry': listing.get('v2').get('expiry') }
        url = 'https://api-mainnet.magiceden.io/v2/instructions/buy_now'
        await self.session.get(url, headers, params, **('headers', 'params'))
        #response = <NODE:27>Unsupported Node type: 27

        if response.status_code != 200:
            if response.status_code == None:
                raise Exception('Unable to generate tx for listing, connection timed out.')
            if response.status_code == 429:
                if len(self.proxy_list) > 0:
                    await self.session.change_proxy(random.choice(self.proxy_list))
                raise Exception('Rotated proxy, unable to generate tx for listing due to rate limit.')
            raise Exception(f'''Unable to generate tx for listing, received status: {response.status_code}''')
        response_json = None.json()
        tx_byte_array = response_json.get('tx').get('data')
        return bytes(tx_byte_array)
