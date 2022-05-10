from typing import Tuple
from borsh_construct import I64, U8, U64, CStruct, Option, String
from construct import Adapter, Bytes, Container
from solana import publickey
from sol.imports import *
from sol.utils import get_proof

class _PublicKey(Adapter):

    def __init__(self = None):
        super().__init__(Bytes(32))


    def _decode(self = None, obj = None, context = None, path = {
        'obj': bytes,
        'return': publickey.PublicKey }):
        return publickey.PublicKey(obj)


    def _encode(self = None, obj = None, context = None, path = {
        'obj': publickey.PublicKey,
        'return': bytes }):
        return bytes(obj)

    __classcell__ = None

PublicKeyType = _PublicKey()

class CivicWorker:

    def __init__(self, wallet = None, captcha_config = None, client = None, proxy = {
        'wallet': dict,
        'captcha_config': dict,
        'client': Client,
        'proxy': str }):
        self.wallet = wallet
        self.captcha_config = captcha_config
        self.client = client
        self.proxy = proxy
        self.session = AsyncSession(self.proxy, **('proxy',))


    async def get_captcha(self = None):
        '''Returns a valid hCaptcha token.'''
        handler = CaptchaHandler(self.session, 'h', '3fe6bf88-7035-45b7-8f56-c9de61a1ca48', 'https://passv2.civic.com/', self.captcha_config, self.proxy, **('session', 'version', 'site_key', 'url', 'config', 'proxies'))
        await handler.solve()
        #token = <NODE:27>Unsupported Node type: 27

        return token


    async def get_state(self = None, data = None):
        schema = CStruct('features' / U8, 'parent_gateway_token' / Option(PublicKeyType), 'owner_wallet' / PublicKeyType, 'owner_identity' / Option(PublicKeyType), 'gatekeeper_network' / PublicKeyType, 'issuing_gatekeeper' / PublicKeyType, 'state' / U8, 'expire_time' / Option(I64))
        return schema.parse(data)


    async def get_pass(self = None):
        '''Requests a Civic Pass for this wallet.'''
        if not self.session.initialized:
            await self.session.init()
        keypair = Keypair(self.wallet['PrivateKey'][:32])
        account = self.client.get_account_info(get_network_token(keypair.public_key, GATEKEEPER_NETWORK)[0])
        if account['result']['value']:
            await self.get_state(base64.b64decode(account['result']['value']['data'][0]))
            #state = <NODE:27>Unsupported Node type: 27

            if state.state == 0 and state.expire_time > time.time():
                return (keypair.public_key, 'ACTIVE')
            await None.get_captcha()
            #captcha = <NODE:27>Unsupported Node type: 27

            await get_proof(keypair, self.client)
            #proof = <NODE:27>Unsupported Node type: 27

            headers = {
                'Connection': 'keep-alive',
                'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="96", "Google Chrome";v="96"',
                'X-Civic-Client': '@civic/solana-gateway-react:0.4.12',
                'sec-ch-ua-mobile': '?0',
                'Content-Type': 'application/json',
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.109 Safari/537.36',
                'sec-ch-ua-platform': '"macOS"',
                'Accept': '*/*',
                'Origin': 'https://getpass.civic.com',
                'Sec-Fetch-Site': 'same-site',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Dest': 'empty',
                'Referer': 'https://getpass.civic.com/',
                'Accept-Language': 'da-DK,da;q=0.9,en-US;q=0.8,en;q=0.7',
                'Accept-Encoding': 'gzip, deflate, br' }
            if account['result']['value']:
                method = 'PATCH'
                url = f'''https://gatekeeper-api.civic.com/v1/token/solana/{keypair.public_key}?network=mainnet-beta&gatekeeperNetworkAddress={GATEKEEPER_NETWORK}'''
                data = {
                    'proof': proof,
                    'request': 'refresh',
                    'acceptedDeclaration': "1. You confirm, to your knowledge, that you're not a bot, do in fact breathe oxygen, and may or may not have what is commonly referred to as a soul.",
                    'provider': 'hcaptcha',
                    'captchaToken': captcha }
            else:
                method = 'POST'
                url = f'''https://gatekeeper-api.civic.com/v1/token/solana?network=mainnet-beta&gatekeeperNetworkAddress={GATEKEEPER_NETWORK}'''
                data = {
                    'acceptedDeclaration': "1. You confirm, to your knowledge, that you're not a bot, do in fact breathe oxygen, and may or may not have what is commonly referred to as a soul.",
                    'acceptedTermsAndConditionsLink': 'https://www.civic.com/legal/terms-of-service-civic-pass-v1',
                    'provider': 'hcaptcha',
                    'captchaToken': captcha,
                    'proof': proof,
                    'address': str(keypair.public_key) }
        await self.session.request(method, url, data, headers, **('url', 'json', 'headers'))
        #response = <NODE:27>Unsupported Node type: 27

        return (keypair.public_key, response.json().get('state', 'ACTIVE') if response.status_code in (200, 201, 202) else 'REJECTED')
