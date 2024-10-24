from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from logging import getLogger as logging_getLogger
from django.contrib.auth.decorators import user_passes_test
from django.utils.decorators import method_decorator

from agreement.gesd32_inventory import GESD32InventoryAPI
from agreement.stirling_pdf import StirlingAPI
from agreement.gesd32_agreement import GESD32Agreement

def is_admin(user):
    return user.is_authenticated and user.is_staff

@method_decorator(user_passes_test(is_admin), name='dispatch')
class AgreementFormView(View):
    def __init__(self):
        self.gesd32_inventory_api = GESD32InventoryAPI()
        self.stirling_api = StirlingAPI()
        self.agreement = GESD32Agreement(self.gesd32_inventory_api, self.stirling_api)
        self.logger = logging_getLogger(__name__)

    def get(self, request):
        return render(request, 'agreement_main.html')

    def post(self, request):
        device_tag = request.POST.get('device_tag')
        document_type = request.POST.get('document_type')

        # Check if the device_tag exists in the GESD32 inventory
        inventory_response = self.gesd32_inventory_api.get_items(asset_tag=device_tag)
        if not inventory_response['items']:
            return HttpResponse("Device with the given tag does not exist.", status=404)

        if document_type == 'user_agreement':
            response = self.agreement.generate_device_user_agreement(device_tag)
        elif document_type == 'return_receipt':
            response = self.agreement.generate_device_return_receipt(device_tag)
        else:
            return HttpResponse("Invalid document type", status=400)

        if response.status_code == 200:
            return HttpResponse(response.content, content_type='application/pdf')
        else:
            return HttpResponse(response.content, content_type='application/json')