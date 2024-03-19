import math

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import manager


class PlaceImage(models.Model):
    place = models.ForeignKey('PlaceModel', on_delete=models.CASCADE, related_name='images')
    url = models.ImageField(upload_to='images/place/%Y/%m/%d/')
    objects: manager


class Category(models.Model):
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=100, default='Standard')
    url = models.FileField(upload_to='images/category/%Y/%m/%d/', blank=True, null=True)
    objects: manager

    def __str__(self):
        return self.name


class PlaceModel(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, related_name='places', blank=True, null=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    description = models.TextField(blank=True, null=True)
    views = models.IntegerField(default=0, verbose_name="Количество просмотров")
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name="Рейтинг"
    )
    quadkey = models.CharField(max_length=30, db_index=True, blank=True)
    objects: manager

    clast = 0

    @staticmethod
    def get_quadkey(lat, lng, zoom=19):
        x = int((lng + 180) / 360 * (1 << zoom))
        y = int(
            (1 - math.log(math.tan(math.radians(lat)) + 1 / math.cos(math.radians(lat))) / math.pi) / 2 * (1 << zoom))
        quadkey = ''
        for i in range(zoom, 0, -1):
            digit = 0
            mask = 1 << (i - 1)
            if (x & mask) != 0:
                digit += 1
            if (y & mask) != 0:
                digit += 2
            quadkey += str(digit)
        return quadkey

    class Meta:
        unique_together = ['latitude', 'longitude']

    def save(self, *args, **kwargs):
        self.quadkey = self.get_quadkey(float(self.latitude), float(self.longitude))
        super(PlaceModel, self).save(*args, **kwargs)

    def increment_view_count(self):
        self.views += 1
        self.save()

    def __str__(self):
        return self.name
