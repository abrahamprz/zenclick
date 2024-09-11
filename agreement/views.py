from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from django.conf import settings
from os import path as os_path
from sys import path as sys_path
from logging import getLogger as logging_getLogger, info as logging_info
from django.contrib.auth.decorators import user_passes_test
from django.utils.decorators import method_decorator

# ------------------------------------------------------------------------------

current = os_path.dirname(os_path.realpath(__file__))
# adding the parent directory to the sys.path
sys_path.append(current)

# ------------------------------------------------------------------------------
from apis.gesd32_inventory import GESD32InventoryAPI
from apis.stirling_pdf import StirlingAPI
from apis.gesd32_agreement import GESD32Agreement

# Test function to check if the user is an admin
def is_admin(user):
    return user.is_authenticated and user.is_staff

@method_decorator(user_passes_test(is_admin), name='dispatch')
class AgreementFormView(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.logger = logging_getLogger(__name__)
        self.gesd32_agreement = GESD32Agreement(
            GESD32InventoryAPI(settings.GESD32_INVENTORY_API_BASE_URL, settings.GESD32_INVENTORY_API_TOKEN), 
            StirlingAPI(settings.STIRLING_API_BASE_URL)
        )
    
    def get(self, request):
        return render(request, 'agreement_form.html')

    def post(self, request):
        tag_number = request.POST.get('tag_number')
        # Construct the path to the Markdown template
        template_path = os_path.join(settings.BASE_DIR, 'agreement', 'templates', 'device_user_agreement.md')
        pdf_content = self.gesd32_agreement.generate_device_user_agreement(device_tag=tag_number, agreement_path=template_path)        
        
        # Return the PDF content as a file response
        response = HttpResponse(pdf_content, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename=agreement_{tag_number}.pdf'
        return response

class HomeView(View):
    def get(self, request):
        return render(request, 'home.html')