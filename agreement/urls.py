from django.urls import path
# from .views import AgreementFormView, HomeView
from .views import AgreementFormView

app_name = "agreement"

urlpatterns = [
    path('', AgreementFormView.as_view(), name='agreement_form'),
    # path('', HomeView.as_view(), name='home'),
    # path('form/', AgreementFormView.as_view(), name='agreement_form'),
]