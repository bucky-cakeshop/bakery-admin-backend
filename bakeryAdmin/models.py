from django.db import models
from django.utils import timezone

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
        return str(self.pk) + " - " + self.name

class FixedCost(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    amount = models.FloatField()

    def __str__(self):
        return self.title + self.amount

class Recipe(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    creationAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now_add=True)
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        self.updatedAt = timezone.now()
        return super().save(*args, **kwargs)

class RecipeDetail(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE,related_name='recipe')
    ingredient = models.ForeignKey(Ingredient, on_delete=models.DO_NOTHING)
    measureUnit = models.ForeignKey(MeasureUnit, on_delete=models.DO_NOTHING)
    quantity = models.DecimalField(max_digits=4,decimal_places=1)
    
    def __str__(self):
        return f'{self.ingredient.name} {self.measureUnit.symbol}'
