
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from organisations.models import Organisation
from accounts.models import Account

class OrganisationRegistrationTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('register_organisation')

    def test_register_organisation_success(self):
        data = {
            "organisation_name": "Health Services Ltd.",
            "email": "admin@healthservices.com",
            "password": "strongpassword123"
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['status'], 'success')
        self.assertTrue(Organisation.objects.filter(organisation_email="admin@healthservices.com").exists())
        self.assertTrue(Account.objects.filter(email="admin@healthservices.com").exists())

    def test_register_organisation_invalid_email(self):
        data = {
            "organisation_name": "Health Services Ltd.",
            "email": "invalid-email",
            "password": "strongpassword123"
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['status'], 'failed')
    