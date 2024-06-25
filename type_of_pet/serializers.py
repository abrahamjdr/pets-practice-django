from rest_framework import serializers
from .models import TypeOfPet


class TypeOfPetSerializer(serializers.ModelSerializer):
    class Meta:
        model = TypeOfPet
        fields = ['id', 'name', 'limbs_number']
        read_only_fields = ['id']

    def create(self, validated_data):
        type_of_pet = TypeOfPet.objects.create(
            name=validated_data['name'],
            limbs_number=validated_data['limbs_number'],
        )
        return type_of_pet

    def validate(self, attrs):
        if TypeOfPet.objects.filter(name=attrs['name']).exists():
            raise serializers.ValidationError("The type of pet already exists")
        return attrs

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.limbs_number = validated_data.get(
            'limbs_number', instance.limbs_number)
        instance.save()
        return instance

    def to_representation(self, instance):
        data = super().to_representation(instance)
        return data

    def to_internal_value(self, data):
        return super().to_internal_value(data)
