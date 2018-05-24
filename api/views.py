from collections import OrderedDict
from typing import List

import copy
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.request import Request
from rest_framework.response import Response

from api.serializers import AnimalSerializer, AnimalWeightSerializer, HerdSerializer, EstimatedWeightSerializer
from livestock.models import Animal, Herd


class BatchCreateMixin:
    """Mixin to add Batch creation."""
    def batch_create(self, batch_data: List[OrderedDict]) -> Response:
        """Batch create of Animals."""
        created_data = []

        for data in batch_data:
            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)

            created_data.append(serializer.data)

        return Response(created_data, status=status.HTTP_201_CREATED)

    def create(self, request: Request, *args, **kwargs) -> Response:
        """Override to handle `batch` requests."""
        if 'batch' in request.data and isinstance(request.data['batch'], list):
            return self.batch_create(request.data['batch'])

        return super(BatchCreateMixin, self).create(request, *args, **kwargs)


class HerdViewSet(BatchCreateMixin, viewsets.ModelViewSet):
    """Herd View Set."""
    serializer_class = HerdSerializer
    queryset = Herd.objects.filter()

    @action(detail=True, methods=['post'], url_path='delete-animal')
    def delete_animal(self, request: Request, *args, **kwargs) -> Response:
        """Remove an Animal from the Herd."""
        animal: Animal = get_object_or_404(self.get_object().animal_set.filter(), id=request.data['animal_id'])
        animal.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class AnimalViewSet(BatchCreateMixin, viewsets.ModelViewSet):
    """Animal View Set."""
    serializer_class = AnimalSerializer
    queryset = Animal.objects.filter()

    @action(detail=True, methods=['post'], serializer_class=AnimalWeightSerializer, url_path='weight')
    def add_weight(self, request, *args, **kwargs) -> Response:
        """Add weight record for an animal."""
        data = copy.deepcopy(request.data)
        data['animal'] = self.get_object().id

        serializer = AnimalWeightSerializer(data=data)
        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response(
            data=AnimalWeightSerializer(instance=serializer.instance).data,
            status=status.HTTP_201_CREATED
        )

    @action(detail=False, methods=['get'], serializer_class=EstimatedWeightSerializer, url_path='estimated_weight')
    def estimated_weight(self, request: Request, *args, **kwargs) -> Response:
        """Return estimated weight of animals for the a given date."""
        serializer = EstimatedWeightSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(data=serializer.data, status=status.HTTP_200_OK)
