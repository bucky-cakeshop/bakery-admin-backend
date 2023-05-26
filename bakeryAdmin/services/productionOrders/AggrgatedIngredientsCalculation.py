from itertools import groupby
import json
from ...models import ProductionOrderDetail, RecipeDetail

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

class CalculateAggregatedIngredients:
    def __init__(self, productionOrderId) -> None:
        self.productionOrderId = productionOrderId
    
    def calculate(self):
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
