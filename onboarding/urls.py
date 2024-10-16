
from django.urls import path
from .views import RegisterOrganisationView

urlpatterns = [
    path('register-organisation/', RegisterOrganisationView.as_view(), name='register_organisation'),
]
