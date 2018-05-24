from datetime import datetime, timezone
from typing import Dict

from django.test import TestCase

from livestock.models import Animal


class TestAnimal(TestCase):
    """Unit testing Animal model."""
    def test_estimated_weight(self) -> None:
        animal: Animal = Animal.objects.create(id=100)
        animal.weights.create(weight=101, weight_date=datetime(2018, 5, 1).astimezone(tz=timezone.utc))
        animal.weights.create(weight=105, weight_date=datetime(2018, 5, 5).astimezone(tz=timezone.utc))

        estimated_weight: Dict[int, float] = Animal.objects.estimated_weight(datetime(2018, 5, 3))
        self.assertEqual(estimated_weight, {'num_animals': 1, 'estimated_total_weight': 103.0})
