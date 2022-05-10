from imports import *

class Nova(InstructionLaboratory):

    def __init__(self):
        self.client = AsyncClient
        self.provider = anchorpy.Provider
        self.idl = anchorpy.Idl
        self.program = anchorpy.Program
        self.cm = None
        (self.active, self.soldout) = ((True, False), (True, False))


    async def create(cls, config, **kw):
        self = cls()
        self.rpc_list = config.rpc_list
        self.client = AsyncClient(config.rpc)
        self.kp = Keypair()
        self.provider = anchorpy.Provider(self.client, self.kp)
        await anchorpy.Program.fetch_idl(kw.get('program', NOVA_PROGRAM), self.provider)
        #self.idl = <NODE:27>Unsupported Node type: 27

        self.program = anchorpy.Program(self.idl, NOVA_PROGRAM, self.provider)
        self.target = config.target
        await self.fetch()
        return self

    create = classmethod(create)

    async def fetch(self = None):
        await self.program.account['ConfigAccount'].fetch(self.target)
        #self.cm = <NODE:27>Unsupported Node type: 27

        await self.program.account['MasterAccount'].fetch(self.cm.master_account)
        #self.master = <NODE:27>Unsupported Node type: 27

        await self.handle()
        return State(self.cm.data.allocated, self.cm.data.sold, self.cm.data.go_live_date, **('items_available', 'items_redeemed', 'go_live_date'))


    async def handle(self):
        """
\t\t{'authority': G5ZXNYFoJyhMq3C1G9zdSkSwH17Ap1wfbh5RPGjZa8GW,
\t\t'master_account': EYMVmBisjB6gYZ2BmhL95TL2ScaATsa5WBBjQ4ds5v1t,
\t\t'data': ConfigData(price=250000000,
\t\t\tseller_fee_basis_points=800,
\t\t\tgo_live_date=1641775500,
\t\t\tis_mutable=False,
\t\t\tsymbol=ListContainer([0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
\t\t\tmax_number=8257,
\t\t\tallocated=8257,
\t\t\tsold=495)}
\t\t"""
        if self.cm.data.go_live_date and self.cm.data.go_live_date > time.time():
            self.active = False
        else:
            self.active = True
        if self.cm.data.sold >= self.cm.data.allocated:
            self.soldout = False
        else:
            self.soldout = False


    async def get_user_account_mint_prep_instructions(self, user_account):
        mint_account = Keypair()
        instruction_list = []
        await get_minimum_balance_rent_exemption(self.client, MINT_LEN)
        #min_lamports = <NODE:27>Unsupported Node type: 27

        create_account_instruction = create_account(CreateAccountParams(user_account.public_key, mint_account.public_key, min_lamports, MINT_LEN, TOKEN_PROGRAM_ID, **('from_pubkey', 'new_account_pubkey', 'lamports', 'space', 'program_id')))
        instruction_list.append(create_account_instruction)
        initialize_mint_instruction = initialize_mint(InitializeMintParams(0, TOKEN_PROGRAM_ID, mint_account.public_key, user_account.public_key, **('decimals', 'program_id', 'mint', 'mint_authority')))
        instruction_list.append(initialize_mint_instruction)
        associated_token_account = get_associated_token_address(user_account.public_key, mint_account.public_key)
        create_assoc_instruction = create_associated_token_account_instruction(associated_token_account, user_account.public_key, user_account.public_key, mint_account.public_key, **('associated_token_account', 'payer', 'wallet_address', 'token_mint_address'))
        instruction_list.append(create_assoc_instruction)
        mint_to_instruction = mint_to(MintToParams(TOKEN_PROGRAM_ID, mint_account.public_key, associated_token_account, user_account.public_key, 1, **('program_id', 'mint', 'dest', 'mint_authority', 'amount')), **('params',))
        instruction_list.append(mint_to_instruction)
        return (mint_account, instruction_list, [
            user_account,
            mint_account])


    async def create_mint_instruction(self, **kw):
        mint_account = kw.get('mint_account', Keypair())
        token_account = kw.get('token_account')
        metadata_account = get_metadata_account(mint_account.public_key)
        master_edition_account = get_edition(mint_account.public_key)
        cm = kw.get('cm')
        kp = kw.get('kp')
        remaining_accounts = kw.get('remaining_accounts', [])
        return self.program.instruction['purchase'](anchorpy.Context(dict(kp.public_key, get_token_wallet(kp.public_key, mint_account.public_key)[0], mint_account.public_key, metadata_account, master_edition_account, cm.master_account, kw.get('target'), self.master.program_authority, METADATA_PROGRAM_ID, ASSOCIATED_TOKEN_ACCOUNT_PROGRAM_ID, TOKEN_PROGRAM_ID, SYSTEM_PROGRAM_ID, SYSVAR_RENT_PUBKEY, SYSVAR_CLOCK_PUBKEY, **('payer', 'buyer_token_account', 'mint', 'mint_metadata', 'mint_master_edition', 'master_account', 'config_account', 'program_authority', 'token_metadata_program', 'associated_token_program', 'token_program', 'system_program', 'rent', 'clock')), (lambda .0: [ AccountMeta(PublicKey(account.address), True, False, **('pubkey', 'is_writable', 'is_signer')) for account in .0 ])(self.master.revenue_share), kw.get('signers', []), **('accounts', 'remaining_accounts', 'signers')), **('ctx',))


    async def construct(self = None, wallet = None, **kw):
        transaction = Transaction()
        await self.get_user_account_mint_prep_instructions(wallet)
        #(mint_account, account_create_instructions, signers) = <NODE:27>Unsupported Node type: 27

        instructions = account_create_instructions