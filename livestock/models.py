from datetime import datetime
from typing import Dict, Union, List

from django.db import models
from django.utils.translation import ugettext_lazy as _

from livestock.utils import linear_interpolation_datetime


class Herd(models.Model):
    """Herd model."""
    name = models.CharField(verbose_name=_('herd'), max_length=150)

    class Meta:
        verbose_name = _('Herd')
        verbose_name_plural = _('Herds')

    def __str__(self) -> str:
        return self.name


class AnimalManager(models.Manager):
    """Animal Weight Manager."""
    def estimated_weight(self, weight_date: datetime) -> Dict[str, Union[int, float]]:
        """Estimated weight of animals."""
        estimated_weights: List[float] = []
        for animal in self.all():
            weight_records = animal.weights.filter().values_list('weight_date', 'weight')
            estimated_weight: float = linear_interpolation_datetime(weight_records, weight_date)
            estimated_weights.append(estimated_weight)

        return {
            'num_animals': self.all().count(),
            'estimated_total_weight': sum(estimated_weights)
        }


class Animal(models.Model):
    """Animal model."""
    id = models.IntegerField(primary_key=True, verbose_name=_('id'))
    herd = models.ForeignKey(Herd, blank=True, null=True, on_delete=models.SET_NULL)

    objects = AnimalManager()

    class Meta:
        verbose_name = _('Animal')
        verbose_name_plural = _('Animals')

    def __str__(self) -> str:
        return f'Animal {self.id}'


class AnimalWeight(models.Model):
    """Animal Weight model."""
    animal = models.ForeignKey(Animal, verbose_name=_('animal'), on_delete=models.CASCADE, related_name='weights')
    weight = models.FloatField(verbose_name=_('weight'))
    weight_date = models.DateTimeField(verbose_name=_('weight date'))

    class Meta:
        verbose_name = _('Animal Weight')
        verbose_name_plural = _('Animal Weights')

    def __str__(self) -> str:
        return f'Animal {self.animal.id} W {self.weight} WDate {self.weight_date}'
