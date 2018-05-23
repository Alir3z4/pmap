from datetime import datetime

from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APITestCase

from api.serializers import AnimalSerializer
from livestock.models import Animal, AnimalWeight


class TestAPIViews(APITestCase):
    """Unit testing API Views."""
    def test_add_animal(self) -> None:
        resp: Response = self.client.post(path=reverse('api:animal-list'), data={'id': 100})
        
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Animal.objects.filter().count(), 1)
        self.assertEqual(Animal.objects.first().id, 100)
    
    def test_animal_weight_record(self) -> None:
        animal: Animal = Animal.objects.create(id=100)
        today = datetime.now()
        
        resp: Response = self.client.post(
            path=reverse('api:animal-add-weight', args=[animal.id, ]),
            data={'weight': 50, 'weight_date': today}
        )

        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(AnimalWeight.objects.filter().count(), 1)
        
        self.assertEqual(
            resp.data,
            {'id': 1, 'weight': 50.0, 'weight_date': f'{today.isoformat()}Z', 'animal': animal.id}
        )
    
    def test_animal_list(self) -> None:
        today = timezone.now()
        
        animal: Animal = Animal.objects.create(id=100)
        animal.weights.create(weight=50, weight_date=today)
        animal.weights.create(weight=52.1, weight_date=today)

        resp: Response = self.client.get(path=reverse('api:animal-list'))
        
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertIsInstance(resp.data, list)
        self.assertEqual(len(resp.data), 1)
        self.assertEqual(resp.data[0], AnimalSerializer(instance=animal).data)
