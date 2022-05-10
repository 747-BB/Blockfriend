import asyncio
from urllib.parse import urlparse
from solver_base import SolverBase, SolverError, FatalSolverError
FATAL_ERRORS = [
    'ERROR_KEY_DOES_NOT_EXIST',
    'ERROR_NO_SLOT_AVAILABLE',
    'ERROR_ZERO_BALANCE',
    'ERROR_IP_NOT_ALLOWED',
    'ERROR_IP_BLOCKED',
    'ERROR_PROXY_CONNECT_REFUSED',
    'ERROR_PROXY_CONNECT_TIMEOUT',
    'ERROR_PROXY_READ_TIMEOUT',
    'ERROR_PROXY_BANNED',
    'ERROR_PROXY_TRANSPARENT',
    'ERROR_RECAPTCHA_INVALID_SITEKEY',
    'ERROR_RECAPTCHA_INVALID_DOMAIN',
    'ERROR_PROXY_INCOMPATIBLE_HTTP_VERSION',
    'ERROR_PROXY_NOT_AUTHORISED',
    'ERROR_ACCOUNT_SUSPENDED',
    'ERROR_TOO_MUCH_REQUESTS',
    'ERROR_DOMAIN_NOT_ALLOWED',
    'ERROR_IP_NOT_ALLOWED',
    'ERROR_PROXY_TIMEOUT']

class CapMonster(SolverBase):

    def __init__(self = None, **kwargs):
        pass


    def get_version_id(self = None):
        '''Gets the corresponding CapMonster `type`.'''
        version_map = {
            'v2': 'NoCaptchaTask',
            'v3': 'RecaptchaV3TaskProxyless',
            'h': 'HCaptchaTask' }
        version_id = version_map[self.version]
        if self.proxies and self.version in ('v2', 'h'):
            version_id += 'Proxyless'
        return version_id


    def parse_proxy(self = None, proxy_string = None):
        """Parses given proxy into CapMonster's expected format."""
        parsed = urlparse(proxy_string)
        return None(dict, 'http' if parsed.scheme == 'https' else parsed.scheme, parsed.hostname, parsed.port, '' if not parsed.username else '', **('proxyType', 'proxyAddress', 'proxyPort', 'proxyLogin', 'proxyPassword'))


    def get_payload(self = None):
        '''Returns the payload for the specific config of this solve.'''
        version_id = self.get_version_id()
        payload = {
            'type': version_id,
            'websiteURL': self.url,
            'websiteKey': self.site_key }
        if self.version == 'v3':
            if self.action:
                payload['pageAction'] = self.action
            payload['minScore'] = 0.3
        if self.proxies and 'Proxyless' not in version_id:
            proxy_payload = self.parse_proxy(self.proxies)
            payload.update(proxy_payload)
        return {
            'clientKey': self.api_key,
            'task': payload }


    def handle_error(self = None, result = None):
        error_code = result['errorCode']
        if error_code in FATAL_ERRORS:
            raise FatalSolverError
        raise SolverError


    async def _get_captcha_id(self = None):
        '''Submits the captcha and gets the `captcha_id`.'''
        payload = self.get_payload()
        endpoint = 'https://api.capmonster.cloud/createTask'
        await self.s.post(endpoint, self.headers, payload, **('headers', 'json'))
        #response = <NODE:27>Unsupported Node type: 27

        result = response.json()
        if 'taskId' in result:
            captcha_id = result['taskId']
            return captcha_id
        None.handle_error(result)


    async def _get_captcha_token(self = None, captcha_id = None):
        '''Polls the API & retrives a captcha token.'''
        payload = {
            'clientKey': self.api_key,
            'taskId': captcha_id }
        await self.s.post('https://api.capmonster.cloud/getTaskResult', self.headers, payload, **('headers', 'json'))
        #response = <NODE:27>Unsupported Node type: 27

        result = response.json()
        if result['status'] == 'processing':
            await asyncio.sleep(self.sleep_time)
            await self.s.post('https://api.capmonster.cloud/getTaskResult', self.headers, payload, **('headers', 'json'))
            #response = <NODE:27>Unsupported Node type: 27

            result = response.json()
        if result['status'] == 'ready':
            captcha_token = result['solution']['gRecaptchaResponse']
            return captcha_token
        None.handle_error(result)

    __classcell__ = None