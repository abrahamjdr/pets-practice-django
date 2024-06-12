"""
Views for the authentication system
"""

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.core.exceptions import PermissionDenied
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializers import UserSerializer, LoginSerializer
from .models import User


class LoginViewSet(viewsets.ViewSet):
    """
    ViewSet for user login
    """
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def create(self, request):
        """
        Handle POST /login requests.

        Authenticates a user and returns an access token.

        Args:
            request (Request): The incoming request.

        Returns:
            Response: A response containing the access token and user information.
        """
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            token = AccessToken.for_user(user)
            return Response({
                'token': str(token),
                'user_id': user.pk,
                'email': user.email
            })
        else:
            return Response({'error': 'Invalid credentials'}, status=401)


class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet for User model

    This ViewSet provides CRUD operations for the User model.
    It uses the UserSerializer to serialize and deserialize User objects.

    Attributes:
        queryset (QuerySet): The queryset of all User objects.
        serializer_class (Serializer): The serializer class for User objects.

    Methods:
        list(request): Handle GET /users/ requests.
        create(request): Handle POST /users/ requests.
        retrieve(request, pk): Handle GET /users/:id requests.
        update(request, pk): Handle PUT /users/:id requests.
        partial_update(request, pk): Handle PATCH /users/:id requests.
        destroy(request, pk): Handle DELETE /users/:id requests.
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self):
        """
        Retrieves a single user object.

        This method is overridden to add permission checks.

        Returns:
            User: The requested user object.

        Raises:
            PermissionDenied: If the requesting user does not have permission to access the requested user.
        """
        obj = super().get_object()
        """
        Get the user object using the parent class's implementation.
        Check if the requesting user is not the same as the requested user and is not a superuser.
        If the check fails, raise a PermissionDenied exception.
        If the check passes, return the requested user object.
        
        """
        if self.request.user != obj and not self.request.user.is_superuser:
            raise PermissionDenied('No permission to access this user')
        return obj

    def list(self, request):
        """
        Handle GET /users/ requests.

        Returns a list of all User objects.

        Args:
            request (Request): The incoming request.

        Returns:
            Response: A response containing the list of User objects.
        """
        users = self.get_queryset()
        serializer = self.serializer_class(users, many=True)
        return Response(serializer.data)

    def create(self, request):
        """
        Handle POST /users/ requests.

        Creates a new User object with the provided data.

        Args:
            request (Request): The incoming request.

        Returns:
            Response: A response containing the created User object.
        """
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def retrieve(self, request, pk):
        """
        Handle GET /users/:id requests.

        Returns a single User object by ID.

        Args:
            request (Request): The incoming request.
            pk (int): The ID of the User object.

        Returns:
            Response: A response containing the User object.
        """
        user = self.get_object()
        serializer = self.serializer_class(user)
        return Response(serializer.data)

    def update(self, request, pk):
        """
        Handle PUT /users/:id requests.

        Updates an existing User object with the provided data.

        Args:
            request (Request): The incoming request.
            pk (int): The ID of the User object.

        Returns:
            Response: A response containing the updated User object.
        """
        user = self.get_object()
        serializer = self.serializer_class(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def partial_update(self, request, pk):
        """
        Handle PATCH /users/:id requests.

        Updates an existing User object with the provided partial data.

        Args:
            request (Request): The incoming request.
            pk (int): The ID of the User object.

        Returns:
            Response: A response containing the updated User object.
        """
        user = self.get_object()
        serializer = self.serializer_class(
            user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def destroy(self, request, pk):
        """
        Handle DELETE /users/:id requests.

        Deletes an existing User object by ID.

        Args:
            request (Request): The incoming request.
            pk (int): The ID of the User object.

        Returns:
            Response: A response indicating the deletion was successful.
        """
        user = self.get_object()
        user.delete()
        return Response(status=204)
