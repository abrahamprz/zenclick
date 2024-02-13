from base64 import b64encode

from requests import get

from time import sleep as time_sleep
from json import dumps as json_dumps

class ZendeskAPI:
    """A class for interacting with the Zendesk API.

    Args:
        api_key (str): The API key for the Zendesk account.
        subdomain (str): The subdomain of the Zendesk account.
        email (str): The email address associated with the Zendesk account.
    """

    def __init__(self, api_key: str, subdomain: str, email: str) -> None:
        """Initializes the API client."""
        self.api_key = api_key
        self.email = email
        self.base_url = f"https://{subdomain}.zendesk.com/api/v2"
        self.headers = {
            "Authorization": f"Basic {self._get_encoded_auth_string()}",
            "Content-Type": "application/json",
        }

    def _get_encoded_auth_string(self) -> str:
        """Returns the encoded authentication string for the API client.

        Returns:
            str: The encoded authentication string.
        """
        auth_string = f"{self.email}/token:{self.api_key}"
        return b64encode(auth_string.encode()).decode()

    def get_active_views(self) -> dict:
        """Returns a list of active views.

        Returns:
            dict: A dictionary containing the list of active views.
        """
        url = f"{self.base_url}/views/active.json"
        response = get(url, headers=self.headers)
        return response.json()

    def get_tickets_in_view(self, view_id: str) -> dict:
        """Returns a list of tickets in the specified view.

        Args:
            view_id (str): The ID of the view.

        Returns:
            dict: A dictionary containing the list of tickets in the view.
        """
        url = f"{self.base_url}/views/{view_id}/tickets.json"
        tickets = []

        while url:
            response = get(url, headers=self.headers)
            data = response.json()

            # Add the tickets from this page to our list
            tickets.extend(data['tickets'])

            # Get the next page URL, if it exists
            url = data['next_page']

            # To avoid hitting the rate limit, pause for a second before the next request
            time_sleep(1)
            
        return {'tickets': tickets}

    def get_ticket_fields(self) -> dict:
        """Returns a list of ticket fields.

        Returns:
            dict: A dictionary containing the list of ticket fields.
        """
        url = f"{self.base_url}/ticket_fields.json"
        response = get(url, headers=self.headers)
        return response.json()

    def get_user(self, user_id: str) -> dict:
        """Returns the user with the specified ID.

        Args:
            user_id (str): The ID of the user.

        Returns:
            dict: A dictionary containing the user information.
        """
        url = f"{self.base_url}/users/{user_id}.json"
        response = get(url, headers=self.headers)
        return response.json()
