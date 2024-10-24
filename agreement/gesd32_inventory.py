from requests import get
from django.conf import settings

class GESD32InventoryAPI:
    """
    A class that provides methods for interacting with the GESD32 Inventory API.
    """
    
    def __init__(self):
        self.base_url = settings.GESD32_INVENTORY_API_BASE_URL
        self.headers = {
            "Authorization": f"Token {settings.GESD32_INVENTORY_API_TOKEN}",
        }

    def manage_pagination(self, initial_url: str, headers: dict, params: dict) -> dict:
        """
        Handles pagination for API requests.

        Args:
            initial_url (str): The initial URL to make the request to.
            headers (dict): The headers to include in the request.
            params (dict): The parameters to include in the request.

        Returns:
            dict: A dictionary containing the count of items and a list of items across all pages.
        """
        items = []  # List to store items across all pages
        url = initial_url  # Start with the initial URL

        while url:  # Loop until there is no next page
            response = get(url, headers=headers, params=params)
            try:
                response.raise_for_status()  # Check for HTTP request errors
                data = response.json()  # Parse the JSON response
                count = data['count']  # Get the total count of items
                items.extend(data['results'])  # Add the items from the current page to the list
                url = data.get('next')  # Get the URL for the next page
            except Exception as e:
                print(f"An error occurred: {e}")
                break  # Exit the loop if an error occurs

        return {"count": count, "items": items}  # Return the list of items
    
    # Schools API calls
    # ------------------------------
    def get_schools(self, short_name: str = "", name: str = "") -> dict:
        """
        Get all schools in the account.
        
        Args:
            short_name (str, optional): The short name of the school. It is usually the initials of the school's name.
            name (str, optional): The complete name of the school.

        Returns:
            dict: A dictionary containing all schools in the account.
        """
        params = {
            "short_name": short_name,
            "name": name
        }
        url = self.base_url + 'schools'
        return self.manage_pagination(url, headers=self.headers, params=params)
    
    def get_school(self, school_id: int) -> dict:
        """
        Get the information for a specific school from the GESD32 Inventory API.

        Args:
            school_id (str): The ID (label as PK) of the school to retrieve information for.

        Returns:
            dict: A dictionary containing the information for the school.
        """
        url = self.base_url + f'schools/{school_id}'
        response = get(url, headers=self.headers)
        
        try:
            response.raise_for_status()
        except Exception as e:
            print(f"An error occurred: {e}")
        
        return response.json()
    
    # Rooms API calls
    # ------------------------------
    def get_rooms(self, name: str = "", school: str = "") -> dict:
        """
        Get all rooms in the account.
        
        Args:
            name (str, optional): The name of the room.
            school (str, optional): The school's PK where the room is located.

        Returns:
            dict: A dictionary containing all rooms in the account.
        """
        params = {
            "name": name,
            "school": school
        }
        url = self.base_url + 'rooms'
        return self.manage_pagination(url, headers=self.headers, params=params)
    
    def get_room(self, room_id: int) -> dict:
        """
        Get the information for a specific room from the GESD32 Inventory API.

        Args:
            room_id (str): The ID (label as PK) of the room to retrieve information for.

        Returns:
            dict: A dictionary containing the information for the room.
        """
        url = self.base_url + f'rooms/{room_id}'
        response = get(url, headers=self.headers)
        
        try:
            response.raise_for_status()
        except Exception as e:
            print(f"An error occurred: {e}")
        
        return response.json()
    
    
    # Items API calls
    # ------------------------------
    def get_items(self, asset_tag: str = "", name: str = "", serial_number: str = "", item_template__brand: str = "", current_location: str = "", current_location__school: str = "") -> dict:
        """
        Get all items in the account.
        
        Args:
            asset_tag (str, optional): Also known as item tag or tag number. The asset tag of the item.
            name (str, optional): The name of the item.
            serial_number (str, optional): The serial number of the item. 
            item_template__brand (str, optional): The brand of the item. Example: "DELL"
            current_location (str, optional): The current location's PK of the item.
            current_location__school (str, optional): The school's PK where the item is located.

        Returns:
            dict: A dictionary containing all items in the account.
        """
        params = {
            "asset_tag": asset_tag,
            "name": name,
            "serial_number": serial_number,
            "item_template__brand": item_template__brand,
            "current_location": current_location,
            "current_location__school": current_location__school
        }
        url = self.base_url + 'items'
        return self.manage_pagination(url, headers=self.headers, params=params)
    
    def get_item(self, item_id: int) -> dict:
        """
        Get the information for a specific item from the GESD32 Inventory API.

        Args:
            item_id (str): The ID (label as PK) of the item to retrieve information for.

        Returns:
            dict: A dictionary containing the information for the item.
        """
        url = self.base_url + f'items/{item_id}'
        response = get(url, headers=self.headers)
        
        try:
            response.raise_for_status()
        except Exception as e:
            print(f"An error occurred: {e}")
        
        return response.json()
    
    # Persons API calls
    # ------------------------------
    def get_persons(self, e_id: str = "", first_name: str = "", last_name: str = "", email_address: str = "") -> dict:
        """
        Get all persons in the account.

        Args:
            e_id (str, optional): The employee ID of the person.
            first_name (str, optional): The first name of the person.
            last_name (str, optional): The last name of the person.
            email_address (str, optional): The email address of the person. The user's username is located before the '@' symbol.

        Returns:
            dict: A dictionary containing all persons in the account.
        """
        params = {
            "e_id": e_id,
            "first_name": first_name,
            "last_name": last_name,
            "email_address": email_address
        }
        url = self.base_url + 'persons'
        return self.manage_pagination(url, headers=self.headers, params=params)
    
    def get_person(self, person_id: int) -> dict:
        """
        Get the information for a specific person from the GESD32 Inventory API.

        Args:
            person_id (str): The ID (label as PK) of the person to retrieve information for.

        Returns:
            dict: A dictionary containing the information for the person.
        """
        url = self.base_url + f'persons/{person_id}'
        response = get(url, headers=self.headers)
        
        try:
            response.raise_for_status()
        except Exception as e:
            print(f"An error occurred: {e}")
        
        return response.json()
    
    # Purchase Orders API calls
    # ------------------------------
    def get_pos(self, po_number: str = "") -> dict:
        """
        Get all purchase orders in the account.
        
        Args:
            po_number (str, optional): The purchase order number.

        Returns:
            dict: A dictionary containing all purchase orders in the account.
        """
        params = {
            "po_number": po_number
        }
        url = self.base_url + 'po'
        return self.manage_pagination(url, headers=self.headers, params=params)
    
    def get_po(self, po_id: int) -> dict:
        """
        Get the information for a specific purchase order from the GESD32 Inventory API.

        Args:
            po_id (str): The ID (label as PK) of the purchase order to retrieve information for.

        Returns:
            dict: A dictionary containing the information for the purchase order.
        """
        url = self.base_url + f'po/{po_id}'
        response = get(url, headers=self.headers)
        
        try:
            response.raise_for_status()
        except Exception as e:
            print(f"An error occurred: {e}")
        
        return response.json()