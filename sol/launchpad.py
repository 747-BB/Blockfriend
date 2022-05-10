from imports import *
from helpers import AsyncSession

class Launchpad(InstructionLaboratory):
    session: AsyncSession = None

    def __init__(self):
        self.client = AsyncClient
        self.provider = anchorpy.Provider
        self.idl = anchorpy.Idl
        self.program = anchorpy.Program
        self.cm = None
        (self.token_mint, self.soldout) = ((True, False), (True, False))
        self.session = self.get_session()
        self.proxy_list = []


    async def entrypoint(self, config, mint_config, task_id, rpc_client):
        '''Task start entry point. Handle all logic from construction to broadcast.'''
        await self.log_task_info(task_id, f'''Using rpc client: {rpc_client._provider.endpoint_uri}''')
        await self.wait_before_broadcast(mint_config, task_id)
        txids = None


    def get_session(cls):
        if not cls.session:
            cls.session = AsyncSession()
        return cls.session

    get_session = classmethod(get_session)

    async def create(cls, config, **kw):
        self = cls()
        self.rpc_list = config.rpc_list
        self.client = AsyncClient(config.rpc)
        self.kp = Keypair()
        self.provider = anchorpy.Provider(self.client, self.kp)
        await anchorpy.Program.fetch_idl(kw.get('program', LAUNCHPAD_PROGRAM), self.provider)
        #self.idl = <NODE:27>Unsupported Node type: 27

        self.program = anchorpy.Program(self.idl, LAUNCHPAD_PROGRAM, self.provider)
        self.target = PublicKey(config.target)
        self.proxy_list = config.proxy_list
        await self.fetch()
        return self

    create = classmethod(create)

    #async def fetch(self = None):