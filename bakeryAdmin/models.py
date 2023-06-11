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
        return f'{self.title} {self.symbol}'

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
    quantity = models.DecimalField(max_digits=5,decimal_places=2)
    
    def __str__(self):
        return f'{self.recipe.title} {self.ingredient.name} {self.quantity} {self.measureUnit.symbol}'


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
    
class Make(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def save(self, *args, **kwargs):
        self.name = self.name.capitalize()
        return super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.name}'


class SupplierInvoice(models.Model):
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

class SupplierInvoiceDetail(models.Model):
    supplierInvoice = models.ForeignKey(SupplierInvoice, on_delete=models.CASCADE,related_name='supplierInvoice')
    ingredient = models.ForeignKey(Ingredient, on_delete=models.DO_NOTHING)
    measureUnit = models.ForeignKey(MeasureUnit, on_delete=models.DO_NOTHING)
    quantity = models.DecimalField(max_digits=5,decimal_places=2)
    price = models.DecimalField(max_digits=4,decimal_places=2)
    batch = models.CharField(max_length=200)
    expirationDate = models.DateField()
    make = models.ForeignKey(Make, on_delete=models.DO_NOTHING, default=None)
    quantityConsumed = models.DecimalField(max_digits=5,decimal_places=2, default=0)

    @property
    def quantityAvailable(self):
        return self.quantity - self.quantityConsumed

    def save(self, *args, **kwargs):
        if self.expirationDate < timezone.now().date():
            raise ValidationError("La fecha de expiración no puede estar en el pasado!")
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.ingredient.name} {self.measureUnit.symbol} {self.batch} {self.expirationDate} {self.quantity} {self.quantityConsumed} Available: {self.quantity - self.quantityConsumed}'


class ProductionOrder(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    creationAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now_add=True)
    deleted = models.BooleanField(default=False)
    startedDate = models.DateTimeField(null=True, blank=True)
    closedDate = models.DateTimeField(null=True, blank=True)
    canceledDate = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f'{self.title}'
    
    def save(self, *args, **kwargs):
        self.updatedAt = timezone.now()
        return super().save(*args, **kwargs)

class ProductionOrderDetail(models.Model):
    productionOrder = models.ForeignKey(ProductionOrder, on_delete=models.CASCADE,related_name='productionOrder')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE,related_name='productionOrder_recipe')
    quantity = models.DecimalField(max_digits=5,decimal_places=2)

class ProductionOrderConsume(models.Model):
    productionOrder = models.ForeignKey(ProductionOrder, on_delete=models.CASCADE,related_name='productionOrderConsume_productionOrder')
    supplierInvoiceDetail = models.ForeignKey(SupplierInvoiceDetail, on_delete=models.CASCADE,related_name='productionOrderConsume_supplierInvoiceDetail')
    quantity = models.DecimalField(max_digits=5,decimal_places=2)
    consumeDate = models.DateTimeField(auto_now_add=True)

class Product(models.Model):
    name = models.CharField()
    description = models.TextField(blank=True)
    recipe = models.OneToOneField(Recipe, on_delete=models.CASCADE,related_name='product_recipe')
    quantityByRecipe = models.DecimalField(max_digits=5,decimal_places=2)
    isForSell = models.BooleanField(default=False)




