
import random

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import OrganisationRegistrationSerializer

from misc.models import OTP
from misc.emails import send_email


class RegisterOrganisationView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = OrganisationRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            organisation, user = serializer.save()

            # Generate OTP and save it in the misc OTP model
            otp_code = str(random.randint(100000, 999999))
            OTP.objects.create(email=user.email, otp=otp_code)

            # Send the OTP to the user's email via the email API
            send_email(
                to=[user.email],
                subject="Verify your email address",
                template_id="verify-email-with-otp",  # Use ZeptoMail template
                vars={"OTP": otp_code}
            )

            # Generate JWT Token for the user
            refresh = RefreshToken.for_user(user)
            token = str(refresh.access_token)

            return Response({
                "status": "success",
                "code": 201,
                "message": "Organisation registered successfully. Please verify your email to continue.",
                "data": {
                    "organisation_id": organisation.organisation_id,
                    "organisation_slug": organisation.organisation_slug,
                    "email_verified": user.email_verified,
                    "token": token
                }
            }, status=status.HTTP_201_CREATED)
        return Response({
            "status": "failed",
            "code": 400,
            "message": "Invalid data provided.",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
