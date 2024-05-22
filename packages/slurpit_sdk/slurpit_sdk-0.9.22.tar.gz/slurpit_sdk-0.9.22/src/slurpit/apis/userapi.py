from slurpit.apis.baseapi import BaseAPI
from slurpit.models.user import User
import pandas as pd

class UserAPI(BaseAPI):
    """
    Provides an interface for interacting with a web API to manage user resources. Inherits functionality from BaseAPI.
    
    Methods:
        get_users: Retrieves all users from the API.
        get_user: Retrieves a specific user by their ID.
        update_user: Updates a user by their ID with provided data.
        create_user: Creates a new user with the provided data.
        delete_user: Deletes a specific user by their ID.
    """

    def __init__(self, base_url, api_key):
        """
        Initializes a new instance of the UserAPI class, setting up the base URL and inheriting from BaseAPI.

        Args:
            base_url (str): The root URL for the user service API.
            api_key (str): The API key used for authorization in the API requests.
        """
        self.base_url = base_url  # Sets the base URL for API calls
        super().__init__(api_key)  # Initializes the BaseAPI with the provided API key

    def get_users(self, export_csv: bool = False, export_df: bool = False):
        """
        Fetches a list of users from the API and returns them as a list of User objects.
        Optionally exports the data to a CSV format or pandas DataFrame if specified.

        Args:
            export_csv (bool): If True, returns the user data in CSV format as bytes.
            export_df (bool): If True, returns the user data as a pandas DataFrame.

        Returns:
            list[User] | bytes | pd.DataFrame: Returns a list of User objects if successful, bytes if exporting to CSV,
                                            or a pandas DataFrame if exporting to DataFrame.
        """
        url = f"{self.base_url}/users"
        try:
            response = self.get(url)
            if response:
                users_data = response.json()
                if export_csv:
                    return self.json_to_csv_bytes(users_data)
                elif export_df:
                    return pd.DataFrame(users_data)
                else:
                    return [User(**item) for item in users_data]
        except Exception as e:
            print(f"User data error: {e}")
            raise

    def get_user(self, user_id: int):
        """
        Fetches a single user by user ID from the API.

        Args:
            user_id (int): The unique identifier of the user to retrieve.

        Returns:
            User: Returns the User object if the fetch is successful.
        """
        url = f"{self.base_url}/users/{user_id}"
        try:
            response = self.get(url)
            
            user_data = response.json()
            return User(**user_data)
        except Exception as e:
            print(f"Unexpected error: {e}")
            raise

    def update_user(self, user_id: int, update_data: dict):
        """
        Updates a user's information on the server.

        Args:
            user_id (int): The unique identifier of the user to update.
            update_data (dict): A dictionary of the data to update.

        Returns:
            User: Returns the updated User object if the update is successful.
        """
        url = f"{self.base_url}/users/{user_id}"
        try:
            response = self.put(url, update_data)
            
            user_data = response.json()
            print("User updated successfully")
            return User(**user_data)
        except Exception as e:
            print(f"Unexpected error: {e}")
            raise

    def create_user(self, new_user: dict):
        """
        Creates a new user in the system.

        Args:
            new_user (dict): A dictionary containing the data of the new user to be created.

        Returns:
            User: Returns the newly created User object if the creation is successful.
        """
        url = f"{self.base_url}/users"
        try:
            response = self.post(url, new_user)
            user_data = response.json()
            print("User created successfully")
            return User(**user_data)
        except Exception as e:
            print(f"Unexpected error: {e}")
            raise

    def delete_user(self, user_id: int):
        """
        Deletes a user from the system by user ID.

        Args:
            user_id (int): The unique identifier of the user to be deleted.

        Returns:
            User: Returns the User object if the deletion is confirmed.
        """
        url = f"{self.base_url}/users/{user_id}"
        try:
            response = self.delete(url)
            user_data = response.json()
            print("User deleted successfully")
            return User(**user_data)
        except Exception as e:
            print(f"Unexpected error: {e}")
            raise
