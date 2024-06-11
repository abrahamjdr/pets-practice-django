"""
Models for the authentication system
"""

from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
import uuid

ROLE_CHOICES = (
    ('admin', 'Admin'),
    ('moderator', 'Moderator'),
    ('user', 'User'),
)


class User(AbstractUser):
    """
    Custom User model

    This model extends the built-in Django AbstractUser model to add additional fields.

    Attributes:
        id (UUIDField): A unique identifier for the user.
        password (CharField): The user's password.
        email (EmailField): The user's email address.
        phone_number (CharField): The user's phone number.
        address (CharField): The user's address.
        role (CharField): The user's role (admin, moderator, or user).
        groups (ManyToManyField): The groups the user belongs to.
        user_permissions (ManyToManyField): The permissions the user has.

    Notes:
        The id field is a UUIDField, which is a unique identifier that is not sequential.
        The password field is a CharField, which is a string field that is not encrypted by default.
        The email field is an EmailField, which is a string field that is validated to ensure it is a valid email address.
        The phone_number field is a CharField, which is a string field that can be up to 20 characters long.
        The address field is a CharField, which is a string field that can be up to 255 characters long.
        The role field is a CharField, which is a string field that can be one of the choices in ROLE_CHOICES.
        The groups field is a ManyToManyField, which is a field that can be related to multiple groups.
        The user_permissions field is a ManyToManyField, which is a field that can be related to multiple permissions.
    """

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
