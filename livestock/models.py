from django.db import models
from django.utils.translation import ugettext_lazy as _


class Herd(models.Model):
    """Herd model."""
    name = models.CharField(verbose_name=_('herd'), max_length=150)

    class Meta:
        verbose_name = _('Herd')
        verbose_name_plural = _('Herds')

    def __str__(self) -> str:
        return self.name


class Animal(models.Model):
    """Animal model."""
    id = models.IntegerField(primary_key=True, verbose_name=_('id'))
    herd = models.ForeignKey(Herd, blank=True, null=True, on_delete=models.SET_NULL)

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
