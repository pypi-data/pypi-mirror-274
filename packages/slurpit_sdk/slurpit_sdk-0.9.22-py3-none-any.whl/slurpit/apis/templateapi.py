from slurpit.apis.baseapi import BaseAPI
from slurpit.models.template import Template
import pandas as pd


class TemplateAPI(BaseAPI):
    """
    Provides an interface for interacting with a web API to manage template resources. Inherits functionality from BaseAPI.
    
    Methods:
        get_all_templates: Retrieves all templates from the API.
        get_template: Retrieves a specific template by its ID.
        update_template: Updates a template by its ID with provided data.
        delete_template: Deletes a specific template by its ID.
        create_template: Creates a new template with the provided data.
        search_template: Searches for templates based on specified criteria.
        run_template: Executes a template with the provided information.
        validate_textfsm: Validates a TextFSM template format.
        test_textfsm: Tests a TextFSM template with provided data.
    """
    
    def __init__(self, base_url, api_key):
        """
        Initializes a new instance of the TemplateAPI class with the specified API key and base URL.
        
        Args:
            base_url (str): The root URL for the API endpoints.
            api_key (str): The API key used for authenticating requests.
        """
        self.base_url = base_url
        super().__init__(api_key)

    def get_templates(self, export_csv: bool = False, export_df: bool = False):
        """
        Fetches all templates from the API and returns them as instances of the Template model. Optionally exports the data to a CSV format or pandas DataFrame if specified.

        Args:
            export_csv (bool): If True, returns the template data in CSV format as bytes.
            export_df (bool): If True, returns the template data as a pandas DataFrame.

        Returns:
            list[Template] | bytes | pd.DataFrame: A list of Template instances if successful, bytes if exporting to CSV,
                                                or a pandas DataFrame if exporting to DataFrame.
        """
        url = f"{self.base_url}/templates"
        try:
            response = self.get(url)
            if response:
                templates_data = response.json()
                if export_csv:
                    return self.json_to_csv_bytes(templates_data)
                elif export_df:
                    return pd.DataFrame(templates_data)
                else:
                    return [Template(**item) for item in templates_data]
        except Exception as e:
            print(f"Unexpected error: {e}")
            raise

    def get_template(self, template_id: int):
        """
        Fetches a template by its ID from the API and returns it as an instance of the Template model.
        
        Args:
            template_id (int): The ID of the template to retrieve.
        
        Returns:
            Template: A Template instance if successful.
        """
        url = f"{self.base_url}/templates/{template_id}"
        try:
            response = self.get(url)
            
            return Template(**response.json())
        except Exception as e:
            print(f"Unexpected error: {e}")
            raise

    def update_template(self, template_id: int, update_data: dict):
        """
        Updates a template by its ID with the provided data.
        
        Args:
            template_id (int): The ID of the template to update.
            update_data (dict): A dictionary of updates to apply to the template.
        
        Returns:
            Template: An updated Template instance if successful.
        """
        url = f"{self.base_url}/templates/{template_id}"
        try:
            response = self.put(url, update_data)
            
            return Template(**response.json())
        except Exception as e:
            print(f"Unexpected error: {e}")
            raise

    def delete_template(self, template_id: int):
        """
        Deletes a template by its ID.
        
        Args:
            template_id (int): The ID of the template to delete.
        
        Returns:
            Template: A Template instance representing the deleted template if successful.
        """
        url = f"{self.base_url}/templates/{template_id}"
        try:
            response = self.delete(url)
            
            return Template(**response.json())
        except Exception as e:
            print(f"Unexpected error: {e}")
            raise

    def create_template(self, new_template: dict):
        """
        Creates a new template with the provided data.
        
        Args:
            new_template (dict): A dictionary representing the new template to create.
        
        Returns:
            Template: A new Template instance if successful.
        """
        url = f"{self.base_url}/templates"
        try:
            response = self.post(url, new_template)
            
            return Template(**response.json())
        except Exception as e:
            print(f"Unexpected error: {e}")
            raise

    
    def search_template(self, search_data: dict, export_csv: bool = False, export_df: bool = False):
        """
        Searches for templates based on the provided search criteria and optionally exports the data to a CSV format or pandas DataFrame.
        
        Args:
            search_data (dict): A dictionary containing search parameters.
            export_csv (bool): If True, returns the search results in CSV format as bytes.
            export_df (bool): If True, returns the search results as a pandas DataFrame.

        Returns:
            list[Template] | bytes | pd.DataFrame: A list of Template instances matching the search criteria if successful,
                                                bytes if exporting to CSV, or a pandas DataFrame if exporting to DataFrame.
        """
        url = f"{self.base_url}/templates/search"
        try:
            response = self.post(url, search_data)
            if response:
                templates_data = response.json()
                if export_csv:
                    return self.json_to_csv_bytes(templates_data)
                elif export_df:
                    return pd.DataFrame(templates_data)
                else:
                    return [Template(**item) for item in templates_data]
        except Exception as e:
            print(f"Unexpected error: {e}")
            raise

    def run_template(self, run_info: dict):
        """
        Get realtime parsed and raw results from a device.

        Args:
            run_info (dict): A dictionary containing the information necessary to run the template.
        
        Returns:
            dict: The result of running the template if successful.
        """
        url = f"{self.base_url}/templates/run"
        try:
            response = self.post(url, run_info)
            
            return response.json()
        except Exception as e:
            print(f"Unexpected error: {e}")
            raise

    def validate_textfsm(self, textfsm: str):
        """
        Validates if the textFSM has validation/syntax errors.

        Args:
            textfsm (str): The TextFSM template string to validate.
        
        Returns:
            dict: The validation result if successful.
        """
        request_data = {"textfsm": textfsm}
        url = f"{self.base_url}/templates/validate"
        try:
            response = self.post(url, request_data)
            
            return response.json()
        except Exception as e:
            print(f"Unexpected error: {e}")
            raise

    def test_textfsm(self, test_data: dict):
        """
        Tests the TextFSM template against a device.
        
        Args:
            test_data (dict): A dictionary containing the test data to evaluate against the TextFSM template.
        
        Returns:
            dict: The test result if successful.
        """
        url = f"{self.base_url}/templates/test"
        try:
            response = self.post(url, test_data)
            
            return response.json()
        except Exception as e:
            print(f"Unexpected error: {e}")
            raise
