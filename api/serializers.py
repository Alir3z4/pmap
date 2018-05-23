from typing import Tuple

from rest_framework import serializers

from livestock.models import Animal, AnimalWeight, Herd


class AnimalWeightSerializer(serializers.ModelSerializer):
    """Animal Weight Serializer."""
    class Meta:
        model = AnimalWeight
        fields = '__all__'


class AnimalSerializer(serializers.ModelSerializer):
    """Animal Serializer."""
    weights = AnimalWeightSerializer(many=True, read_only=True)

    class Meta:
        model = Animal
        fields: Tuple[str] = ('id', 'weights', )


class HerdSerializer(serializers.ModelSerializer):
    """Herd Serializer."""
    animals = AnimalSerializer(many=True, source='animal_ser', read_only=True)

    class Meta:
        model = Herd
        fields: Tuple[str] = ('id', 'name', 'animals', )
