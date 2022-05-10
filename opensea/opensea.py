import requests
from datetime import datetime
from opensea import utils

class OpenseaBase:
    BASE_API_URL = 'https://api.opensea.io/api'

    def __init__(self, endpoint, version = ('v1',)):
        '''Base class to interact with the OpenSea API and fetch NFT data.

        Args:
            endpoint (str): OpenSea API endpoint, eg. \'asset\' or \'collections\'
            version (str, optional): API version. Defaults to "v1".
        '''
        self.api_url = f'''{self.BASE_API_URL}/{version}/{endpoint}'''


    def _make_request(self, params, export_file_name, return_response = (None, '', False)):
        """Makes a request to the OpenSea API and returns either a response
        object or dictionary.

        Args:
            params (dict, optional): Query parameters to include in the
            request. Defaults to None.
            export_file_name (str, optional): In case you want to download the
            data into a file,
            specify the filename here. Eg. 'export.json'. Be default, no file
            is created.
            return_response (bool, optional): Set it True if you want it to
            return the actual response object.
            By default, it's False, which means a dictionary will be returned.

        Raises:
            ValueError: returns the error message from the API in case one
            (or more) of your request parameters are incorrect.

        Returns:
            Data sent back from the API. Either a response or dict object
            depending on the *return_response* argument.
        """
        response = requests.get(self.api_url, params, **('params',))
        if response.status_code == 400:
            raise ValueError(response.text)
        if response.status_code == 504:
            raise TimeoutError('The server reported a gateway time-out error.')
        if None != '':
            utils.export_file(response.content, export_file_name)
        if return_response:
            return response
        return None.json()



class Events(OpenseaBase):
    MAX_API_ITEMS = 300

    def __init__(self = None):
        '''Endpoint to fetch data about multiple events.
        More info about this endpoint in the OpenSea docs:
        https://docs.opensea.io/reference/retrieving-asset-events
        '''
        super().__init__('events', **('endpoint',))


    def fetch(self, asset_contract_address, collection_slug, token_id, account_address = None, event_type = None, only_opensea = None, auction_type = None, offset = None, limit = None, occurred_before = None, occurred_after = None, export_file_name = ((None, None, None, None, None, False, None, 0, None, None, None, ''),)):
        """Fetches Events data from the API. Function arguments will be passed
        as API query parameters.

        OpenSea API Events query parameters:
        https://docs.opensea.io/reference/retrieving-asset-events

        All arguments will be passed without modification, except
        *occurred_before* and *occurred_after*. For these two args, you need
        to use datetime objects when calling this function.

        There's one extra optional argument:
        export_file_name (str, optional): Exports the JSON data into a the
        specified file.

        Returns:
            [dict]: Events data
        """
        if not occurred_after is not None and isinstance(occurred_after, datetime):
            raise ValueError('occurred_after must be a datetime object')
        if not None is not None and isinstance(occurred_before, datetime):
            raise ValueError('occurred_before must be a datetime object')
        query_params = {
            'asset_contract_address': None,
            'collection_slug': collection_slug,
            'token_id': token_id,
            'account_address': account_address,
            'event_type': event_type,
            'only_opensea': only_opensea,
            'auction_type': auction_type,
            'offset': offset,
            'limit': self.MAX_API_ITEMS if limit is None else limit }
        if occurred_before is not None:
            query_params['occurred_before'] = occurred_before.timestamp()
        if occurred_after is not None:
            query_params['occurred_after'] = occurred_after.timestamp()
        return super()._make_request(query_params, export_file_name)

    __classcell__ = None


class Asset(OpenseaBase):

    def __init__(self = None, asset_contract_address = None, token_id = None):
        '''Endpoint to fetch data about a single asset.
        More info about this endpoint in the OpenSea docs:
        https://docs.opensea.io/reference/retrieving-a-single-asset

        Args:
            asset_contract_address (str)
            token_id (str):
        '''
        super().__init__(f'''asset/{asset_contract_address}/{token_id}''', **('endpoint',))


    def fetch(self = None, account_address = None, export_file_name = None):
        '''Fetches Asset data from the API.

        Args:
            account_address (str, optional). Defaults to None.
            export_file_name (str, optional): Exports the JSON data into a the
            specified file.

        Returns:
            [dict]: Single asset data
        '''
        query_params = {
            'account_address': account_address }
        return super()._make_request(query_params, export_file_name)

    __classcell__ = None


class Assets(OpenseaBase):
    MAX_API_ITEMS = 50

    def __init__(self = None):
        '''Endpoint to fetch data about multiple assets.
        More info about this endpoint in the OpenSea docs:
        https://docs.opensea.io/reference/getting-assets
        '''
        super().__init__('assets', **('endpoint',))


    def fetch(self, owner, token_ids = None, asset_contract_address = None, asset_contract_addresses = None, order_by = None, order_direction = None, offset = None, limit = None, collection = None, export_file_name = ((None, [], None, None, None, None, None, None, None, ''),)):
        """Fetches assets data from the API. Function arguments will be passed
        as API query parameters, without modification.

        OpenSea API Assets query parameters:
        https://docs.opensea.io/reference/getting-assets

        There's one extra optional argument:
        export_file_name (str, optional): Exports the JSON data into a the
        specified file.

        Returns:
            [dict]: Assets data
        """
        query_params = {
            'owner': owner,
            'token_ids': token_ids,
            'asset_contract_address': asset_contract_address,
            'asset_contract_addresses': asset_contract_addresses,
            'order_by': order_by,
            'order_direction': order_direction,
            'offset': offset,
            'limit': self.MAX_API_ITEMS if limit is None else limit,
            'collection': collection }
        return super()._make_request(query_params, export_file_name)

    __classcell__ = None


class Contract(OpenseaBase):

    def __init__(self = None, asset_contract_address = None):
        '''Endpoint to fetch data about a single asset contract.
        More info about this endpoint in the OpenSea docs:
        https://docs.opensea.io/reference/retrieving-a-single-contract

        Args:
            asset_contract_address (str)
        '''
        super().__init__(f'''asset_contract/{asset_contract_address}''', **('endpoint',))


    def fetch(self = None, export_file_name = None):
        '''Fetches asset contract data from the API.

        OpenSea API Asset Contract query parameters:
        https://docs.opensea.io/reference/retrieving-a-single-contract

        Args:
            export_file_name (str, optional): Exports the JSON data into a the
            specified file.

        Returns:
            [dict]: Single asset contract data
        '''
        return super()._make_request(None, export_file_name)

    __classcell__ = None


class Collection(OpenseaBase):

    def __init__(self = None, collection_slug = None):
        '''Endpoint to fetch data about a single asset contract.
        More info about this endpoint in the OpenSea docs:
        https://docs.opensea.io/reference/retrieving-a-single-collection

        Args:
            collection_slug (str)
        '''
        super().__init__(f'''collection/{collection_slug}''', **('endpoint',))


    def fetch(self = None, export_file_name = None):
        '''Fetches collection data from the API.

        OpenSea API Collection query parameters:
        https://docs.opensea.io/reference/retrieving-a-single-collection

        Args:
            export_file_name (str, optional): Exports the JSON data into a the
            specified file.

        Returns:
            [dict]: Single collection data
        '''
        return super()._make_request(None, export_file_name)

    __classcell__ = None


class CollectionStats(OpenseaBase):

    def __init__(self = None, collection_slug = None):
        """Endpoint to fetch a single collection's stats.
        More info about this endpoint in the OpenSea docs:
        https://docs.opensea.io/reference/retrieving-collection-stats

        Args:
            collection_slug (str)
        """
        super().__init__(f'''collection/{collection_slug}/stats''', **('endpoint',))


    def fetch(self = None, export_file_name = None):
        '''Fetches collection stats data from the API.

        OpenSea API Collection Stats query parameters:
        https://docs.opensea.io/reference/retrieving-collection-stats

        Args:
            export_file_name (str, optional): Exports the JSON data into the
            specified file.

        Returns:
            [dict]: Collection stats
        '''
        return super()._make_request(None, export_file_name)

    __classcell__ = None


class Collections(OpenseaBase):
    MAX_API_ITEMS = 300

    def __init__(self = None):
        '''Endpoint to fetch data about multiple collections.
        More info about this endpoint in the OpenSea docs:
        https://docs.opensea.io/reference/retrieving-collections
        '''
        super().__init__('collections', **('endpoint',))


    def fetch(self = None, asset_owner = None, offset = None, limit = None, export_file_name = None):
        """Fetches Collections data from the API. Function arguments will be
        passed as API query parameters,
        without modification.

        OpenSea API Collections query parameters:
        https://docs.opensea.io/reference/retrieving-collections

        There's one extra optional argument:
        export_file_name (str, optional): Exports the JSON data into a the
        specified file.

        Returns:
            [dict]: Collections data
        """
        query_params = {
            'asset_owner': asset_owner,
            'offset': offset,
            'limit': self.MAX_API_ITEMS if limit is None else limit }
        return super()._make_request(query_params, export_file_name)

    __classcell__ = None


class Bundles(OpenseaBase):
    MAX_API_ITEMS = 50

    def __init__(self = None):
        super().__init__('bundles', **('endpoint',))


    def fetch(self = None, on_sale = None, owner = None, asset_contract_address = None, asset_contract_addresses = None, token_ids = None, limit = None, export_file_name = None, offset = ((None, None, None, [], [], None, '', None),)):
        """Fetches Bundles data from the API. Function arguments will be
        passed as API query parameters,
        without modification.

        OpenSea API Bundles query parameters:
        https://docs.opensea.io/reference/retrieving-bundles

        There's one extra optional argument:
        export_file_name (str, optional): Exports the JSON data into a the
        specified file.

        Returns:
            [dict]: Bundles data
        """
        query_params = {
            'on_sale': on_sale,
            'owner': owner,
            'asset_contract_address': asset_contract_address,
            'asset_contract_addresses': asset_contract_addresses,
            'token_ids': token_ids,
            'limit': self.MAX_API_ITEMS if limit is None else limit,
            'offset': offset }
        return super()._make_request(query_params, export_file_name)

    __classcell__ = None