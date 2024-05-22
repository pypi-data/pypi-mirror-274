from definite_sdk.integration import DefiniteIntegrationStore
from definite_sdk.secret import DefiniteSecretStore
from definite_sdk.store import DefiniteKVStore

API_URL = "https://api.definite.app"


class DefiniteClient:
    """Client for interacting with the Definite API."""

    def __init__(self, api_key: str, api_url: str = API_URL):
        """Creates a definite client with the provided API key.

        See: https://docs.definite.app/definite-api for how to obtain an API key.
        """
        self.api_key = api_key
        self.api_url = api_url

    def get_kv_store(self, name: str) -> DefiniteKVStore:
        """Initializes a key-value store with the provided name.

        See DefiniteKVStore for more how to interact with the store.
        """

        return DefiniteKVStore(name, self.api_key, self.api_url)

    def get_secret_store(self) -> DefiniteSecretStore:
        """Initializes the secret store.

        See DefiniteSecretStore for more how to interact with the store.
        """

        return DefiniteSecretStore(self.api_key, self.api_url)

    def get_integration_store(self) -> DefiniteIntegrationStore:
        """Initializes the integration store.

        See DefiniteIntegrationStore for more how to interact with the store.
        """

        return DefiniteIntegrationStore(self.api_key, self.api_url)
