from django.db import models


# Create your models here.
class Venue(models.Model):
    name = models.CharField(max_length=150)
    location = models.TextField()
    price = models.DecimalField(verbose_name="Hotel cost", max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name + " - " + self.location
