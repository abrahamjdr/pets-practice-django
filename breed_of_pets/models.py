"""
    Models for the API breeds
"""

from django.db import models
from type_of_pet.models import TypeOfPet
import uuid


class Breed(models.Model):
    """
        Model for pet breeds

        This model represents a pet breed and its characteristics.

        Attributes:
            id (UUIDField): A unique identifier for the breed.
            name (CharField): The name of the breed.
            color (CharField): The color of the breed.
            type_of_pet (ForeignKey): The type of pet that the breed belongs to, related to the TypeOfPet model.

        Notes:
            The id field is a UUIDField, which is a unique identifier that is not sequential.
            The name field is a CharField, which is a string field that can have up to 255 characters.
            The color field is a CharField, which is a string field that can have up to 255 characters.
            The type_of_pet field is a ForeignKey, which relates the breed to a type of pet.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          editable=False, db_column='id')
    name = models.CharField(max_length=255, blank=False, null=False)
    color = models.CharField(max_length=255, blank=False, null=False)
    type_of_pet = models.ForeignKey(
        TypeOfPet, on_delete=models.CASCADE)  # Relación con TypeOfPet

    def __str__(self):
        return self.name
