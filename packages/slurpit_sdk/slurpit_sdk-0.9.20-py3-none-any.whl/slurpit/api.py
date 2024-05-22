from slurpit.apis.userapi import UserAPI  # Import UserAPI for user-related API interactions
from slurpit.apis.vaultapi import VaultAPI  # Import VaultAPI for vault-related API interactions
from slurpit.apis.platformapi import PlatformAPI  # Import PlatformAPI for platform-related API interactions
from slurpit.apis.deviceapi import DeviceAPI
from slurpit.apis.planningapi import PlanningAPI
from slurpit.apis.scannerapi import ScannerAPI
from slurpit.apis.scraperapi import ScraperAPI
from slurpit.apis.templateapi import TemplateAPI

class Api:
    def __init__(self, url, api_key=None):
        """
        Initializes a new instance of the Api class, which aggregates access to various API services.

        Args:
            url (str): The base URL for the API server.
            api_key (str, optional): The API key used for authentication with the API server. Defaults to None.

        Attributes:
            base_url (str): The full base URL for the API including the '/api' endpoint suffix.
            token (str): The API key used for authenticating requests.
            users (UserAPI): An instance of UserAPI initialized with the base URL and API key.
            vault (VaultAPI): An instance of VaultAPI initialized with the base URL and API key.
            platform (PlatformAPI): An instance of PlatformAPI initialized with the base URL and API key.
        """
        base_url = "{}/api".format(url if url[-1] != "/" else url[:-1])  # Format the base URL to ensure it ends with '/api'
        self.base_url = base_url  # Set the formatted base URL
        self.token = api_key  # Store the API key
        self.users = UserAPI(base_url, api_key)  # Initialize the UserAPI with the base URL and API key
        self.vault = VaultAPI(base_url, api_key)  # Initialize the VaultAPI with the base URL and API key
        self.platform = PlatformAPI(base_url, api_key)  # Initialize the PlatformAPI with the base URL and API key
        self.device = DeviceAPI(base_url, api_key)
        self.planning = PlanningAPI(base_url, api_key)
        self.scanner = ScannerAPI(base_url, api_key)
        self.scraper = ScraperAPI(base_url, api_key)
        self.templates = TemplateAPI(base_url, api_key)
        