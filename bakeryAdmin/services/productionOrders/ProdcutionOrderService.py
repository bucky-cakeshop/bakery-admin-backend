import datetime
from enum import Enum
from itertools import groupby
import json
from dataclasses import dataclass
from collections import namedtuple
from decimal import Decimal
from typing import List
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import F
from django.utils import timezone
from operator import attrgetter, itemgetter

from bakeryAdmin.domain.models.production.AggregatedProduct import AggregatedProduct
from bakeryAdmin.domain.models.production.AggregatedTotalProduct import AggregatedTotalProduct
from bakeryAdmin.domain.models.production.ConsumeByProductionOrderDetail import ConsumeByProductionOrderDetail
from bakeryAdmin.domain.models.production.ConsumeByRecipeDetail import ConsumeByRecipeDetail, IngredientConsumeByRecipeDetail
from bakeryAdmin.domain.models.production.ProductionOrderConsumeProductItem import ProductionOrderConsumeProductItem
from bakeryAdmin.domain.models.production.ProductionOrderMissingProductItem import ProductionOrderMissingProductItem
from bakeryAdmin.domain.models.production.ProductStockToAdd import ProductStockToAdd

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

    def to_dict(self):
        return self.__dict__
    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)


    def __str__(self):
        return f'IngredientId: {self.ingredientId} measureUnitId: {self.measureUnitId} Total: {self.total}'

    def __repr__(self):
        return f'IngredientId: {self.ingredientId} measureUnitId: {self.measureUnitId} Total: {self.total}'

class ProdcutionOrderStatusEnum(int, Enum):
    OK = 1
    ERROR_MISSING_INGREDIENTS = 2
    ERROR_ALREADY_STARTED = 3
    ERROR_ALREADY_CANCELED = 4
    ERROR_ALREADY_CLOSED = 5
    ERROR_CANCELED_CANT_CLOSE = 6
    ERROR_SHOULD_START = 7
    ERROR_MISSING_PRODUCTS = 8

@dataclass
class ProductionOrderConsumeItem:
    productionOrder_id: int
    supplierInvoiceDetail_id: int
    quantity: float

    def to_dict(self):
        return self.__dict__

    def toJson(self):
        return json.dumps(self, default=lambda o: str(o) if (isinstance(o,float) or isinstance(o,Decimal)) else o.__dict__, 
            sort_keys=True, indent=4)

@dataclass
class ProductionOrderMissingItem:
    aggregatedTotalIngredient:AggregatedTotalIngredient
    totalQuantityInStock:float
    totalToConsume:float
                        
@dataclass
class ResultStatus:
    code: ProdcutionOrderStatusEnum
    message: str

    @staticmethod
    def ofOk():
        return ResultStatus(ProdcutionOrderStatusEnum.OK,"Success")

    @staticmethod
    def ofMissingIngredient():
        return ResultStatus(ProdcutionOrderStatusEnum.ERROR_MISSING_INGREDIENTS,"Missed ingredients")
            
    @staticmethod
    def ofAlreadyStarted():
        return ResultStatus(ProdcutionOrderStatusEnum.ERROR_ALREADY_STARTED,"Production order already started")

    @staticmethod
    def ofAlreadyCanceled():
        return ResultStatus(ProdcutionOrderStatusEnum.ERROR_ALREADY_CANCELED,"Production order already canceled")
    
    @staticmethod
    def ofAlreadyClosed():
        return ResultStatus(ProdcutionOrderStatusEnum.ERROR_ALREADY_CLOSED,"Production order already closed")
    
    @staticmethod
    def ofCanceledCantClose():
        return ResultStatus(ProdcutionOrderStatusEnum.ERROR_CANCELED_CANT_CLOSE,"Production order canceled cant close")

    @staticmethod
    def ofShouldStart():
        return ResultStatus(ProdcutionOrderStatusEnum.ERROR_SHOULD_START,"Production order should start")
    
    @staticmethod
    def ofMissingProduct():
        return ResultStatus(ProdcutionOrderStatusEnum.ERROR_MISSING_PRODUCTS,"Missed products")



    

@dataclass
class ProductionOrderStatus:
    status: ResultStatus
    supplierInvoiceDetails: list
    productionOrderConsumes: list[ProductionOrderConsumeItem]
    missingIngredients: list
    productStock: list
    productionOrderConsumesProduct: list[ProductionOrderConsumeProductItem]
    missingProducts: list

    @property
    def isOk(self):
        return len(self.missingIngredients) <= 0 and len(self.missingProducts) <= 0

    @staticmethod
    def ofOk():
        return ProductionOrderStatus(ResultStatus.ofOk(),[],[],[],[],[],[])

    @staticmethod
    def ofMissingIngredient():
        return ProductionOrderStatus(ResultStatus.ofMissingIngredient(),[],[],[],[],[],[])

    @staticmethod
    def ofMissingProduct():
        return ProductionOrderStatus(ResultStatus.ofMissingProduct(),[],[],[],[],[],[])

    @staticmethod
    def ofAlreadyStarted():
        return ProductionOrderStatus(ResultStatus.ofAlreadyStarted(),[],[],[],[],[],[])

    @staticmethod
    def ofAlreadyCanceled():
        return ProductionOrderStatus(ResultStatus.ofAlreadyCanceled(),[],[],[],[],[],[])

    @staticmethod
    def ofAlreadyClosed():
        return ProductionOrderStatus(ResultStatus.ofAlreadyClosed(),[],[],[],[],[],[])

    @staticmethod
    def ofCanceledCantClose():
        return ProductionOrderStatus(ResultStatus.ofCanceledCantClose(),[],[],[],[],[],[])

    @staticmethod
    def ofShouldStart():
        return ProductionOrderStatus(ResultStatus.ofShouldStart(),[],[],[],[],[],[])

    def to_dict(self):
        return self.__dict__

    def toJson(self):
        return json.dumps(self, 
                            default=lambda o: {o} if (isinstance(o,Decimal) or isinstance(o,float) or isinstance(o,datetime.date)) else o.__dict__, 
            sort_keys=True, indent=4, cls=DjangoJSONEncoder)
      


class ProdcutionOrderService:
    def __init__(self, productionOrderId, poObjects, poDetailsObjects, rDetailsObjects, siDetailsObjects, poConsumeObjects, rDetailsProductObjects, pStockObjects, poConsumeProducObjects, productObjects) -> None:
        self.poObjects = poObjects
        self.productionOrderId = productionOrderId
        self.poDetailsObjects = poDetailsObjects
        self.rDetailsObjects = rDetailsObjects
        self.siDetailsObjects = siDetailsObjects
        self.poConsumeObjects = poConsumeObjects
        self.rDetailsProductObjects = rDetailsProductObjects
        self.pStockObjects = pStockObjects
        self.poConsumeProductObjects = poConsumeProducObjects
        self.productObjects = productObjects
    
    def calculateAggregatedIngredients(self) -> list[AggregatedTotalIngredient]:
        productionOrderDetails = self.poDetailsObjects.filter(productionOrder_id = self.productionOrderId)
        aggregated = []
        for detail in productionOrderDetails:
            recipeDetails = self.rDetailsObjects.filter(recipe_id = detail.recipe.id)
            generator = [
                AggregatedIngredient(
                item.ingredient.id,
                item.ingredient.name,
                item.measureUnit.id,
                item.measureUnit.symbol,
                item.quantity,
                detail.quantity) 
                for item in recipeDetails]
            for item in generator:
                aggregated.append(item)

        sorted_aggregated = sorted(aggregated, key=lambda AggregatedIngredient:AggregatedIngredient.ingredientId )
        aggregatedTotals = [
            AggregatedTotalIngredient(
            key['ingId'],
            key['ingName'],
            key['ingUnitId'],
            key['ingUnitSymbol'],
            sum(item.total for item in list(result))
            )
            for key, result in groupby(sorted_aggregated,
                                       key = lambda AggregatedIngredient:{
                                           'ingId':AggregatedIngredient.ingredientId,
                                           'ingName':AggregatedIngredient.ingredientName,
                                           'ingUnitId':AggregatedIngredient.measureUnitId,
                                           'ingUnitSymbol': AggregatedIngredient.measureUnitSymbol
                                           } )
            ]

        return aggregatedTotals
    
    def calculateAggregatedProducts(self) -> list[AggregatedTotalProduct]:
        productionOrderDetails = self.poDetailsObjects.filter(productionOrder_id = self.productionOrderId)
        aggregated = []
        for detail in productionOrderDetails:
            recipeDetailsProduct = self.rDetailsProductObjects.filter(recipe_id = detail.recipe.id)
            generator = [
                AggregatedProduct(
                item.product.id,
                item.product.name,
                item.measureUnit.id,
                item.measureUnit.symbol,
                item.quantity,
                detail.quantity) 
                for item in recipeDetailsProduct]
            for item in generator:
                aggregated.append(item)

        sorted_aggregated = sorted(aggregated, key=lambda AggregatedProduct:AggregatedProduct.productId )
        aggregatedTotals = [
            AggregatedTotalProduct(
            key['prodId'],
            key['prodName'],
            key['prodUnitId'],
            key['prodUnitSymbol'],
            sum(item.total for item in list(result))
            )
            for key, result in groupby(sorted_aggregated,
                                       key = lambda AggregatedProduct:{
                                           'prodId':AggregatedProduct.productId,
                                           'prodName':AggregatedProduct.productName,
                                           'prodUnitId':AggregatedProduct.measureUnitId,
                                           'prodUnitSymbol': AggregatedProduct.measureUnitSymbol
                                           } )
            ]

        return aggregatedTotals


    def customAggregatedTotalIngredientDecoder(self,dict):
        return namedtuple(AggregatedTotalIngredient.__name__, dict.keys())(*dict.values())

    def isCreated(self, productionOrder) -> bool:
        return productionOrder.startedDate == None and productionOrder.canceledDate == None and productionOrder.closedDate == None

    def isStarted(self, productionOrder) -> bool:
        return productionOrder.startedDate != None and productionOrder.canceledDate == None and productionOrder.closedDate == None
    
    def isCanceled(self, productionOrder) -> bool:
        return productionOrder.startedDate != None and productionOrder.canceledDate != None and productionOrder.closedDate == None
    
    def isClosed(self, productionOrder) -> bool:
        return productionOrder.startedDate != None and productionOrder.canceledDate == None and productionOrder.closedDate != None

    def canStart(self) -> tuple[ProductionOrderStatus, object]:
        productionOrder = self.poObjects.get(id = self.productionOrderId)
        
        if(self.isCreated(productionOrder=productionOrder) or self.isCanceled(productionOrder=productionOrder)):
            result = ProductionOrderStatus.ofOk()
        
        elif(self.isStarted(productionOrder=productionOrder)):
            result = ProductionOrderStatus.ofAlreadyStarted()
        
        elif(self.isClosed(productionOrder=productionOrder)):
            result = ProductionOrderStatus.ofAlreadyClosed()

        return result, productionOrder

    def canCancel(self) -> tuple[ProductionOrderStatus, object]:
        productionOrder = self.poObjects.get(id = self.productionOrderId)
        
        if(self.isStarted(productionOrder=productionOrder)):
            result = ProductionOrderStatus.ofOk()
        
        elif(self.isCreated(productionOrder=productionOrder)):
            result = ProductionOrderStatus.ofShouldStart()
        
        elif(self.isClosed(productionOrder=productionOrder)):
            result = ProductionOrderStatus.ofAlreadyClosed()
        
        elif(self.isCanceled(productionOrder=productionOrder)):
            result = ProductionOrderStatus.ofAlreadyCanceled()
        
        return result, productionOrder

    def canClose(self) -> tuple[ProductionOrderStatus, object]:
        productionOrder = self.poObjects.get(id = self.productionOrderId)
        
        if(self.isStarted(productionOrder=productionOrder)):
            result = ProductionOrderStatus.ofOk()
        
        elif(self.isCreated(productionOrder=productionOrder)):
            result = ProductionOrderStatus.ofShouldStart()
        
        elif(self.isClosed(productionOrder=productionOrder)):
            result = ProductionOrderStatus.ofAlreadyClosed()
        
        elif(self.isCanceled(productionOrder=productionOrder)):
            result = ProductionOrderStatus.ofCanceledCantClose()
        
        return result, productionOrder

    def start(self) -> ProductionOrderStatus:
        poStatus = ProductionOrderStatus.ofOk()
        aggregatedIngredients = self.calculateAggregatedIngredients()
        aggregatedProducts = self.calculateAggregatedProducts()
        
        self.calculateConsumedIngredients(aggregatedIngredients, poStatus)
        self.calculateConsumedProducts(aggregatedProducts, poStatus)
        return poStatus

    def calculateConsumedIngredients(self, aggregatedIngredients, poStatus):
        for aggregatedIngredient in aggregatedIngredients:
            totalToConsume = Decimal(aggregatedIngredient.total)
                       
            supplierInvoiceDetail = list(self.siDetailsObjects
                                         .annotate(quantityAvailableCalculated=F('quantity')-F('quantityConsumed'))
                                         .filter(ingredient = aggregatedIngredient.ingredientId, quantityAvailableCalculated__gt = 0)
                                         .order_by('expirationDate'))
            totalInDetails = sum(item.quantityAvailableCalculated for item in supplierInvoiceDetail)

            if totalToConsume > totalInDetails:
                poStatus.status = ResultStatus.ofMissingIngredient()
                poStatus.missingIngredients.append(
                    ProductionOrderMissingItem(aggregatedIngredient,totalInDetails,totalToConsume)
                )
            else:
                for detail in supplierInvoiceDetail:
                    if(totalToConsume < detail.quantityAvailable):
                        detail.quantityConsumed += totalToConsume
                    else:
                        detail.quantityConsumed += detail.quantityAvailable
                    totalToConsume -= detail.quantityConsumed
                    poStatus.supplierInvoiceDetails.append(detail)
                    poStatus.productionOrderConsumes.append(ProductionOrderConsumeItem(self.productionOrderId,detail.id,detail.quantityConsumed))      
            
            return poStatus

    def calculateConsumedProducts(self, aggregatedProducts, poStatus):
        for aggregatedProduct in aggregatedProducts:
            totalToConsume = Decimal(aggregatedProduct.total)
                       
            productStock = list(self.pStockObjects
                                         .annotate(quantityAvailableCalculated=F('quantity')-F('quantityConsumed'))
                                         .filter(product = aggregatedProduct.productId, quantityAvailableCalculated__gt = 0)
                                         .order_by('expirationDate'))
            totalInDetails = sum(item.quantityAvailableCalculated for item in productStock)

            if totalToConsume > totalInDetails:
                poStatus.status = ResultStatus.ofMissingProduct()
                poStatus.missingProducts.append(
                    ProductionOrderMissingProductItem(aggregatedProduct,totalInDetails,totalToConsume)
                )
            else:
                for detail in productStock:
                    if(totalToConsume < detail.quantityAvailable):
                        detail.quantityConsumed += totalToConsume
                    else:
                        detail.quantityConsumed += detail.quantityAvailable
                    totalToConsume -= detail.quantityConsumed
                    poStatus.productStock.append(detail)
                    poStatus.productionOrderConsumesProduct.append(ProductionOrderConsumeProductItem(
                        self.productionOrderId,
                        detail.id,
                        detail.quantityConsumed
                        )
                        )           
            return poStatus


    def cancel(self) -> ProductionOrderStatus:
        poStatus = ProductionOrderStatus.ofOk()
        poStatus.productionOrderConsumes = self.poConsumeObjects.filter(productionOrder_id = self.productionOrderId)
        poStatus.productionOrderConsumesProduct = self.poConsumeProductObjects.filter(productionOrder_id = self.productionOrderId)
        for poConsume in poStatus.productionOrderConsumes:
            siDetail = self.siDetailsObjects.get(id = poConsume.supplierInvoiceDetail.id)
            siDetail.quantityConsumed = siDetail.quantityConsumed - poConsume.quantity
            poStatus.supplierInvoiceDetails.append(siDetail)
        for poProdConsume in poStatus.productionOrderConsumesProduct:
            prodStock = self.pStockObjects.get(id = poProdConsume.productStock_id)
            prodStock.quantityConsumed = prodStock.quantityConsumed - poProdConsume.quantity
            poStatus.productStock.append(prodStock)

        return poStatus

    def close(self) -> ProductionOrderStatus:
        poStatus = ProductionOrderStatus.ofOk()
        productionOrderDetails = self.poDetailsObjects.filter(productionOrder_id = self.productionOrderId)

        for productionOrderDetail in productionOrderDetails:
            productDetails = self.getConsumesByProductionOrderDetail(productionOrderDetail)
            product = self.productObjects.get(recipe_id = productionOrderDetail.recipe_id)
            quantity = product.quantityByRecipe * productionOrderDetail.quantity
            unitCostPrice = productDetails.costPrice/quantity
            unitSellPrice = unitCostPrice * product.utilityMultiplier
            poStatus.productStock.append(
                ProductStockToAdd(
                productId = product.id,
                measureUnitId = product.measureUnit_id,
                quantity = quantity,
                quantityConsumed = 0,
                isForSell = product.isForSell,
                batch = productDetails.batch,
                expirationDate = productDetails.expirationDate,
                unitCostPrice = unitCostPrice,
                unitSellPrice = unitSellPrice
                )
            )
        return poStatus

    def getConsumesByProductionOrderDetail(self, productionOrderDetail) -> ConsumeByProductionOrderDetail:
        ingredientsByRecipe = self.getIngredientsConsumesByProductionOrderDetail(productionOrderDetail)
        productsByRecipe = self.getProductsConsumesByProductionOrderDetail(productionOrderDetail)

        ingredientConsumeByProductionOrderDetail = ConsumeByProductionOrderDetail.of(productionOrderDetail.id)
        ingredientConsumeByProductionOrderDetail.consumesByRecipeDetail.extend(ingredientsByRecipe)
        ingredientConsumeByProductionOrderDetail.consumesByRecipeDetail.extend(productsByRecipe)
            
        ingredientConsumeByProductionOrderDetail.expirationDate = min(
            [item.expirationDate for item in ingredientConsumeByProductionOrderDetail.consumesByRecipeDetail]
        )
        
        ingredientConsumeByProductionOrderDetail.costPrice = round(
            sum((detail.unitCostPrice * detail.totalQuantity) for detail in ingredientConsumeByProductionOrderDetail.consumesByRecipeDetail),
            2)
        ingredientConsumeByProductionOrderDetail.batch = ProdcutionOrderService.getBatchNumber()

        return ingredientConsumeByProductionOrderDetail

    def getIngredientsConsumesByProductionOrderDetail(self, productionOrderDetail) -> List[ConsumeByRecipeDetail]:
        ingredientsConsumes = self.poConsumeObjects.filter(productionOrder_id = self.productionOrderId)

        recipeDetails = self.rDetailsObjects.filter(recipe_id = productionOrderDetail.recipe_id)

        consumeByRecipeDetail = []
        for recipeDetail in recipeDetails:
            # Get production order consumes by recipe ingredient
            itemConsumed = [
                ConsumeByRecipeDetail(
                    recipeDetail_id = recipeDetail.id,
                    totalQuantity = consumed.quantity,
                    expirationDate = consumed.supplierInvoiceDetail.expirationDate,
                    unitCostPrice = consumed.supplierInvoiceDetail.price,
                ) 
                for consumed in ingredientsConsumes if consumed.supplierInvoiceDetail.ingredient_id == recipeDetail.ingredient_id]
            
            consumeByRecipeDetail.extend(itemConsumed)
            
        return consumeByRecipeDetail

    def getProductsConsumesByProductionOrderDetail(self, productionOrderDetail) -> List[ConsumeByRecipeDetail]:
        productsConsumes = self.poConsumeProductObjects.filter(productionOrder_id = self.productionOrderId)

        recipeDetailsProduct = self.rDetailsProductObjects.filter(recipe_id = productionOrderDetail.recipe_id)

        consumeByRecipeDetail = []
        for recipeDetail in recipeDetailsProduct:
            ingredientConsumed = [
                ConsumeByRecipeDetail(
                    recipeDetail_id = recipeDetail.id,
                    totalQuantity = consumed.quantity,
                    expirationDate = consumed.productStock.expirationDate,
                    unitCostPrice = consumed.productStock.unitCostPrice,
                ) 
                for consumed in productsConsumes if consumed.productStock.product_id == recipeDetail.product_id]
            
            consumeByRecipeDetail.extend(ingredientConsumed)
        return consumeByRecipeDetail

    def getConsumesByProductionOrder(self) -> List[ConsumeByProductionOrderDetail]:
        productionOrderDetails = self.poDetailsObjects.filter(productionOrder_id = self.productionOrderId)

        consumesByProductionOrderDetail = []
        for productionOrderDetail in productionOrderDetails:
            ingredientConsumeByProductionOrderDetail = self.getConsumesByProductionOrderDetail(productionOrderDetail)
            consumesByProductionOrderDetail.append(ingredientConsumeByProductionOrderDetail)
        return consumesByProductionOrderDetail
    
    @classmethod
    def getBatchNumber(self) -> str:
        return datetime.date.today().strftime("%Y%m%d")
                


