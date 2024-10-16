
from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission

from organisations.models import Organisation

class Account(AbstractUser):

    groups = models.ManyToManyField(
        Group,
        related_name='ribbon_user_set',
        blank=True,
        help_text='The groups this user belongs to.',
        related_query_name='user',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='ribbon_user_permissions_set',
        blank=True,
        help_text='Specific permissions for this user.',
        related_query_name='user',
    )

    organisation = models.ForeignKey(Organisation, on_delete=models.CASCADE, related_name='accounts')
    email_verified = models.BooleanField(default=False)
    role = models.CharField(max_length=50, choices=[('admin', 'Admin'), ('staff', 'Staff')], default='admin')

    def __str__(self):
        return self.email
    