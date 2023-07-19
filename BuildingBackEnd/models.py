from django.contrib.gis.db import models
from rest_framework import serializers

def geom_validation(value):
    if not value.valid:
        raise serializers.ValidationError(value.valid_reason)

        
class Building(models.Model):
    address = models.CharField(max_length=100, null=True, blank=True)
    geom = models.GeometryField(srid=4326, validators=[geom_validation])

    def __str__(self):
        return str(type(self.geom)) + str(self.geom)