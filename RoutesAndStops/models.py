from django.db import models

# Create your models here.


class Route(models.Model):
    DIRECTION_CHOICES = [
        (True, "UP"),
        (False, "Down")
    ]
    STATUS_CHOICES = [
        (True, "Active"),
        (False, "Inactive")
    ]
    TYPE_CHOICES = [
        (True, "AC"),
        (False, "General")
    ]
    name = models.CharField(verbose_name="Route Name", unique=True, blank=False, null=False, max_length=50)
    direction = models.BooleanField(verbose_name="Direction", null=False, blank=False, choices=DIRECTION_CHOICES)
    status = models.BooleanField(verbose_name="Status", null=False, blank=False, choices=STATUS_CHOICES)
    list_of_stops = models.TextField(verbose_name="Stops", null=False, blank=False)
    type = models.BooleanField(verbose_name="Type", null=False, blank=False, choices=TYPE_CHOICES)


class Stop(models.Model):
    name = models.CharField(verbose_name="Name", unique=True, blank=False, null=False, max_length=50)
    latitudes = models.DecimalField(verbose_name="Latitudes", max_digits=9, decimal_places=6)
    longitudes = models.DecimalField(verbose_name="Longitudes", max_digits=9, decimal_places=6)

