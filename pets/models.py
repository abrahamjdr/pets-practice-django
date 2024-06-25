"""
    Models for the API's Pets
"""

from django.db import models
from type_of_pet.models import TypeOfPet
from users.models import User
from breed_of_pets.models import Breed
import uuid


class Pets(models.Model):
    """
        Model for pets

        This model represents a pet and its characteristics.

        Attributes:
            id (UUIDField): A unique identifier for the pet.
            name (CharField): The name of the pet.
            owner (ForeignKey): The owner of the pet, related to the User model.
            type_of_pet (ForeignKey): The type of pet, related to the TypeOfPet model.
            breed (ForeignKey): The breed of the pet, related to the Breed model.

        Notes:
            The id field is a UUIDField, which is a unique identifier that is not sequential.
            The name field is a CharField, which is a string field that can have up to 255 characters.
            The owner field is a ForeignKey, which relates the pet to a user.
            The type_of_pet field is a ForeignKey, which relates the pet to a type of pet.
            The breed field is a ForeignKey, which relates the pet to a breed.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          editable=False, db_column='id')
    name = models.CharField(max_length=255, blank=False, null=False)
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE)  # Relacion con users
    breed = models.ForeignKey(Breed, on_delete=models.CASCADE)
