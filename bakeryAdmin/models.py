from django.db import models

# Create your models here.
class MeasureUnit(models.Model):
    title = models.CharField(max_length=200)
    symbol = models.CharField(max_length=20)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.title + self.symbol

class Ingredient(models.Model):
    name = models.CharField(max_length=200)
    measureUnit = models.ForeignKey(MeasureUnit, on_delete=models.DO_NOTHING)
    
    def __str__(self):
        return self.name
