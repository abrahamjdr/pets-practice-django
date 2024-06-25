from django.core.exceptions import PermissionDenied
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializers import TypeOfPetSerializer
from .models import TypeOfPet


class TypeOfPetViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Type Of Pet model

    This ViewSet provides CRUD operations for the Type Of Pet model.
    It uses the type-of-peterializer to serialize and deserialize Type Of Pet objects.

    Attributes:
        queryset (QuerySet): The queryset of all Type Of Pet objects.
        serializer_class (Serializer): The serializer class for Type Of Pet objects.

    Methods:
        list(request): Handle GET /type-of-pet/ requests.
        create(request): Handle POST /type-of-pet/ requests.
        retrieve(request, pk): Handle GET /type-of-pet/:id requests.
        update(request, pk): Handle PUT /type-of-pet/:id requests.
        partial_update(request, pk): Handle PATCH /type-of-pet/:id requests.
        destroy(request, pk): Handle DELETE /type-of-pet/:id requests.
    """

    queryset = TypeOfPet.objects.all()
    serializer_class = TypeOfPetSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self):
        """
        Retrieves a single Type Of Pet object.

        This method is overridden to add permission checks.

        Returns:
            Type Of Pet: The requested Type Of Pet object.

        Raises:
            PermissionDenied: If the requesting Type Of Pet does not have permission to access the requested Type Of Pet.
        """
        obj = super().get_object()
        """
        Get the Type Of Pet object using the parent class's implementation.
        Check if the requesting Type Of Pet is not the same as the requested Type Of Pet and is not a superType Of Pet.
        If the check fails, raise a PermissionDenied exception.
        If the check passes, return the requested Type Of Pet object.
        
        """
        if self.request.user != obj and not self.request.user.is_superuser:
            raise PermissionDenied('No permission to access this Type Of Pet')
        return obj

    def list(self, request):
        """
        Handle GET /type-of-pet/ requests.

        Returns a list of all Type Of Pet objects.

        Args:
            request (Request): The incoming request.

        Returns:
            Response: A response containing the list of Type Of Pet objects.
        """
        breed = self.get_queryset()
        serializer = self.serializer_class(breed, many=True)
        return Response(serializer.data)

    def create(self, request):
        """
        Handle POST /type-of-pet/ requests.

        Creates a new Type Of Pet object with the provided data.

        Args:
            request (Request): The incoming request.

        Returns:
            Response: A response containing the created Type Of Pet object.
        """
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def retrieve(self, request, pk):
        """
        Handle GET /type-of-pet/:id requests.

        Returns a single Type Of Pet object by ID.

        Args:
            request (Request): The incoming request.
            pk (int): The ID of the Type Of Pet object.

        Returns:
            Response: A response containing the Type Of Pet object.
        """
        breed = self.get_object()
        serializer = self.serializer_class(breed)
        return Response(serializer.data)

    def update(self, request, pk):
        """
        Handle PUT /type-of-pet/:id requests.

        Updates an existing Type Of Pet object with the provided data.

        Args:
            request (Request): The incoming request.
            pk (int): The ID of the Type Of Pet object.

        Returns:
            Response: A response containing the updated Type Of Pet object.
        """
        breed = self.get_object()
        serializer = self.serializer_class(breed, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def partial_update(self, request, pk):
        """
        Handle PATCH /type-of-pet/:id requests.

        Updates an existing Type Of Pet object with the provided partial data.

        Args:
            request (Request): The incoming request.
            pk (int): The ID of the Type Of Pet object.

        Returns:
            Response: A response containing the updated Type Of Pet object.
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
        Handle DELETE /type-of-pet/:id requests.

        Deletes an existing Type Of Pet object by ID.

        Args:
            request (Request): The incoming request.
            pk (int): The ID of the Type Of Pet object.

        Returns:
            Response: A response indicating the deletion was successful.
        """
        breed = self.get_object()
        breed.delete()
        return Response(status=204)
