from django.db import models


class Location(models.Model):
    address = models.CharField(max_length=255, unique=True,
                               verbose_name='адрес')
    latitude = models.FloatField(verbose_name='широта')
    longitude = models.FloatField(verbose_name='долгота')
    updated_at = models.DateTimeField(auto_now=True,
                                      verbose_name='Время запроса')

    class Meta:
        verbose_name = 'локация'
        verbose_name_plural = 'локации'

    def __str__(self):
        return self.address
