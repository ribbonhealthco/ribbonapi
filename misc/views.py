# misc/views.py


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import SendEmailSerializer
from config import core

from .emails import send_email

class SendEmailView(APIView):
    """
    API View to send an email using ZeptoMail API with SMTP fallback.
    """

    def post(self, request, *args, **kwargs):
        """
        Post an email to be sent using ZeptoMail API with SMTP fallback.
        
        Parameters:
        - to (list[str]): List of email addresses of recipients.
        - subject (str): Subject of the email.
        - template_id (str): ID of the email template.
        - vars (dict): Dictionary of variables to be used in the email template.
        - plain_text (str): Plain text content of the email.
        - html_page (str): HTML content of the email.
        - cc (list[str]): List of email addresses to be cc'd.
        - bcc (list[str]): List of email addresses to be bcc'd.
        
        Returns:
        - Response (dict): Response containing the status, code, and message of sending the email.
        """
        
        serializer = SendEmailSerializer(data=request.data)
        if serializer.is_valid():
            # Validate access key
            if serializer.validated_data['access_key'] != core.ACCESS_KEY:
                return Response({'status': 'failed', 'code': 401, 'message': 'Missing or incorrect access key'}, status=status.HTTP_401_UNAUTHORIZED)
            
            try:
                send_email(
                    to=serializer.validated_data['to'],
                    subject=serializer.validated_data['subject'],
                    template_id=serializer.validated_data.get('template_id'),
                    vars=serializer.validated_data.get('vars'),
                    plain_text=serializer.validated_data.get('plain_text'),
                    html_page=serializer.validated_data.get('html_page'),
                    cc=serializer.validated_data.get('cc'),
                    bcc=serializer.validated_data.get('bcc')
                )
                return Response({'status': 'success', 'code': 200, 'message': 'Email sent successfully'}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({'status': 'failed', 'code': 500, 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
