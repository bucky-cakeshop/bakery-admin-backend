from django.db import models
from datetime import datetime
from django.core.validators import EmailValidator
from django.utils import timezone
from django.core.exceptions import ValidationError

# Create your models here.
class MeasureUnit(models.Model):
    title = models.CharField(max_length=200)
    symbol = models.CharField(max_length=20)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.title + self.symbol

class Ingredient(models.Model):
    name = models.CharField(max_length=200)
    
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
    quantity = models.DecimalField(max_digits=4,decimal_places=2)
    
    def __str__(self):
        return f'{self.ingredient.name} {self.measureUnit.symbol}'


class Supplier(models.Model):
    name = models.CharField(max_length=200)
    email = models.CharField(blank=True,
                             max_length=254,
                             null=True,
                             validators=[EmailValidator(message="Email no válido")])
    web = models.CharField(max_length=200, blank=True)
    phone = models.CharField(max_length=20)
    description = models.TextField(blank=True)

    def __str__(self):
        return f'{self.name}'
    
class BuyOrder(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.DO_NOTHING)
    description = models.TextField(blank=True)
    creationAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now_add=True)
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.supplier.name}'
    
    def save(self, *args, **kwargs):
        self.updatedAt = timezone.now()
        return super().save(*args, **kwargs)

class BuyOrderDetail(models.Model):
    buyOrder = models.ForeignKey(BuyOrder, on_delete=models.CASCADE,related_name='buyOrder')
    ingredient = models.ForeignKey(Ingredient, on_delete=models.DO_NOTHING)
    measureUnit = models.ForeignKey(MeasureUnit, on_delete=models.DO_NOTHING)
    quantity = models.DecimalField(max_digits=5,decimal_places=2)
    price = models.DecimalField(max_digits=4,decimal_places=2)
    batch = models.CharField(max_length=200)
    expirationDate = models.DateField()

    def save(self, *args, **kwargs):
        if self.expirationDate < timezone.now().date():
            raise ValidationError("La fecha de expiración no puede estar en el pasado!")
        super().save(*args, **kwargs)


