from datetime import datetime

from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.exceptions import ErrorDetail
from rest_framework.response import Response
from rest_framework.test import APITestCase

from api.serializers import AnimalSerializer, HerdSerializer
from livestock.models import Animal, AnimalWeight, Herd


class TestAPIViews(APITestCase):
    """Unit testing API Views."""
    def test_add_animal(self) -> None:
        resp: Response = self.client.post(path=reverse('api:animal-list'), data={'id': 100})

        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Animal.objects.filter().count(), 1)
        self.assertEqual(Animal.objects.first().id, 100)

    def test_batch_animal_addition(self) -> None:
        herd: Herd = Herd.objects.create(name='meat lovers')

        resp: Response = self.client.post(
            path=reverse('api:animal-list'),
            data={'batch': [{'id': 100}, {'id': 200, 'herd': herd.id}]},
            format='json'
        )

        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            resp.data,
            [{'id': 100, 'weights': [], 'herd': None}, {'id': 200, 'weights': [], 'herd': herd.id}]
        )

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

        # Testing bad data for weights
        resp: Response = self.client.post(
            path=reverse('api:animal-add-weight', args=[animal.id, ]),
            data={'weight': 50}
        )

        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.data, {'weight_date': [ErrorDetail(string='This field is required.', code='required')]})

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

    def test_edit_animal(self) -> None:
        animal: Animal = Animal.objects.create(id=100)

        resp: Response = self.client.put(
            path=reverse('api:animal-detail', args=[animal.id]),
            data={'id': 400}
        )

        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data, {'id': 400, 'weights': [], 'herd': None})

        animal.refresh_from_db()
        herd: Herd = Herd.objects.create(name='meat lovers')
        resp: Response = self.client.put(
            path=reverse('api:animal-detail', args=[animal.id]),
            data={'herd': herd.id, 'id': animal.id}
        )

        self.assertEqual(resp.data, {'id': animal.id, 'weights': [], 'herd': herd.id})

    def test_add_herd(self) -> None:
        resp: Response = self.client.post(path=reverse('api:herd-list'), data={'name': 'meat lovers'})

        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Herd.objects.filter().count(), 1)

    def test_batch_herd_addition(self) -> None:
        resp: Response = self.client.post(
            path=reverse('api:herd-list'),
            data={'batch': [{'name': 'meat lovers'}, {'name': 'grass lovers'}]},
            format='json'
        )

        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Herd.objects.filter().count(), 2)
        self.assertEqual(
            resp.data,
            [{'id': 1, 'name': 'meat lovers', 'animals': []}, {'id': 2, 'name': 'grass lovers', 'animals': []}]
        )

    def test_herd_list(self) -> None:
        herd: Herd = Herd.objects.create(name='meat lovers')
        herd.animal_set.create(id=2)

        resp: Response = self.client.get(path=reverse('api:herd-list'))

        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertIsInstance(resp.data, list)
        self.assertEqual(len(resp.data), 1)
        self.assertEqual(resp.data[0], HerdSerializer(instance=herd).data)

    def test_delete_animal_from_herd(self) -> None:
        herd: Herd = Herd.objects.create(name='meat lovers')
        herd.animal_set.create(id=1)
        herd.animal_set.create(id=2)

        resp: Response = self.client.post(
            path=reverse('api:herd-delete-animal', args=[herd.id]),
            data={'animal_id': 1}
        )

        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(herd.animal_set.filter().count(), 1)
        self.assertEqual(herd.animal_set.first().id, 2)
