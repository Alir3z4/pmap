from typing import Tuple

from rest_framework import serializers

from livestock.models import Animal, AnimalWeight


class AnimalWeightSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnimalWeight
        fields = '__all__'


class AnimalSerializer(serializers.ModelSerializer):
    weights = AnimalWeightSerializer(many=True, read_only=True)

    class Meta:
        model = Animal
        fields: Tuple[str] = ('id', 'weights', )
