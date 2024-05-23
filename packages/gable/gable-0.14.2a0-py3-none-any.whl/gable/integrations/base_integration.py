from gable.client import GableClient


class BaseDataAssetIntegration:
    """
    This is the base class for all data asset integrations. It provides a common
    interface for interacting with integration-specific data assets.

    Subclasses must implement the following methods:
    - register: Registers the data asset
    - check: Checks the data asset against a data contract (if it exists)
    - check_and_register (combo of the above two methods)
    """

    client: GableClient

    def __init__(self, client: GableClient):
        self.client = client

    def register(self):
        raise NotImplementedError("register method must be implemented by subclass")

    def check(self):
        raise NotImplementedError("check method must be implemented by subclass")

    def check_and_register(self):
        raise NotImplementedError(
            "check_and_register method must be implemented by subclass"
        )
