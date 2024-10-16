from django.db import models
from django.utils import timezone

class OTP(models.Model):
    email = models.EmailField()
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(default=timezone.now)
    is_used = models.BooleanField(default=False)

    def is_valid(self):
        """ OTP is valid for 10 minutes and must not have been used. """
        expiry_time = self.created_at + timezone.timedelta(minutes=10)
        return not self.is_used and timezone.now() <= expiry_time
