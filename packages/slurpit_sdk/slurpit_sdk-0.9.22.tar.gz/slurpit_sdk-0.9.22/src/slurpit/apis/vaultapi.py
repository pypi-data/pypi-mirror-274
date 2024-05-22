from slurpit.apis.baseapi import BaseAPI
from slurpit.models.vault import Vault, SingleVault
import pandas as pd

class VaultAPI(BaseAPI):
    def __init__(self, base_url, api_key):
        """
        Initializes a new instance of the VaultAPI class.

        Args:
            base_url (str): The base URL for the Vault API.
            api_key (str): The API key used for authentication.
        """
        self.base_url = base_url  # Sets the base URL for API calls
        super().__init__(api_key)  # Initializes the BaseAPI with the provided API key

    def get_vaults(self, export_csv: bool = False, export_df: bool = False):
        """
        Fetches a list of all vaults from the API and returns them as a list of Vault objects.
        Optionally exports the data to a CSV format or pandas DataFrame if specified.

        Args:
            export_csv (bool): If True, returns the vault data in CSV format as bytes.
            export_df (bool): If True, returns the vault data as a pandas DataFrame.

        Returns:
            list[Vault] | bytes | pd.DataFrame: Returns a list of Vault objects if successful, bytes if exporting to CSV,
                                            or a pandas DataFrame if exporting to DataFrame.
        """
        url = f"{self.base_url}/vault"
        try:
            response = self.get(url)
            if response:
                vaults_data = response.json()
                if export_csv:
                    return self.json_to_csv_bytes(vaults_data)
                elif export_df:
                    return pd.DataFrame(vaults_data)
                else:
                    return [Vault(**item) for item in vaults_data]
        except Exception as e:
            print(f"Unexpected error: {e}")
            raise
        
    def get_vault(self, vault_id: int):
        """
        Fetches a single vault by its ID.

        Args:
            vault_id (int): The ID of the vault to retrieve.

        Returns:
            SingleVault: Returns a SingleVault object if the fetch is successful.
        """
        url = f"{self.base_url}/vault/{vault_id}"
        try:
            response = self.get(url)
            if response:
                vault_data = response.json()
                return SingleVault(**vault_data)
        except Exception as e:
            print(f"Unexpected error: {e}")
            raise
    
    def update_vault(self, vault_id: int, update_data: dict):
        """
        Updates a vault with specified data.

        Args:
            vault_id (int): The ID of the vault to update.
            update_data (dict): The data to update in the vault.

        Returns:
            SingleVault: Returns a SingleVault object if the update is successful.
        """
        url = f"{self.base_url}/vault/{vault_id}"
        try:
            response = self.put(url, update_data)
            if response:
                vault_data = response.json()
                print("vault_data", vault_data)
                return SingleVault(**vault_data)
        except Exception as e:
            print(f"Unexpected error: {e}")
            raise
    
    def create_vault(self, new_vault: dict):
        """
        Creates a new vault with the specified data.

        Args:
            new_vault (dict): The data for the new vault.

        Returns:
            SingleVault: Returns a SingleVault object if the creation is successful.
        """
        url = f"{self.base_url}/vault"
        try:
            response = self.post(url, new_vault)
            if response:
                vault_data = response.json()
                print("new data", vault_data)
                return SingleVault(**vault_data)
        except Exception as e:
            print(f"Unexpected error: {e}")
            raise
    
    def delete_vault(self, vault_id: int):
        """
        Deletes a vault by its ID.

        Args:
            vault_id (int): The ID of the vault to delete.

        Returns:
            SingleVault: Returns a SingleVault object if the deletion is successful.
        """
        url = f"{self.base_url}/vault/{vault_id}"
        try:
            response = self.delete(url)
            if response:
                vault_data = response.json()
                print("new data", vault_data)
                return SingleVault(**vault_data)
        except Exception as e:
            print(f"Unexpected error: {e}")
            raise
