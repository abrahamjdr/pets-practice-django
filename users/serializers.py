from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email',
                  'phone_number', 'address', 'password', 'role']
        read_only_fields = ['id']
        extra_kwargs = {'password': {'write_only': True, 'required': True}}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = kwargs.get('context', {}).get('request')
        self.user = self.request.user

    def create(self, validated_data):
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
        if User.objects.filter(username=attrs['username']).exclude(id=attrs['id']).exists():
            raise serializers.ValidationError("El nombre de usuario ya existe")
        if User.objects.filter(email=attrs['email']).exclude(id=attrs['id']).exists():
            raise serializers.ValidationError(
                "El correo electrónico ya existe")
        return attrs

    def update(self, instance, validated_data):
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
        data = super().to_representation(instance)
        # Aquí puedes agregar o modificar campos en la representación serializada
        return data

    def to_internal_value(self, data):
        # Aquí puedes agregar o modificar la conversión de la representación serializada a un objeto
        return super().to_internal_value(data)
