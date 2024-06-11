from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
import uuid

ROLE_CHOICES = (
    ('admin', 'Admin'),
    ('moderator', 'Moderator'),
    ('user', 'User'),
)


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          editable=False, db_column='id')
    password = models.CharField(blank=False, null=False, db_column='password')
    email = models.EmailField(unique=True, db_column='email')
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    address = models.CharField(max_length=255, default="")
    role = models.CharField(max_length=30, choices=ROLE_CHOICES)
    groups = models.ManyToManyField(Group, related_name='my_auth_user_groups')
    user_permissions = models.ManyToManyField(
        Permission, related_name='my_auth_user_permissions')
