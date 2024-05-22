from slurpit.apis.baseapi import BaseAPI
from slurpit.models.scanner import Node
import pandas as pd

class ScannerAPI(BaseAPI):
    def __init__(self, base_url, api_key):
        """
        Initialize the ScannerAPI with the base URL of the API and an API key for authentication.
        
        Args:
            base_url (str): The root URL for the API endpoints.
            api_key (str): The API key used for authenticating requests.
        """
        self.base_url = base_url  # API base URL
        super().__init__(api_key)  # Initialize the parent class with the API key

    def get_nodes(self, batch_id: int, offset: int = 0, limit: int = 1000, export_csv: bool = False, export_df: bool = False):
        """
        Retrieves a list of nodes based on the batch_id with pagination options and optionally exports the data to CSV format or pandas DataFrame.

        Args:
            batch_id (int): The batch identifier to filter nodes.
            offset (int): The starting index for pagination.
            limit (int): The maximum number of nodes to return.
            export_csv (bool): If True, returns the nodes data in CSV format as bytes.
            export_df (bool): If True, returns the nodes data as a pandas DataFrame.

        Returns:
            list[dict] | bytes | pd.DataFrame: A list of nodes, CSV data as bytes if export_csv is True, 
                                            or a pandas DataFrame if export_df is True.
        """
        url = f"{self.base_url}/scanner/{batch_id}"
        params = {'offset': offset, 'limit': limit}
        try:
            response = self.get(url, params=params)
            if response:
                nodes_data = response.json()
                if export_csv:
                    return self.json_to_csv_bytes(nodes_data)
                elif export_df:
                    return pd.DataFrame(nodes_data)
                else:
                    return nodes_data
        except Exception as e:
            print(f"Unexpected error: {e}")
            raise

    def get_finders(self, export_csv: bool = False, export_df: bool = False):
        """
        Retrieves a list of configured finders from the scanner API and optionally exports the data to CSV format or pandas DataFrame.

        Args:
            export_csv (bool): If True, returns the finders data in CSV format as bytes.
            export_df (bool): If True, returns the finders data as a pandas DataFrame.

        Returns:
            list[dict] | bytes | pd.DataFrame: A list of finders, CSV data as bytes if export_csv is True,
                                            or a pandas DataFrame if export_df is True.
        """
        url = f"{self.base_url}/scanner/configured/finders"
        try:
            response = self.get(url)
            if response:
                finders_data = response.json()
                if export_csv:
                    return self.json_to_csv_bytes(finders_data)
                elif export_df:
                    return pd.DataFrame(finders_data)
                else:
                    return finders_data
        except Exception as e:
            print(f"Unexpected error: {e}")
            raise

    def get_crawlers(self, export_csv: bool = False, export_df: bool = False):
        """
        Retrieves a list of configured crawlers from the scanner API and optionally exports the data to CSV format or pandas DataFrame.

        Args:
            export_csv (bool): If True, returns the crawlers data in CSV format as bytes.
            export_df (bool): If True, returns the crawlers data as a pandas DataFrame.

        Returns:
            list[dict] | bytes | pd.DataFrame: A list of crawlers, CSV data as bytes if export_csv is True,
                                            or a pandas DataFrame if export_df is True.
        """
        url = f"{self.base_url}/scanner/configured/crawlers"
        try:
            response = self.get(url)
            if response:
                crawlers_data = response.json()
                if export_csv:
                    return self.json_to_csv_bytes(crawlers_data)
                elif export_df:
                    return pd.DataFrame(crawlers_data)
                else:
                    return crawlers_data
        except Exception as e:
            print(f"Unexpected error: {e}")
            raise

    def start_scanner(self, scanner_data: dict):
        """
        Starts a scanning process with provided scanner configuration data.

        Returns:
            dict: Status of the scanning process if successful.
        """
        url = f"{self.base_url}/scanner"
        try:
            response = self.post(url, scanner_data)
            if response:
                scanner_status = response.json()
                return scanner_status
        except Exception as e:
            print(f"Unexpected error: {e}")
            raise

    def clean_logging(self, datetime: str):
        """
        Triggers a cleaning process for scanner logs older than the specified datetime.

        Returns:
            dict: Result of the cleaning process if successful.
        """
        url = f"{self.base_url}/scanner/clean"
        request_data = {"datetime": datetime}
        try:
            response = self.post(url, request_data)
            if response:
                clean_result = response.json()
                return clean_result
        except Exception as e:
            print(f"Unexpected error: {e}")
            raise

    def get_status(self):
        """
        Retrieves the current status of the scanner.

        Returns:
            dict: The current status of the scanner if successful.
        """
        url = f"{self.base_url}/scanner/status"
        try:
            response = self.get(url)
            if response:
                status_result = response.json()
                return status_result
        except Exception as e:
            print(f"Unexpected error: {e}")
            raise

    def test_snmp(self, ip_data: dict):
        """
        Tests SNMP configuration by attempting to gather device information from the specified IP.

        Returns:
            dict: Device information gathered via SNMP if successful.
        """
        url = f"{self.base_url}/scanner/test"
        try:
            response = self.post(url, ip_data)
            if response:
                device_info = response.json()
                return device_info
        except Exception as e:
            print(f"Unexpected error: {e}")
            raise

    def get_queue_list(self, export_csv: bool = False):
        """
        Gives a list of currently queued tasks for the scanner.

        Args:
            export_csv (bool): If True, returns the queued tasks data in CSV format as bytes. If False, returns list of queued tasks.

        Returns:
            list[dict] | bytes: A list of queued tasks or CSV data as bytes if export_csv is True.
        """
        url = f"{self.base_url}/scanner/queue/list"
        try:
            response = self.post(url, None)
            if response:
                queue_list = response.json()
                if export_csv:
                    return self.json_to_csv_bytes(queue_list)
                else:
                    return queue_list
        except Exception as e:
            print(f"Unexpected error: {e}")
            raise
    
    def clear_queue(self):
        """
        Clears the queue of the scanner by sending a DELETE request to the queue list endpoint.

        Returns:
            dict: The result of clearing the queue if successful.
        """
        url = f"{self.base_url}/scanner/queue/clear"
        
        try:
            response = self.delete(url)
            
            if response:
                clear_result = response.json()
                return clear_result
        except Exception as e:
            print(f"Unexpected error: {e}")
            raise
