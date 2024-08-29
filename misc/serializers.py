# your_app/serializers.py

from rest_framework import serializers

class SendEmailSerializer(serializers.Serializer):
    access_key = serializers.CharField(required=True)
    to = serializers.ListField(child=serializers.EmailField(), required=True)
    cc = serializers.ListField(child=serializers.EmailField(), required=False)
    bcc = serializers.ListField(child=serializers.EmailField(), required=False)
    subject = serializers.CharField(required=True)
    template_id = serializers.CharField(required=False)
    vars = serializers.DictField(required=False)
    plain_text = serializers.CharField(required=False)
    html_page = serializers.CharField(required=False)
