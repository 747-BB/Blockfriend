import asyncio
from urllib.parse import urlparse
from solver_base import SolverBase, SolverError, FatalSolverError
FATAL_ERRORS = [
    'ERROR_WRONG_USER_KEY',
    'ERROR_KEY_DOES_NOT_EXIST',
    'ERROR_ZERO_BALANCE',
    'ERROR_PAGEURL',
    'IP_BANNED',
    'ERROR_BAD_TOKEN_OR_PAGEURL',
    'ERROR_GOOGLEKEY',
    'ERROR_BAD_PROXY']

class TwoCaptcha(SolverBase):

    def __init__(self = None, **kwargs):
        pass


    def get_params(self = None):
        '''Returns the params for the specific config of this solve.'''
        params = {
            'key': self.api_key,
            'pageurl': self.url }
        if self.version == 'h':
            payload = {
                'method': 'hcaptcha',
                'sitekey': self.site_key }
        else:
            payload = {
                'googlekey': self.site_key,
                'method': 'userrecaptcha',
                'version': self.version }
            if self.version == 'v2':
                payload['invisible'] = '1' if self.invisible else '0'
            elif self.version == 'v3' and self.action:
                payload['action'] = self.action
        if self.proxies:
            uri = urlparse(self.proxies)
            proxy_payload = {
                'proxy': uri.netloc,
                'proxytype': 'HTTP' }
            params.update(proxy_payload)
        params.update(payload)
        return params


    def handle_error(self = None, error_code = None):
        if error_code in FATAL_ERRORS:
            raise FatalSolverError
        raise SolverError


    async def _get_captcha_id(self = None):
        '''Submits the captcha and gets the `captcha_id`.'''
        params = self.get_params()
        endpoint = 'https://2captcha.com/in.php'
        await self.s.post(endpoint, self.headers, params, **('headers', 'data'))
        #response = <NODE:27>Unsupported Node type: 27

        if response.text.startswith('OK|'):
            captcha_id = response.text.split('|')[1]
            return captcha_id
        None.handle_error(response.text)


    async def _get_captcha_token(self = None, captcha_id = None):
        '''Polls the API & retrives a captcha token.'''
        params = {
            'id': captcha_id,
            'action': 'get',
            'key': self.api_key }
        await self.s.get('https://2captcha.com/res.php', self.headers, params, **('headers', 'params'))
        #response = <NODE:27>Unsupported Node type: 27

        if 'CAPCHA_NOT_READY' in response.text:
            await asyncio.sleep(self.sleep_time)
            await self.s.get('https://2captcha.com/res.php', self.headers, params, **('headers', 'params'))
            #response = <NODE:27>Unsupported Node type: 27

        if response.text.startswith('OK|'):
            captcha_token = response.text.split('OK|')[1]
            return captcha_token
        None.handle_error(response.text)

    __classcell__ = None