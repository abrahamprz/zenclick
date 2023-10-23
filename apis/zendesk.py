from requests import get
from base64 import b64encode


class ZendeskAPI:
    
    def __init__(self, api_key: str, subdomain: str, email:str) -> None:
        """Initializes the API client.

        Args:
            api_key (str): The API key for the Zendesk account.
            subdomain (str): The subdomain of the Zendesk account.
            email (str): The email address associated with the Zendesk account.
        """
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
        """_summary_

        https://developer.zendesk.com/api-reference/ticketing/business-rules/views/#list-active-views
        
        Returns:
            dict: _description_
        """
        url = f"{self.base_url}/views/active.json"
        response = get(url, headers=self.headers)
        return response.json()


    def get_tickets_in_view(self, view_id: str) -> dict:
        """_summary_

        https://developer.zendesk.com/api-reference/ticketing/business-rules/views/#list-tickets-from-a-view
        
        Args:
            view_id (str): _description_

        Returns:
            dict: _description_
        """
        url = f"{self.base_url}/views/{view_id}/tickets.json"
        response = get(url, headers=self.headers)
        return response.json()
