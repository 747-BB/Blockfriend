from imports import *
from helpers import AsyncSession

class CMV2(InstructionLaboratory):
    session: AsyncSession = None

    def __init__(self):
        self.client = AsyncClient
        self.provider = anchorpy.Provider
        self.idl = anchorpy.Idl
        self.program = anchorpy.Program
        self.cm = None
        (self.token_mint, self.whitelist, self.active, self.ended, self.soldout) = ((True, False), (True, False), (True, False), (True, False), (True, False))
        self.session = self.get_session()


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
        await anchorpy.Program.fetch_idl(kw.get('program', SOLANA_CMV2_PROGRAM), self.provider)
        #self.idl = <NODE:27>Unsupported Node type: 27

        self.program = anchorpy.Program(self.idl, SOLANA_CMV2_PROGRAM, self.provider)
        self.target = config.target
        await self.fetch()
        return self

    create = classmethod(create)

    async def fetch(self = None):
        await self.program.account['CandyMachine'].fetch(self.target)
        #self.cm = <NODE:27>Unsupported Node type: 27

        await self.handle()
        return State(self.cm.data.items_available, self.cm.items_redeemed, self.cm.data.go_live_date, **('items_available', 'items_redeemed', 'go_live_date'))


    async def handle(self):
        """
\t\tCandyMachine(
\t\t\tauthority=SLG3YBuM31VzjcisnpDPjZPkTTuhTuQiRnqzBwicYCx,
\t\t\twallet=SLG3YBuM31VzjcisnpDPjZPkTTuhTuQiRnqzBwicYCx,
\t\t\ttoken_mint=None,
\t\t\titems_redeemed=777,
\t\t\tdata=CandyMachineData(
\t\t\t\tuuid='C5cqme',
\t\t\t\tprice=1000000000,
\t\t\t\tsymbol='BF\x00\x00\x00\x00\x00\x00\x00\x00',
\t\t\t\tseller_fee_basis_points=1000,
\t\t\t\tmax_supply=0,
\t\t\t\tis_mutable=True,
\t\t\t\tretain_authority=True,
\t\t\t\tgo_live_date=1642444200,
\t\t\t\tend_settings=None,
\t\t\t\tcreators=ListContainer(
\t\t\t\t\t[Creator(address=GEAxiZdEJqrwjJkzEpnC7Kcc1CGH5ujGjn2jK1FRVAeP, verified=True, share=50),
\t\t\t\t\tCreator(address=DHPFzMQsGGk4twh3A1Ssc7Wj19DknzVJNbjar5sKTWg4, verified=True, share=50)]
\t\t\t\t),
\t\t\t\thidden_settings=None,
\t\t\t\twhitelist_mint_settings=WhitelistMintSettings(
\t\t\t\t\tmode=WhitelistMintMode.BurnEveryTime(),
\t\t\t\t\tmint=WLkzLgziRh7VDzdhxtPH8WJDWqbQQNar1EQoceFAFir,
\t\t\t\t\tpresale=True, discount_price=None
\t\t\t\t),
\t\t\t\titems_available=777,
\t\t\t\tgatekeeper=None
\t\t\t)
\t\t)
\t\t"""
        [
            None,
            None]
        if self.cm.token_mint:
            self.token_mint = True
        else:
            self.token_mint = False
        if self.cm.data.whitelist_mint_settings:
            self.whitelist = True
        else:
            self.whitelist = False
        if not self.cm.data.go_live_date and self.cm.data.go_live_date > time.time() and self.cm.data.end_settings:
            self.active = False
        else:
            self.active = True
        if self.cm.data.end_settings:
            if hasattr(self.cm.data.end_settings.end_setting_type, 'date'):
                if time.time() > self.cm.data.end_settings.value:
                    self.ended = True
                else:
                    self.ended = False
            elif hasattr(self.cm.data.end_settings.end_setting_type, 'amount'):
                if self.cm.items_redeemed >= self.cm.data.end_settings.value:
                    self.ended = True
                else:
                    self.ended = False
            else:
                self.ended = False
        if self.cm.items_redeemed >= self.cm.data.items_available:
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
        initialize_mint_instruction = initialize_mint(InitializeMintParams(0, TOKEN_PROGRAM_ID, mint_account.public_key, user_account.public_key, user_account.public_key, **('decimals', 'program_id', 'mint', 'mint_authority', 'freeze_authority')))
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
        metadata_account = get_metadata_account(mint_account.public_key)
        master_edition_account = get_edition(mint_account.public_key)
        (cm_creator, creator_bump) = get_creator(kw.get('target'))
        cm = kw.get('cm')
        kp = kw.get('kp')
        remaining_accounts = kw.get('remaining_accounts', [])
        return self.program.instruction['mint_nft'](creator_bump, anchorpy.Context(dict(kw.get('target'), cm_creator, kp.public_key, cm.wallet, metadata_account, mint_account.public_key, kp.public_key, kp.public_key, master_edition_account, METADATA_PROGRAM_ID, TOKEN_PROGRAM_ID, SYSTEM_PROGRAM_ID, SYSVAR_RENT_PUBKEY, SYSVAR_CLOCK_PUBKEY, SYSVAR_RECENT_BLOCKHASHES_PUBKEY, SYSVAR_INSTRUCTIONS, **('candy_machine', 'candy_machine_creator', 'payer', 'wallet', 'metadata', 'mint', 'mint_authority', 'update_authority', 'master_edition', 'token_metadata_program', 'token_program', 'system_program', 'rent', 'clock', 'recent_blockhashes', 'instruction_sysvar_account')), remaining_accounts, kw.get('signers', []), **('accounts', 'remaining_accounts', 'signers')), **('ctx',))


    async def construct(self = None, wallet = None, **kw):
        remaining_accounts = []
        transaction = Transaction()
        await self.get_user_account_mint_prep_instructions(wallet)
        #(mint_account, account_create_instructions, signers) = <NODE:27>Unsupported Node type: 27

        instructions = account_create_instructions