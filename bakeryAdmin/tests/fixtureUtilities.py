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

products = {
    'masa alfajores de maicena':models.Product(id=1, name="masa alfajores de maicena"),
    'masa base tarta':models.Product(id=2, name="masa base tarta")
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

def createProductStock(id=1, product='masa base tarta', symbol='kg', quantity=5, quantityConsumed=0, costPrice=2.3, sellPrice=3.3, batch='L1', 
                                expirationDate = timezone.now() + timezone.timedelta(days=15), quantityAvailableCalculated = 5):
    detail =  models.ProductStock(
        id = id,
        product = products[product],
        measureUnit = measureUnits[symbol],
        quantity = quantity,
        quantityConsumed = quantityConsumed,
        unitCostPrice = costPrice,
        unitSellPrice = sellPrice,
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
def createRecipeDetailProduct(id, recipe, quantity, product, symbol):
    return models.RecipeDetailProduct(
            id=id,
            recipe=recipe, 
            product = products[product],
            measureUnit = measureUnits[symbol],
            quantity = quantity
        )

def createProductionOrderConsume(productionOrder,supplierInvoiceDetail,quantity) -> models.ProductionOrderConsume:
    return models.ProductionOrderConsume (
        productionOrder =productionOrder,
        supplierInvoiceDetail = supplierInvoiceDetail,
        quantity = quantity
    )

def createProductionOrderConsumeProduct(productionOrder,productStock,quantity) -> models.ProductionOrderConsumeProduct:
    return models.ProductionOrderConsumeProduct (
        productionOrder =productionOrder,
        productStock = productStock,
        quantity = quantity
    )

def createProduct(recipe,id=1,name="Producto masa", description="Producto masa desc", quantityByRecipe=12, measureUnit="u", isForSell=True) -> models.Product:
    return models.Product(
        id=id,
        recipe = recipe,
        name = name,
        description = description, 
        quantityByRecipe = quantityByRecipe,
        measureUnit = measureUnits[measureUnit],
        isForSell = isForSell
    )
