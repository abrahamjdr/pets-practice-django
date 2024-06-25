from rest_framework import serializers
from .models import Breed


class BreedOfPetsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Breed
        fields = ['id', 'name', 'color', 'type_of_pet']
        read_only_fields = ['id']

    def create(self, validated_data):
        breed = Breed.objects.create(
            name=validated_data['name'],
            color=validated_data['color'],
            type_of_pet=validated_data['type_of_pet']
        )
        return breed

    def validate(self, attrs):
        if Breed.objects.filter(name=attrs['name']).exists():
            raise serializers.ValidationError("The breed already exists")
        return attrs

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.color = validated_data.get('color', instance.color)
        instance.type_of_pet = validated_data.get(
            'type_of_pet', instance.type_of_pet)
        instance.save()
        return instance

    def to_representation(self, instance):
        data = super().to_representation(instance)
        return data

    def to_internal_value(self, data):
        return super().to_internal_value(data)
