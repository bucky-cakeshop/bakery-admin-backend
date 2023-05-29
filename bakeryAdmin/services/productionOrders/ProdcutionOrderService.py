from itertools import groupby
import json
from django.core.serializers.json import DjangoJSONEncoder
from collections import namedtuple
from decimal import Decimal
from ...models import ProductionOrderDetail, RecipeDetail, SupplierInvoiceDetail

class AggregatedIngredient:
    def __init__(self, ingredientId,ingredientName,measureUnitId,measureUnitSymbol,quantity, recipeQuantity):
        self.ingredientId = ingredientId
        self.ingredientName = ingredientName
        self.measureUnitId = measureUnitId
        self.measureUnitSymbol = measureUnitSymbol
        self.quantity = quantity
        self.recipeQuantity = recipeQuantity
        self.total = quantity*recipeQuantity

    def to_dict(self):
        return self.__dict__
    
    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)
    
    def __str__(self):
        return f'IngredientId: {self.ingredientId} measureUnitId: {self.measureUnitId} Quantity: {self.quantity} recipeQuantity: {self.recipeQuantity}'

    def __repr__(self):
        return f'IngredientId: {self.ingredientId} measureUnitId: {self.measureUnitId} Quantity: {self.quantity} recipeQuantity: {self.recipeQuantity}'

class AggregatedTotalIngredient:
    def __init__(self, ingredientId,ingredientName,measureUnitId,measureUnitSymbol,total):
        self.ingredientId = ingredientId
        self.ingredientName = ingredientName
        self.measureUnitId = measureUnitId
        self.measureUnitSymbol = measureUnitSymbol
        self.total = total

    # def __str__(self):
    #     return f'IngredientId: {self.ingredientId} measureUnitId: {self.measureUnitId} Total: {self.total}'

    # def __repr__(self):
    #     return f'IngredientId: {self.ingredientId} measureUnitId: {self.measureUnitId} Total: {self.total}'


class ProdcutionOrderService:
    def __init__(self, productionOrderId) -> None:
        self.productionOrderId = productionOrderId
    
    def calculateAggregatedIngredients(self):
        productionOrderDetails = ProductionOrderDetail.objects.filter(productionOrder_id = self.productionOrderId)
        aggregated = []
        for detail in productionOrderDetails:
            recipeDetails = RecipeDetail.objects.filter(recipe_id = detail.recipe.id)
            generator = [AggregatedIngredient(item.ingredient.id,item.ingredient.name,item.measureUnit.id,item.measureUnit.symbol,item.quantity,detail.quantity) for item in recipeDetails]
            for item in generator:
                aggregated.append(item)

        sorted_aggregated = sorted(aggregated, key=lambda AggregatedIngredient:AggregatedIngredient.ingredientId )
        aggregatedTotals = [
            {'ingredientId':key['ingId'],
             'ingredientName':key['ingName'],
             'total':sum(item.total for item in list(result)),
             'measureUnitId':key['ingUnitId'],
             'measureUnitSymbol':key['ingUnitSymbol']
             }
            for key, result in groupby(sorted_aggregated,
                                       key = lambda AggregatedIngredient:{
                                           'ingId':AggregatedIngredient.ingredientId,
                                           'ingName':AggregatedIngredient.ingredientName,
                                           'ingUnitId':AggregatedIngredient.measureUnitId,
                                           'ingUnitSymbol': AggregatedIngredient.measureUnitSymbol
                                           } )
            ]
        return aggregatedTotals
    def customAggregatedTotalIngredientDecoder(self,dict):
        return namedtuple(AggregatedTotalIngredient.__name__, dict.keys())(*dict.values())
        #return AggregatedTotalIngredient(dict['ingredientId'],dict['ingredientName'],dict['measureUnitId'],dict['measureUnitSymbol'],dict['total'])
    
    def getIngredientsFromStock(self):
        aggregatedIngredients = self.calculateAggregatedIngredients()
        for aggregatedIngredient in aggregatedIngredients:
            aggregatedIngredientObject = json.loads(json.dumps(aggregatedIngredient, cls=DjangoJSONEncoder),object_hook=self.customAggregatedTotalIngredientDecoder)
            supplierInvoiceDetail = list(SupplierInvoiceDetail.objects.filter(ingredient = aggregatedIngredientObject.ingredientId).order_by('expirationDate'))
            totalToConsume = Decimal(aggregatedIngredientObject.total)
            supplierInvoiceDetailIdx = 0
            while totalToConsume > 0:
                detail = supplierInvoiceDetail[supplierInvoiceDetailIdx]
                detail.quantityConsumed = totalToConsume
                if totalToConsume > (detail.quantityAvailable):
                    detail.quantityConsumed = detail.quantity
                supplierInvoiceDetailIdx += 1
                totalToConsume -= detail.quantity

                print(detail)
                print(totalToConsume)


