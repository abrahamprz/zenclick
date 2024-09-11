from tempfile import NamedTemporaryFile as tempfile_NamedTemporaryFile
from os import remove as os_remove
from apis.stirling_pdf import StirlingAPI
from apis.gesd32_inventory import GESD32InventoryAPI
from requests import Response
from logging import getLogger as logging_getLogger, info as logging_info

class GESD32Agreement:
    """
    A class that provides methods for generating device user agreements.
    
    Attributes:
        gesd32_inventory_api (GESD32InventoryAPI): An instance of the GESD32InventoryAPI class.
        stirling_api (StirlingAPI): An instance of the StirlingAPI class.
    """
    def __init__(self, gesd32_inventory_api: GESD32InventoryAPI, stirling_api: StirlingAPI) -> None:
        self.gesd32_inventory_api = gesd32_inventory_api
        self.stirling_api = stirling_api
        self.logger = logging_getLogger(__name__)
    
    def generate_device_user_agreement(self, device_tag: str, agreement_path: str, output_agreement_path: str = "") -> Response:
        """Generate a PDF of the device user agreement and return the path to the PDF file.

        Args:
            device_tag (str): tag of the device to generate the agreement for.

        Returns:
            Response: The response object from the API request.
        """
        # Load the template from templates/device_user_agreement.md
        with open(agreement_path, 'r') as file:
            template = file.read()
        
        # Get the device information from the GESD32 Inventory API and create the context for the template
        inventory_response = self.gesd32_inventory_api.get_items(asset_tag=device_tag)
        device = inventory_response['items'][0]
        
        context = {
            "device_tag": device['tag'],
            "device_name": device['name'],
            "device_price": device['purchase_price']
        }
                
        # Fill in the template with the context
        template = template.format_map(context)
        
        # Create a temporary Markdown file
        with tempfile_NamedTemporaryFile(mode='w', suffix='.md', delete=False) as tmp_file:
            tmp_file.write(template)
            tmp_file_path = tmp_file.name

        try:
            # Perform the API request to convert Markdown to PDF
            response = self.stirling_api.generate_pdf_from_md(tmp_file_path)
            # now log the content of the pdf_content variable
            if response.status_code == 200:
                return response
            else:
                raise Exception(f"Failed to generate PDF. Status code: {response.status_code}")
        finally:
            # Delete the temporary Markdown file
            os_remove(tmp_file_path)