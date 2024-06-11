"""
Serializers for the authentication system
"""

from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for User model

    This serializer is used to serialize and deserialize User objects.
    It includes fields for username, email, phone number, address, password, and role.
    The password field is write-only and required.
    The id field is read-only.

    Attributes:
        request (Request): The request object passed to the serializer.
        user (User): The user object associated with the request.

    Methods:
        create(validated_data): Create a new user with the validated data.
        validate(attrs): Validate the username and email uniqueness.
        update(instance, validated_data): Update an existing user with the validated data.
        to_representation(instance): Convert the instance to a serialized representation.
        to_internal_value(data): Convert the serialized data to an internal value.
    """

    class Meta:
        model = User
        fields = ['id', 'username', 'email',
                  'phone_number', 'address', 'password', 'role']
        read_only_fields = ['id']
        extra_kwargs = {'password': {'write_only': True, 'required': True}}

    def __init__(self, *args, **kwargs):
        """
        Initialize the serializer with the request and user objects.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        super().__init__(*args, **kwargs)
        self.request = kwargs.get('context', {}).get('request')
        self.user = self.request.user

    def create(self, validated_data):
        """
        Create a new user with the validated data.

        Args:
            validated_data (dict): The validated data to create the user.

        Returns:
            User: The created user object.
        """
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            phone_number=validated_data['phone_number'],
            address=validated_data['address'],
            role=validated_data['role']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    def validate(self, attrs):
        """
        Validate the username and email uniqueness.

        Args:
            attrs (dict): The attributes to validate.

        Returns:
            dict: The validated attributes.

        Raises:
            serializers.ValidationError: If the username or email already exists.
        """
        if User.objects.filter(username=attrs['username']).exclude(id=attrs['id']).exists():
            raise serializers.ValidationError("El nombre de usuario ya existe")
        if User.objects.filter(email=attrs['email']).exclude(id=attrs['id']).exists():
            raise serializers.ValidationError(
                "El correo electrónico ya existe")
        return attrs

    def update(self, instance, validated_data):
        """
        Update an existing user with the validated data.

        Args:
            instance (User): The user object to update.
            validated_data (dict): The validated data to update the user.

        Returns:
            User: The updated user object.
        """
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.phone_number = validated_data.get(
            'phone_number', instance.phone_number)
        instance.address = validated_data.get('address', instance.address)
        instance.role = validated_data.get('role', instance.role)

        if 'password' in validated_data:
            instance.set_password(validated_data['password'])

        instance.save()
        return instance

    def to_representation(self, instance):
        """
        Convert the instance to a serialized representation.

        Args:
            instance (User): The user object to serialize.

        Returns:
            dict: The serialized representation of the user object.
        """
        data = super().to_representation(instance)
        # Aquí puedes agregar o modificar campos en la representación serializada
        return data

    def to_internal_value(self, data):
        """
        Convert the serialized data to an internal value.

        Args:
            data (dict): The serialized data to convert.

        Returns:
            dict: The internal value of the serialized data.
        """
        # Aquí puedes agregar o modificar la conversión de la representación serializada a un objeto
        return super().to_internal_value(data)
