from io import BytesIO
from agreement.stirling_pdf import StirlingAPI
from agreement.gesd32_inventory import GESD32InventoryAPI
from requests import Response
from logging import getLogger as logging_getLogger, warning, error

class GESD32Agreement:
    def __init__(self, gesd32_inventory_api: GESD32InventoryAPI, stirling_api: StirlingAPI):
        self.gesd32_inventory_api = gesd32_inventory_api
        self.stirling_api = stirling_api
        self.logger = logging_getLogger(__name__)

    def _generate_document(self, template_path: str, device_tag: str) -> Response:
        """Generate a PDF document from a Markdown template.

        Args:
            template_path (str): The path to the Markdown template.
            device_tag (str): The asset tag of the device.

        Returns:
            Response: The response from the Stirling API.
        """
        try:
            # Load the template
            with open(template_path, 'r') as file:
                template = file.read()

            # Get the device information from the GESD32 Inventory API
            inventory_response = self.gesd32_inventory_api.get_items(asset_tag=device_tag)
            
            if not inventory_response['items']:
                raise ValueError(f"No device found with tag {device_tag}")
            
            device = inventory_response['items'][0]

            context = {
                "device_tag": device['tag'],
                "device_name": device['name'],
                "device_price": device['purchase_price']
            }

            # Fill in the template with the context
            template = template.format_map(context)
            
            # Create a byte stream from the file content
            file_stream = BytesIO(template.encode())
            
            return self.stirling_api.generate_pdf_from_md(file_stream)
        except ValueError as ve:
            warning(f"Validation error: {ve}")
            raise
        except Exception as e:
            error(f"An error occurred while generating the agreement: {e}")
            raise

    def generate_device_user_agreement(self, device_tag: str) -> Response:
        """Generate a device user agreement for a device with the given tag.

        Args:
            device_tag (str): The asset tag of the device.

        Returns:
            Response: The response from the Stirling API.
        """
        return self._generate_document('agreement/templates/device_user_agreement.md', device_tag)

    def generate_device_return_receipt(self, device_tag: str) -> Response:
        """Generate a device return receipt for a device with the given tag.

        Args:
            device_tag (str): The asset tag of the device.

        Returns:
            Response: The response from the Stirling API.
        """
        return self._generate_document('agreement/templates/device_return_receipt.md', device_tag)