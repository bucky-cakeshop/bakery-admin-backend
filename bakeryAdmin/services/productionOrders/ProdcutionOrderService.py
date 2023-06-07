import datetime
from enum import Enum
from itertools import groupby
import json
from dataclasses import dataclass
from collections import namedtuple
from decimal import Decimal
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import F, Sum

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

@dataclass
class ProductionOrderConsumeItem:
    productionOrderId: int
    supplierInvoiceDetailId: int
    quantityConsumed: float

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


    

@dataclass
class ProdcutionOrderStatus:
    status: ResultStatus
    supplierInvoiceDetails: list
    productionOrderConsumes: list[ProductionOrderConsumeItem]
    missingIngredients: list
    isOk:bool

    @staticmethod
    def ofOk():
        return ProdcutionOrderStatus(ResultStatus.ofOk(),[],[],[],True)

    @staticmethod
    def ofMissingIngredient():
        return ProdcutionOrderStatus(ResultStatus.ofMissingIngredient(),[],[],[], False)

    @staticmethod
    def ofAlreadyStarted():
        return ProdcutionOrderStatus(ResultStatus.ofAlreadyStarted(),[],[],[], False)

    @staticmethod
    def ofAlreadyCanceled():
        return ProdcutionOrderStatus(ResultStatus.ofAlreadyCanceled(),[],[],[], False)

    @staticmethod
    def ofAlreadyClosed():
        return ProdcutionOrderStatus(ResultStatus.ofAlreadyClosed(),[],[],[], False)

    @staticmethod
    def ofCanceledCantClose():
        return ProdcutionOrderStatus(ResultStatus.ofCanceledCantClose(),[],[],[], False)

    @staticmethod
    def ofShouldStart():
        return ProdcutionOrderStatus(ResultStatus.ofShouldStart(),[],[],[])

    def to_dict(self):
        return self.__dict__

    def toJson(self):
        return json.dumps(self, 
                            default=lambda o: {o} if (isinstance(o,Decimal) or isinstance(o,float) or isinstance(o,datetime.date)) else o.__dict__, 
            sort_keys=True, indent=4, cls=DjangoJSONEncoder)
      


class ProdcutionOrderService:
    def __init__(self, productionOrderId, poObjects, poDetailsObjects, rDetailsObjects, siDetailsObjects, poConsumeObjects) -> None:
        self.poObjects = poObjects
        self.productionOrderId = productionOrderId
        self.poDetailsObjects = poDetailsObjects
        self.rDetailsObjects = rDetailsObjects
        self.siDetailsObjects = siDetailsObjects
        self.poConsumeObjects = poConsumeObjects
    
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

    def canStart(self) -> tuple[ProdcutionOrderStatus, object]:
        productionOrder = self.poObjects.get(id = self.productionOrderId)
        
        if(self.isCreated(productionOrder=productionOrder) or self.isCanceled(productionOrder=productionOrder)):
            result = ProdcutionOrderStatus.ofOk()
        
        elif(self.isStarted(productionOrder=productionOrder)):
            result = ProdcutionOrderStatus.ofAlreadyStarted()
        
        elif(self.isClosed(productionOrder=productionOrder)):
            result = ProdcutionOrderStatus.ofAlreadyClosed()

        return result, productionOrder

    def canCancel(self) -> tuple[ProdcutionOrderStatus, object]:
        productionOrder = self.poObjects.get(id = self.productionOrderId)
        
        if(self.isStarted(productionOrder=productionOrder)):
            result = ProdcutionOrderStatus.ofOk()
        
        elif(self.isCreated(productionOrder=productionOrder)):
            result = ProdcutionOrderStatus.ofShouldStart()
        
        elif(self.isClosed(productionOrder=productionOrder)):
            result = ProdcutionOrderStatus.ofAlreadyClosed()
        
        elif(self.isCanceled(productionOrder=productionOrder)):
            result = ProdcutionOrderStatus.ofAlreadyCanceled()
        
        return result, productionOrder

    def canClose(self) -> tuple[ProdcutionOrderStatus, object]:
        productionOrder = self.poObjects.get(id = self.productionOrderId)
        
        if(self.isStarted(productionOrder=productionOrder)):
            result = ProdcutionOrderStatus.ofOk()
        
        elif(self.isCreated(productionOrder=productionOrder)):
            result = ProdcutionOrderStatus.ofShouldStart()
        
        elif(self.isClosed(productionOrder=productionOrder)):
            result = ProdcutionOrderStatus.ofAlreadyClosed()
        
        elif(self.isCanceled(productionOrder=productionOrder)):
            result = ProdcutionOrderStatus.ofCanceledCantClose()
        
        return result, productionOrder

    def start(self) -> ProdcutionOrderStatus:
        aggregatedIngredients = self.calculateAggregatedIngredients()
        for aggregatedIngredient in aggregatedIngredients:
            totalToConsume = Decimal(aggregatedIngredient.total)
            poStatus = ProdcutionOrderStatus.ofOk()
           
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
    
    def cancel(self) -> ProdcutionOrderStatus:
        poStatus = ProdcutionOrderStatus.ofOk()
        return poStatus

    def close(self) -> ProdcutionOrderStatus:
        poStatus = ProdcutionOrderStatus.ofOk()
        return poStatus

