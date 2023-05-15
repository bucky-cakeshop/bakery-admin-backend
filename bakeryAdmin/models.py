from django.db import models

# Create your models here.
class MeasureUnit(models.Model):
    title = models.CharField(max_length=200)
    symbol = models.CharField(max_length=20)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.title + self.symbol

