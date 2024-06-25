from django.core.exceptions import PermissionDenied
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializers import BreedOfPetsSerializer
from .models import Breed
# Create your views here.


class BreedViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Breed model

    This ViewSet provides CRUD operations for the Breed model.
    It uses the breedSerializer to serialize and deserialize Breed objects.

    Attributes:
        queryset (QuerySet): The queryset of all Breed objects.
        serializer_class (Serializer): The serializer class for Breed objects.

    Methods:
        list(request): Handle GET /breed/ requests.
        create(request): Handle POST /breed/ requests.
        retrieve(request, pk): Handle GET /breed/:id requests.
        update(request, pk): Handle PUT /breed/:id requests.
        partial_update(request, pk): Handle PATCH /breed/:id requests.
        destroy(request, pk): Handle DELETE /breed/:id requests.
    """

    queryset = Breed.objects.all()
    serializer_class = BreedOfPetsSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self):
        """
        Retrieves a single Breed object.

        This method is overridden to add permission checks.

        Returns:
            Breed: The requested Breed object.

        Raises:
            PermissionDenied: If the requesting Breed does not have permission to access the requested Breed.
        """
        obj = super().get_object()
        """
        Get the Breed object using the parent class's implementation.
        Check if the requesting Breed is not the same as the requested Breed and is not a superBreed.
        If the check fails, raise a PermissionDenied exception.
        If the check passes, return the requested Breed object.
        
        """
        if self.request.user != obj and not self.request.user.is_superuser:
            raise PermissionDenied('No permission to access this Breed')
        return obj

    def list(self, request):
        """
        Handle GET /breed/ requests.

        Returns a list of all Breed objects.

        Args:
            request (Request): The incoming request.

        Returns:
            Response: A response containing the list of Breed objects.
        """
        breed = self.get_queryset()
        serializer = self.serializer_class(breed, many=True)
        return Response(serializer.data)

    def create(self, request):
        """
        Handle POST /breed/ requests.

        Creates a new Breed object with the provided data.

        Args:
            request (Request): The incoming request.

        Returns:
            Response: A response containing the created Breed object.
        """
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def retrieve(self, request, pk):
        """
        Handle GET /breed/:id requests.

        Returns a single Breed object by ID.

        Args:
            request (Request): The incoming request.
            pk (int): The ID of the Breed object.

        Returns:
            Response: A response containing the Breed object.
        """
        breed = self.get_object()
        serializer = self.serializer_class(breed)
        return Response(serializer.data)

    def update(self, request, pk):
        """
        Handle PUT /breed/:id requests.

        Updates an existing Breed object with the provided data.

        Args:
            request (Request): The incoming request.
            pk (int): The ID of the Breed object.

        Returns:
            Response: A response containing the updated Breed object.
        """
        breed = self.get_object()
        serializer = self.serializer_class(breed, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def partial_update(self, request, pk):
        """
        Handle PATCH /breed/:id requests.

        Updates an existing Breed object with the provided partial data.

        Args:
            request (Request): The incoming request.
            pk (int): The ID of the Breed object.

        Returns:
            Response: A response containing the updated Breed object.
        """
        breed = self.get_object()
        serializer = self.serializer_class(
            breed, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def destroy(self, request, pk):
        """
        Handle DELETE /breed/:id requests.

        Deletes an existing Breed object by ID.

        Args:
            request (Request): The incoming request.
            pk (int): The ID of the Breed object.

        Returns:
            Response: A response indicating the deletion was successful.
        """
        breed = self.get_object()
        breed.delete()
        return Response(status=204)
