from typing import TYPE_CHECKING, Optional, Tuple
from anticaptcha import AntiCaptcha
from capmonster import CapMonster
from twocaptcha import TwoCaptcha
if TYPE_CHECKING:
    from client.async_session import AsyncSession
    from solver_base import SolverBase

class CaptchaHandler:

    def __init__(self, session, version, site_key, url, config = None, action = None, proxies = None, invisible = ('verify', None, False, None), user_agent = {
        'session': 'AsyncSession',
        'version': str,
        'site_key': str,
        'url': str,
        'config': dict,
        'action': str,
        'proxies': Optional[str],
        'invisible': bool,
        'user_agent': Optional[str] }):
        '''Initializer for CaptchaHandler.

\t\tsession: The `AsyncSession` object to use.
\t\tversion: The captcha version; ["v2", "v3", "h"].
\t\tsite_key: It\'s the sitekey bro.
\t\turl: URL to solve the captcha against, use homepage if unsure.
\t\tconfig: The API-keys mapped to 3rd-party providers.
\t\taction: The reCaptcha v3 pageAction.
\t\tproxies: HTTP Proxies to use, in the format; `http://user:pass@ip:port`.
\t\tinvisible: If this is an Invisible reCaptcha v2.
\t\tuser_agent: The User-Agent header to use.
\t\t'''
        self.s = session
        self.version = version
        self.site_key = site_key
        self.url = url
        self.config = config
        self.action = action
        self.proxies = proxies
        self.invisible = invisible
        self.user_agent = user_agent
        self.sleep_time = 5
        self.solver_map = {
            '2captcha': TwoCaptcha,
            'capmonster': CapMonster,
            'anticaptcha': AntiCaptcha }
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36(KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'sec-fetch-site': 'none',
            'sec-fetch-mode': 'navigate',
            'content-type': 'application/x-www-form-urlencoded',
            'sec-fetch-user': '?1',
            'sec-fetch-dest': 'document',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en-US,en;q=0.9' }
        if user_agent:
            self.headers['user-agent'] = user_agent
        self.ua = self.headers['user-agent']


    def kwargs(self = None):
        '''Returns the arguments for the solver.'''
        kwargs = self.__dict__.copy()
        return kwargs

    kwargs = None(kwargs)

    def get_captcha_service(self = None):
        '''Returns the first loaded captcha service.'''
        if self.config.get('2captcha'):
            return (TwoCaptcha, self.config.get('2captcha'))
        if None.config.get('anticaptcha'):
            return (AntiCaptcha, self.config.get('anticaptcha'))
        if None.config.get('capmonster'):
            return (CapMonster, self.config.get('capmonster'))
        return None


    async def solve(self = None):
        '''Requests a captcha token from the user-selected service.'''
        (Solver, self.api_key) = self.get_captcha_service()
        if Solver is None:
            print('TODO? Is there a better way we could handle this?')
            raise Exception('No Captcha API-keys loaded!')