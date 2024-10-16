
from django.db import models
from django.utils import timezone
import uuid

class Organisation(models.Model):
    uid = models.AutoField(primary_key=True)
    organisation_id = models.UUIDField(default=uuid.uuid4, unique=True)
    organisation_slug = models.SlugField(unique=True)
    organisation_name = models.CharField(max_length=255)
    organisation_email = models.EmailField(unique=True)
    organisation_email_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.organisation_name
    