from django.db import models

# Create your models here.


class Route(models.Model):
    DIRECTION_CHOICES = [
        ("UP", "UP"),
        ("Down", "Down")
    ]
    STATUS_CHOICES = [
        ("Active", "Active"),
        ("Inactive", "Inactive")
    ]
    TYPE_CHOICES = [
        ("AC", "AC"),
        ("General", "General")
    ]
    name = models.CharField(verbose_name="Route Name", unique=True, blank=False, null=False, max_length=50)
    direction = models.CharField(verbose_name="Direction", null=False, blank=False, choices=DIRECTION_CHOICES, max_length=10)
    status = models.CharField(verbose_name="Status", null=False, blank=False, choices=STATUS_CHOICES, max_length=10)
    list_of_stops = models.TextField(verbose_name="Stops", null=False, blank=False)
    type = models.CharField(verbose_name="Type", null=False, blank=False, choices=TYPE_CHOICES, max_length=10)


class Stop(models.Model):
    name = models.CharField(verbose_name="Name", unique=True, blank=False, null=False, max_length=50)
    latitudes = models.DecimalField(verbose_name="Latitudes", max_digits=9, decimal_places=6)
    longitudes = models.DecimalField(verbose_name="Longitudes", max_digits=9, decimal_places=6)

    def __str__(self):
        return self.name

