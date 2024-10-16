
from rest_framework import serializers
from django.contrib.auth.hashers import make_password

from organisations.models import Organisation
from user.models import User

class OrganisationRegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = Organisation
        fields = ['organisation_name', 'email', 'password']

    def create(self, validated_data):
        # Create the Organisation
        organisation = Organisation.objects.create(
            organisation_name=validated_data['organisation_name'],
            organisation_slug=validated_data['organisation_name'].lower().replace(' ', '-'),
            organisation_email=validated_data['email'],
        )

        # Create Admin User for the Organisation
        user = User.objects.create(
            username=validated_data['email'],
            email=validated_data['email'],
            password=make_password(validated_data['password']),
            organisation=organisation,
            role='admin'
        )

        return organisation, user