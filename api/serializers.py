from typing import Tuple, Union, Dict

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
        fields: Tuple[str] = ('id', 'weights', 'herd', )


class HerdSerializer(serializers.ModelSerializer):
    """Herd Serializer."""
    animals = AnimalSerializer(many=True, source='animal_set', read_only=True)

    class Meta:
        model = Herd
        fields: Tuple[str] = ('id', 'name', 'animals', )


class EstimatedWeightSerializer(serializers.Serializer):
    """Estimated Weight Serializer."""
    num_animals = serializers.IntegerField(read_only=True)
    estimated_total_weight = serializers.FloatField(read_only=True)
    date = serializers.DateTimeField(write_only=True, required=True)

    def create(self, validated_data) -> Dict[str, Union[int, float]]:
        return Animal.objects.estimated_weight(validated_data['date'])
