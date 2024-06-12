"""
    Models for the API type_of_pets
"""

from django.db import models
import uuid


class TypeOfPet(models.Model):
    """
        Model for pet types

        This model represents a pet type and its characteristics.

        Attributes:
            id (UUIDField): A unique identifier for the pet type.
            name (CharField): The name of the pet type.
            limbs_number (IntegerField): The number of limbs of the pet type.

        Notes:
            The id field is a UUIDField, which is a unique identifier that is not sequential.
            The name field is a CharField, which is a string field that can have up to 255 characters.
            The limbs_number field is an IntegerField, which is a numeric field that can have a value between 0 and 2147483647.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          editable=False, db_column='id')
    name = models.CharField(blank=False, null=False, max_length=255)
    limbs_number = models.IntegerField(blank=False, null=False)

    def __str__(self):
        return self.name
