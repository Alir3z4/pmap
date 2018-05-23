import copy
from django.core.exceptions import ValidationError
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from api.serializers import AnimalSerializer, AnimalWeightSerializer, HerdSerializer
from livestock.models import Animal


class HerdViewSet(viewsets.ModelViewSet):
    """Herd View Set."""
    serializer_class = HerdSerializer
    queryset = Animal.objects.filter()


class AnimalViewSet(viewsets.ModelViewSet):
    """Animal View Set."""
    serializer_class = AnimalSerializer
    queryset = Animal.objects.filter()

    @action(detail=True, methods=['post'], serializer_class=AnimalWeightSerializer, url_path='weight')
    def add_weight(self, request, *args, **kwargs) -> Response:
        """Add weight record for an animal."""
        data = copy.deepcopy(request.data)
        data['animal'] = self.get_object().id

        serializer = AnimalWeightSerializer(data=data)

        if not serializer.is_valid():
            raise ValidationError(serializer.errors)

        serializer.save()

        return Response(
            data=AnimalWeightSerializer(instance=serializer.instance).data,
            status=status.HTTP_201_CREATED
        )
