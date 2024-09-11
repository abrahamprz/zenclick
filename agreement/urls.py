from django.urls import path
from .views import AgreementFormView, HomeView

app_name = "agreement"

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('form/', AgreementFormView.as_view(), name='agreement_form'),
]