from smartystreets_python_sdk import StaticCredentials, exceptions, ClientBuilder
from smartystreets_python_sdk.us_extract import Lookup as ExtractLookup
import middleware.context as context

from address_services.base_address_service import BaseAddressService


class SmartyAddressService(BaseAddressService):

    def __init__(self):
        pass

    @classmethod
    def get_api_keys(cls):
        smarty_info = context.get_context("SMARTY")

        auth_id = smarty_info["auth_id"]
        auth_token = smarty_info["auth_token"]

        return auth_id, auth_token

    @classmethod
    def get_credentials(cls):
        auth_id, auth_token = cls.get_api_keys()
        credentials = StaticCredentials(auth_id, auth_token)
        return credentials

    @classmethod
    def do_lookup(cls, address_dto):
        creds = cls.get_credentials()
        client = ClientBuilder(creds).build_us_extract_api_client()
        lookup = ExtractLookup()
        lookup.text = address_dto
        lookup.aggressive = True
        lookup.addresses_have_line_breaks = False
        lookup.addresses_per_line = 1

        result = client.send(lookup)
        if result.metadata.verified_count == 0:
            return False
        return True
