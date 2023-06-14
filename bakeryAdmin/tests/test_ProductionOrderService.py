from datetime import date
from unittest.mock import patch
from django.test import TestCase
from bakeryAdmin import models
from bakeryAdmin.services.productionOrders.ProdcutionOrderService import *
from .fixtureUtilities import *

class ProductionOrderServiceTest(TestCase):

    @patch('bakeryAdmin.models.RecipeDetail.objects')
    @patch('bakeryAdmin.models.ProductionOrderDetail.objects')
    def test_calculate_aggregated_ingredients(self,productionOrderDetailMock, recipeDetailMock):
        podFixture = []
        podFixture.append(models.ProductionOrderDetail(
            productionOrder=models.ProductionOrder(title='test'),
            recipe=models.Recipe(id=1,title='Recipe test'), 
            quantity=4))
        rdFixture = []
        rdFixture.append(models.RecipeDetail(
            id=10,
            recipe=models.Recipe(id=1,title='Recipe test'), 
            ingredient = models.Ingredient(id=1,name='harina'),
            measureUnit = models.MeasureUnit(id=1,title='kilogramo',symbol='Kg.'),
            quantity = 3
        ))
        productionOrderDetailMock.filter.return_value = podFixture
        recipeDetailMock.filter.return_value = rdFixture

        service = ProdcutionOrderService(1, None, productionOrderDetailMock, recipeDetailMock, None, None,None,None)
        actual = service.calculateAggregatedIngredients()

        self.assertEqual(1,len(actual))
        self.assertEqual(1,actual[0].ingredientId)
        self.assertEqual(1,actual[0].measureUnitId)
        self.assertEqual(12,actual[0].total)
    
    @patch('bakeryAdmin.models.RecipeDetailProduct.objects')
    @patch('bakeryAdmin.models.ProductionOrderDetail.objects')
    def test_calculate_aggregated_products(self,productionOrderDetailMock, recipeDetailProductMock):
        podFixture = []
        podFixture.append(models.ProductionOrderDetail(
            productionOrder=models.ProductionOrder(title='test'),
            recipe=models.Recipe(id=1,title='Recipe test'), 
            quantity=4))
        rdpFixture = []
        rdpFixture.append(models.RecipeDetailProduct(
            id=10,
            recipe=models.Recipe(id=1,title='Recipe test'), 
            product = models.Product(id=1,name='masa base'),
            measureUnit = models.MeasureUnit(id=1,title='unitario',symbol='u.'),
            quantity = 3
        ))
        productionOrderDetailMock.filter.return_value = podFixture
        recipeDetailProductMock.filter.return_value = rdpFixture

        service = ProdcutionOrderService(1, None, productionOrderDetailMock, None, None, None,recipeDetailProductMock,None)
        actual = service.calculateAggregatedProducts()
        print(actual)

        self.assertEqual(1,len(actual))
        self.assertEqual(1,actual[0].productId)
        self.assertEqual(1,actual[0].measureUnitId)
        self.assertEqual(12,actual[0].total)


    @patch('bakeryAdmin.models.RecipeDetailProduct.objects')
    @patch('bakeryAdmin.models.ProductionOrder.objects')
    @patch('bakeryAdmin.models.ProductionOrderConsume.objects')
    @patch('bakeryAdmin.models.SupplierInvoiceDetail.objects')
    @patch('bakeryAdmin.models.RecipeDetail.objects')
    @patch('bakeryAdmin.models.ProductionOrderDetail.objects')
    def test_start_ok(self,productionOrderDetailMock, recipeDetailMock, supplierInvoiceDetailMock, productionOrderConsumeMock, productionOrderMock, recipeDetailProductMock):
        podFixture = list([createProductionOrderDetail(id=i, quantity=4) for i in range(1,2)])
        rdFixture = list([createRecipeDetail(id=i, quantity=3,ingredient='harina',symbol='kg') for i in range(1,2)])
        siFixture = list([createSupplierInvoiceDetail(id=i) for i in range(1,4)])
        poFixture = createProductionOrder()
        rdpFixture = []
        rdpFixture.append(models.RecipeDetailProduct(
            id=10,
            recipe=models.Recipe(id=1,title='Recipe test'), 
            product = models.Product(id=1,name='masa base'),
            measureUnit = models.MeasureUnit(id=1,title='unitario',symbol='u.'),
            quantity = 3
        ))


        productionOrderDetailMock.filter.return_value = podFixture
        recipeDetailMock.filter.return_value = rdFixture
        supplierInvoiceDetailMock.annotate.return_value.filter.return_value.order_by.return_value = siFixture
        productionOrderMock.get.return_value = poFixture
        recipeDetailProductMock.filter.return_value = rdpFixture
        
        service = ProdcutionOrderService(1, productionOrderMock, productionOrderDetailMock, recipeDetailMock, supplierInvoiceDetailMock, productionOrderConsumeMock, recipeDetailProductMock,None)
        actual = service.start()

        self.assertEqual(actual.status.code, ProdcutionOrderStatusEnum.OK)
        self.assertEqual(len(actual.productionOrderConsumes) , 3)
        self.assertEqual(actual.supplierInvoiceDetails[0].quantityConsumed , 5)
        self.assertEqual(actual.supplierInvoiceDetails[1].quantityConsumed , 5)
        self.assertEqual(actual.supplierInvoiceDetails[2].quantityConsumed , 2)
        self.assertEqual(actual.productionOrderConsumes[0].quantity, 5)
        self.assertEqual(actual.productionOrderConsumes[1].quantity, 5)
        self.assertEqual(actual.productionOrderConsumes[2].quantity, 2)

    @patch('bakeryAdmin.models.ProductionOrder.objects')
    @patch('bakeryAdmin.models.ProductionOrderConsume.objects')
    @patch('bakeryAdmin.models.SupplierInvoiceDetail.objects')
    @patch('bakeryAdmin.models.RecipeDetail.objects')
    @patch('bakeryAdmin.models.ProductionOrderDetail.objects')
    def test_start_missingIngredient(self,productionOrderDetailMock, recipeDetailMock, supplierInvoiceDetailMock, productionOrderConsumeMock, productionOrderMock):
        podFixture = list([createProductionOrderDetail(id=i, quantity=4) for i in range(1,2)])
        rdFixture = list([createRecipeDetail(id=i, quantity=3,ingredient='harina',symbol='kg') for i in range(1,2)])
        siFixture = list([createSupplierInvoiceDetail(id=i) for i in range(1,4)])
        siFixture[2].quantityAvailableCalculated = 1
        poFixture = createProductionOrder()

        productionOrderDetailMock.filter.return_value = podFixture
        recipeDetailMock.filter.return_value = rdFixture
        supplierInvoiceDetailMock.annotate.return_value.filter.return_value.order_by.return_value = siFixture
        productionOrderMock.get.return_value = poFixture
        
        service = ProdcutionOrderService(1, productionOrderMock, productionOrderDetailMock, recipeDetailMock, supplierInvoiceDetailMock, productionOrderConsumeMock, None,None)
        actual = service.start()

        self.assertEqual(actual.status.code, ProdcutionOrderStatusEnum.ERROR_MISSING_INGREDIENTS)
        self.assertEqual(len(actual.productionOrderConsumes), 0)
        self.assertEqual(len(actual.supplierInvoiceDetails), 0)
        self.assertEqual(len(actual.missingIngredients), 1)
        self.assertEqual(actual.missingIngredients[0].aggregatedTotalIngredient.ingredientId, 1)
        self.assertEqual(actual.missingIngredients[0].totalQuantityInStock, 11)
        self.assertEqual(actual.missingIngredients[0].totalToConsume, 12)
        

    @patch('bakeryAdmin.models.ProductionOrder.objects')
    @patch('bakeryAdmin.models.ProductionOrderConsume.objects')
    @patch('bakeryAdmin.models.SupplierInvoiceDetail.objects')
    @patch('bakeryAdmin.models.RecipeDetail.objects')
    @patch('bakeryAdmin.models.ProductionOrderDetail.objects')
    def test_start_canStart_Error(self,productionOrderDetailMock, recipeDetailMock, supplierInvoiceDetailMock, productionOrderConsumeMock, productionOrderMock):
        podFixture = list([createProductionOrderDetail(id=i, quantity=4) for i in range(1,2)])
        rdFixture = list([createRecipeDetail(id=i, quantity=3,ingredient='harina',symbol='kg') for i in range(1,2)])
        siFixture = list([createSupplierInvoiceDetail(id=i) for i in range(1,4)])
        siFixture[2].quantityAvailableCalculated = 1
        poFixture = createProductionOrder()
        poFixture.startedDate = date(2023,5,31)

        productionOrderDetailMock.filter.return_value = podFixture
        recipeDetailMock.filter.return_value = rdFixture
        supplierInvoiceDetailMock.annotate.return_value.filter.return_value.order_by.return_value = siFixture
        productionOrderMock.get.return_value = poFixture
        
        service = ProdcutionOrderService(1,productionOrderMock, productionOrderDetailMock, recipeDetailMock, supplierInvoiceDetailMock, productionOrderConsumeMock, None,None)
        actual, productionOrder = service.canStart()

        self.assertEqual(actual.status.code, ProdcutionOrderStatusEnum.ERROR_ALREADY_STARTED)
        self.assertEqual(len(actual.productionOrderConsumes), 0)
        self.assertEqual(len(actual.supplierInvoiceDetails), 0)
        self.assertEqual(len(actual.missingIngredients), 0)
        self.assertEqual(productionOrder.id, 1)
    

    @patch('bakeryAdmin.models.ProductionOrder.objects')
    @patch('bakeryAdmin.models.ProductionOrderConsume.objects')
    @patch('bakeryAdmin.models.SupplierInvoiceDetail.objects')
    def test_cancel_ok(self, supplierInvoiceDetailMock, productionOrderConsumeMock, productionOrderMock):
        siFixture = list([createSupplierInvoiceDetail(id=i) for i in range(1,4)])
        poFixture = createProductionOrder()
        poFixture.startedDate = datetime.date(2023,6,1)

        siFixture[0].quantityConsumed = 5
        siFixture[1].quantityConsumed = 5
        siFixture[2].quantityConsumed = 2

        pocFixture = []
        pocFixture.append(createProductionOrderConsume(poFixture,siFixture[0],5))
        pocFixture.append(createProductionOrderConsume(poFixture,siFixture[1],5))
        pocFixture.append(createProductionOrderConsume(poFixture,siFixture[2],2))

        supplierInvoiceDetailMock.get.return_value = siFixture[0]
        productionOrderMock.get.return_value = poFixture
        productionOrderConsumeMock.filter.return_value = [createProductionOrderConsume(poFixture,siFixture[0],5)]

        self.assertEqual(siFixture[0].quantityConsumed, 5)

        service = ProdcutionOrderService(1, productionOrderMock, None, None, supplierInvoiceDetailMock, productionOrderConsumeMock, None,None)
        actual = service.cancel()
        
        self.assertEqual(actual.status.code, ProdcutionOrderStatusEnum.OK)
        self.assertEqual(len(actual.productionOrderConsumes) , 1)
        self.assertEqual(actual.supplierInvoiceDetails[0].quantityConsumed , 0)
        self.assertEqual(actual.productionOrderConsumes[0].quantity, 5)

    def test_isCreated_ok(self):
        poFixture = createProductionOrder()
        service = ProdcutionOrderService(1,None, None, None, None, None, None,None)

        self.assertTrue(service.isCreated(poFixture))
        self.assertFalse(service.isStarted(poFixture))
        self.assertFalse(service.isCanceled(poFixture))
        self.assertFalse(service.isClosed(poFixture))

    def test_isStarted_ok(self):
        poFixture = createProductionOrder()
        poFixture.startedDate = datetime.date(2023,6,1)
        service = ProdcutionOrderService(1,None, None, None, None, None, None,None)

        self.assertFalse(service.isCreated(poFixture))
        self.assertTrue(service.isStarted(poFixture))
        self.assertFalse(service.isCanceled(poFixture))
        self.assertFalse(service.isClosed(poFixture))

    def test_isCanceled_ok(self):
        poFixture = createProductionOrder()
        poFixture.startedDate = datetime.date(2023,6,1)
        poFixture.canceledDate = datetime.date(2023,6,2)

        service = ProdcutionOrderService(1,None, None, None, None, None, None,None)

        self.assertFalse(service.isCreated(poFixture))
        self.assertFalse(service.isStarted(poFixture))
        self.assertTrue(service.isCanceled(poFixture))
        self.assertFalse(service.isClosed(poFixture))

    def test_isClosed_ok(self):
        poFixture = createProductionOrder()
        poFixture.startedDate = datetime.date(2023,6,1)
        poFixture.closedDate = datetime.date(2023,6,2)
        
        service = ProdcutionOrderService(1,None, None, None, None, None, None,None)

        self.assertFalse(service.isCreated(poFixture))
        self.assertFalse(service.isStarted(poFixture))
        self.assertFalse(service.isCanceled(poFixture))
        self.assertTrue(service.isClosed(poFixture))





