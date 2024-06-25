from rest_framework import serializers
from .models import Pets


class PetsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pets
        fields = ['id', 'name', 'breed']
        read_only_fields = ['id']

    def create(self, validated_data, owner):
        pet = Pets.objects.create(
            name=validated_data['name'],
            owner=owner,
            breed=validated_data['breed'],
        )
        return pet

    def validate(self, attrs):
        return attrs

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.owner = validated_data.get('owner', instance.owner)
        instance.breed = validated_data.get('breed', instance.breed)
        instance.save()
        return instance

    def to_representation(self, instance):
        data = super().to_representation(instance)
        return data

    def to_internal_value(self, data):
        return super().to_internal_value(data)
