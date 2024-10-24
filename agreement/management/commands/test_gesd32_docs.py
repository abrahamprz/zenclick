from django.core.management.base import BaseCommand

from agreement.gesd32_agreement import GESD32Agreement
from agreement.gesd32_inventory import GESD32InventoryAPI
from agreement.stirling_pdf import StirlingAPI

class Command(BaseCommand):
    def handle(self, *args, **options):
        print("Hello, world!")
        
        # Create the API objects
        inventory_api = GESD32InventoryAPI()
        stirling_api = StirlingAPI()
        agreement = GESD32Agreement(inventory_api, stirling_api)
        
        response = agreement.generate_device_return_receipt("33186")
        
        print(response.status_code)
