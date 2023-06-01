from bakeryAdmin import models
from datetime import date
from django.utils import timezone

ingredients = {
    'harina':models.Ingredient(id=1, name="harina"),
    'azúcar':models.Ingredient(id=2, name="azúcar"),
    'nata':models.Ingredient(id=3, name="nata"),
    'chocolate':models.Ingredient(id=4, name="chocolate"),
    'mantequilla':models.Ingredient(id=5, name="mantequilla"),
    'leche':models.Ingredient(id=6, name="leche"),
    'huevo':models.Ingredient(id=7, name="huevo"),
}

measureUnits = {
    'kg':models.MeasureUnit(id=1,title="kilogramo", symbol="kg"),
    'lt':models.MeasureUnit(id=2,title="litro", symbol="lt"),
    'u':models.MeasureUnit(id=3,title="unidad", symbol="u")
}

suppliers = {
    'proveedor1':models.Supplier(id=1, name='Proveedor1', phone='111111111'),
    'proveedor2':models.Supplier(id=1, name='Proveedor2', phone='222222222'),
    'proveedor2':models.Supplier(id=1, name='Proveedor3', phone='333333333')
}

def createSupplierInvoice(id=1,supplierName='proveedor1'):
    return models.SupplierInvoice(
        id = id,
        supplier = suppliers[supplierName]
    )

def createSupplierInvoiceDetail(id=1, ingredient='harina', symbol='kg', quantity=5, quantityConsumed=0, price=2.3, batch='L1', 
                                expirationDate = timezone.now() + timezone.timedelta(days=15), quantityAvailableCalculated = 5):
    detail =  models.SupplierInvoiceDetail(
        id = id,
        ingredient = ingredients[ingredient],
        measureUnit = measureUnits[symbol],
        quantity = quantity,
        quantityConsumed = quantityConsumed,
        price = price,
        batch = batch,
        expirationDate = expirationDate
    )
    detail.quantityAvailableCalculated = quantityAvailableCalculated
    return detail
def createProductionOrder(id=1, title="PO Test"):
    return models.ProductionOrder(
        id = id, 
        title = title
    )

def createRecipe(id=1, title="R Test"):
    return models.Recipe(
        id = id, 
        title = title
    )

def createProductionOrderDetail(id=1,quantity=4):
    return models.ProductionOrderDetail(
        productionOrder = createProductionOrder(),
        recipe = createRecipe(),
        quantity = quantity
    )

def createRecipeDetail(id, quantity, ingredient, symbol):
    
    return  models.RecipeDetail(
        id = id,
        recipe = createRecipe(title="Solo harina"),
        ingredient = ingredients[ingredient],
        measureUnit = measureUnits[symbol],
        quantity = quantity
    )