from django.core.exceptions import PermissionDenied
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializers import PetsSerializer
from .models import Pets


class PetsViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Pets model

    This ViewSet provides CRUD operations for the Pets model.
    It uses the petserializer to serialize and deserialize Pets objects.

    Attributes:
        queryset (QuerySet): The queryset of all Pets objects.
        serializer_class (Serializer): The serializer class for Pets objects.

    Methods:
        list(request): Handle GET /pets/ requests.
        create(request): Handle POST /pets/ requests.
        retrieve(request, pk): Handle GET /pets/:id requests.
        update(request, pk): Handle PUT /pets/:id requests.
        partial_update(request, pk): Handle PATCH /pets/:id requests.
        destroy(request, pk): Handle DELETE /pets/:id requests.
    """

    queryset = Pets.objects.all()
    serializer_class = PetsSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self):
        """
        Retrieves a single Pets object.

        This method is overridden to add permission checks.

        Returns:
            Pets: The requested Pets object.

        Raises:
            PermissionDenied: If the requesting Pets does not have permission to access the requested Pets.
        """
        obj = super().get_object()
        """
        Get the Pets object using the parent class's implementation.
        Check if the requesting Pets is not the same as the requested Pets and is not a superPets.
        If the check fails, raise a PermissionDenied exception.
        If the check passes, return the requested Pets object.
        
        """
        if self.request.user != obj and not self.request.user.is_superuser:
            raise PermissionDenied('No permission to access this Pets')
        return obj

    def list(self, request):
        """
        Handle GET /pets/ requests.

        Returns a list of all Pets objects.

        Args:
            request (Request): The incoming request.

        Returns:
            Response: A response containing the list of Pets objects.
        """
        breed = self.get_queryset()
        serializer = self.serializer_class(breed, many=True)
        return Response(serializer.data)

    def create(self, request):
        """
        Handle POST /pets/ requests.

        Creates a new Pets object with the provided data.

        Args:
            request (Request): The incoming request.

        Returns:
            Response: A response containing the created Pets object.
        """
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.create(
                validated_data=serializer.validated_data, owner=request.user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def retrieve(self, request, pk):
        """
        Handle GET /pets/:id requests.

        Returns a single Pets object by ID.

        Args:
            request (Request): The incoming request.
            pk (int): The ID of the Pets object.

        Returns:
            Response: A response containing the Pets object.
        """
        breed = self.get_object()
        serializer = self.serializer_class(breed)
        return Response(serializer.data)

    def update(self, request, pk):
        """
        Handle PUT /pets/:id requests.

        Updates an existing Pets object with the provided data.

        Args:
            request (Request): The incoming request.
            pk (int): The ID of the Pets object.

        Returns:
            Response: A response containing the updated Pets object.
        """
        breed = self.get_object()
        serializer = self.serializer_class(breed, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def partial_update(self, request, pk):
        """
        Handle PATCH /pets/:id requests.

        Updates an existing Pets object with the provided partial data.

        Args:
            request (Request): The incoming request.
            pk (int): The ID of the Pets object.

        Returns:
            Response: A response containing the updated Pets object.
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
        Handle DELETE /pets/:id requests.

        Deletes an existing Pets object by ID.

        Args:
            request (Request): The incoming request.
            pk (int): The ID of the Pets object.

        Returns:
            Response: A response indicating the deletion was successful.
        """
        breed = self.get_object()
        breed.delete()
        return Response(status=204)
