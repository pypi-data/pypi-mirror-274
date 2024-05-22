import requests
import pandas as pd
from io import BytesIO
import os
class BaseAPI:
    def __init__(self, api_key):
        """
        Initializes a new instance of the BaseAPI class.

        Args:
            api_key (str): The API key used for authorization which will be included in the headers
                           of all requests made using this session.
        """
        self.session = requests.Session()  # Creates a session to persist certain parameters across requests
        self.session.headers.update({
            'Authorization': f'Bearer {api_key}',  # Authentication header with Bearer token
            'Content-Type': 'application/json'     # Sets default content type to JSON for all requests
        })
    
    def get(self, url, **kwargs):
        """
        Sends a GET request to the specified URL.

        Args:
            url (str): The URL to send the GET request to.
            **kwargs: Arbitrary keyword arguments that are forwarded to the `requests.get` method.

        Returns:
            requests.Response: The response object if the request was successful.

        Raises:
            requests.exceptions.Timeout: If the request timed out.
            requests.exceptions.ConnectionError: If there was a network problem.
            requests.exceptions.HTTPError: If the HTTP request returned an error response.
            requests.exceptions.RequestException: If there was an ambiguous exception that occurred while handling your request.
        """
        try:
            response = self.session.get(url, **kwargs)  # Sends a GET request
            response.raise_for_status()  # Raises an exception for HTTP error codes
            return response
        except requests.exceptions.Timeout:
            print("The request timed out")
            raise
        except requests.exceptions.ConnectionError:
            print("Network problem (e.g., DNS failure, refused connection, etc)")
            raise
        except requests.exceptions.HTTPError as e:
            error_message = e.response.json().get('messages', {}).get('error', 'No error message provided')
            print(f"HTTP Error: {e}")
            print(f"Error Message: {error_message}")
            raise
        except requests.exceptions.RequestException as e:
            print(f"Request Error: {e}")
            raise
    
    def post(self, url, data, **kwargs):
        """
        Sends a POST request with JSON data to the specified URL.

        Args:
            url (str): The URL to send the POST request to.
            data (dict): The JSON data to send in the body of the POST request.
            **kwargs: Arbitrary keyword arguments that are forwarded to the `requests.post` method.

        Returns:
            requests.Response | None: The response object if the request was successful; otherwise, None.
        """
        try:
            response = self.session.post(url, json=data, **kwargs)  # Sends a POST request with JSON payload
            response.raise_for_status()
            return response
        except requests.exceptions.Timeout:
            print("The request timed out")
            raise
        except requests.exceptions.ConnectionError:
            print("Network problem (e.g., DNS failure, refused connection, etc)")
            raise
        except requests.exceptions.HTTPError as e:
            error_message = e.response.json().get('messages', {}).get('error', 'No error message provided')
            print(f"HTTP Error: {e}")
            print(f"Error Message: {error_message}")
            raise
        except requests.exceptions.RequestException as e:
            print(f"Request Error: {e}")
            raise

    
    def put(self, url, data, **kwargs):
        """
        Sends a PUT request with JSON data to the specified URL.

        Args:
            url (str): The URL to send the PUT request to.
            data (dict): The JSON data to send in the body of the PUT request.
            **kwargs: Arbitrary keyword arguments that are forwarded to the `requests.put` method.

        Returns:
            requests.Response | None: The response object if the request was successful; otherwise, None.
        """
        try:
            response = self.session.put(url, json=data, **kwargs)
            response.raise_for_status()
            return response
        except requests.exceptions.Timeout:
            print("The request timed out")
            raise
        except requests.exceptions.ConnectionError:
            print("Network problem (e.g., DNS failure, refused connection, etc)")
            raise
        except requests.exceptions.HTTPError as e:
            error_message = e.response.json().get('messages', {}).get('error', 'No error message provided')
            print(f"HTTP Error: {e}")
            print(f"Error Message: {error_message}")
            raise
        except requests.exceptions.RequestException as e:
            print(f"Request Error: {e}")
            raise
    
    def delete(self, url, **kwargs):
        """
        Sends a DELETE request to the specified URL.

        Args:
            url (str): The URL to send the DELETE request to.
            **kwargs: Arbitrary keyword arguments that are forwarded to the `requests.delete` method.

        Returns:
            requests.Response | None: The response object if the request was successful; otherwise, None.
        """
        try:
            response = self.session.delete(url, **kwargs)
            response.raise_for_status()
            return response
        except requests.exceptions.Timeout:
            print("The request timed out")
            raise
        except requests.exceptions.ConnectionError:
            print("Network problem (e.g., DNS failure, refused connection, etc)")
            raise
        except requests.exceptions.HTTPError as e:
            error_message = e.response.json().get('messages', {}).get('error', 'No error message provided')
            print(f"HTTP Error: {e}")
            print(f"Error Message: {error_message}")
            raise
        except requests.exceptions.RequestException as e:
            print(f"Request Error: {e}")
            raise


    def json_to_csv_bytes(self, json_data):
        """
        Converts JSON data to CSV byte array.

        Args:
            json_data (list[dict]): A list of dictionaries representing JSON data.

        Returns:
            bytes: CSV formatted data as a byte array.
        """

        try:
            # Convert JSON to DataFrame
            df = pd.DataFrame(json_data)
            
            # Create a buffer
            buffer = BytesIO()
            
            # Convert DataFrame to CSV and save it to buffer
            df.to_csv(buffer, index=False)
            buffer.seek(0)  # Rewind the buffer to the beginning
            
            # Return bytes
            return buffer.getvalue()
        except Exception as e:
            print(f"Data error while converting CSV file: {e}")
            raise
        
    
    def save_csv_bytes(self, byte_data, filename):
        """
        Saves CSV byte array data to a CSV file.

        Args:
            byte_data (bytes): CSV data in byte array format.
            filename (str): The filename to save the CSV file as.
        """
        try:
            directory = os.path.dirname(filename)
            if not os.path.exists(directory):
                os.makedirs(directory)
                
            # Open file in binary write mode and write byte data
            with open(filename, 'wb') as file:
                file.write(byte_data)
            return True
        except Exception as e:
            print(f"Data error while saving CSV file: {e}")
            raise