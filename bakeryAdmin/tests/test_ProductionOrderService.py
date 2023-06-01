from datetime import date
from unittest.mock import patch
from django.test import TestCase
from bakeryAdmin import models
from bakeryAdmin.services.productionOrders.ProdcutionOrderService import *
from .fixtureUtilities import *

class ProductionOrderServiceTest(TestCase):
    def test_fixtures(self):
        value = ingredients['harina']
        print(value) #.index('harina')

    @patch('bakeryAdmin.models.ProductionOrderDetail.objects')
    def test_unit_testing(self,mockPod):
        podMock = []
        podMock.append(models.ProductionOrderDetail(
            productionOrder=models.ProductionOrder(title='test'),
            recipe=models.Recipe(title='Recipe test'), 
            quantity=10))
        mockPod.filter.return_value = podMock
        service = ProdcutionOrderService(1, mockPod, None, None, None)
        actual = service.testUnitTesting()
        self.assertEquals(10, actual[0].quantity)

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

        service = ProdcutionOrderService(1, productionOrderDetailMock, recipeDetailMock, None, None)
        actual = service.calculateAggregatedIngredients()

        self.assertEqual(1,len(actual))
        self.assertEqual(1,actual[0].ingredientId)
        self.assertEqual(1,actual[0].measureUnitId)
        self.assertEqual(12,actual[0].total)

    @patch('bakeryAdmin.models.ProductionOrderConsume.objects')
    @patch('bakeryAdmin.models.SupplierInvoiceDetail.objects')
    @patch('bakeryAdmin.models.RecipeDetail.objects')
    @patch('bakeryAdmin.models.ProductionOrderDetail.objects')
    def test_start_ok(self,productionOrderDetailMock, recipeDetailMock, supplierInvoiceDetailMock, productionOrderConsumeMock):
        podFixture = list([createProductionOrderDetail(id=i, quantity=4) for i in range(1,2)])
        rdFixture = list([createRecipeDetail(id=i, quantity=3,ingredient='harina',symbol='kg') for i in range(1,2)])
        siFixture = list([createSupplierInvoiceDetail(id=i) for i in range(1,4)])

        productionOrderDetailMock.filter.return_value = podFixture
        recipeDetailMock.filter.return_value = rdFixture
        supplierInvoiceDetailMock.annotate.return_value.filter.return_value.order_by.return_value = siFixture
        
        service = ProdcutionOrderService(1, productionOrderDetailMock, recipeDetailMock, supplierInvoiceDetailMock, productionOrderConsumeMock)
        actual = service.start()

        self.assertEqual(actual.status, ProdcutionOrderStatusEnum.OK)
        self.assertEqual(len(actual.productionOrderConsumes) , 3)
        self.assertEqual(actual.supplierInvoiceDetails[0].quantityConsumed , 5)
        self.assertEqual(actual.supplierInvoiceDetails[1].quantityConsumed , 5)
        self.assertEqual(actual.supplierInvoiceDetails[2].quantityConsumed , 2)
        self.assertEqual(actual.productionOrderConsumes[0].quantityConsumed , 5)
        self.assertEqual(actual.productionOrderConsumes[1].quantityConsumed , 5)
        self.assertEqual(actual.productionOrderConsumes[2].quantityConsumed , 2)

    @patch('bakeryAdmin.models.ProductionOrderConsume.objects')
    @patch('bakeryAdmin.models.SupplierInvoiceDetail.objects')
    @patch('bakeryAdmin.models.RecipeDetail.objects')
    @patch('bakeryAdmin.models.ProductionOrderDetail.objects')
    def test_start_missingIngredient(self,productionOrderDetailMock, recipeDetailMock, supplierInvoiceDetailMock, productionOrderConsumeMock):
        podFixture = list([createProductionOrderDetail(id=i, quantity=4) for i in range(1,2)])
        rdFixture = list([createRecipeDetail(id=i, quantity=3,ingredient='harina',symbol='kg') for i in range(1,2)])
        siFixture = list([createSupplierInvoiceDetail(id=i) for i in range(1,4)])
        siFixture[2].quantityAvailableCalculated = 1

        productionOrderDetailMock.filter.return_value = podFixture
        recipeDetailMock.filter.return_value = rdFixture
        supplierInvoiceDetailMock.annotate.return_value.filter.return_value.order_by.return_value = siFixture
        
        service = ProdcutionOrderService(1, productionOrderDetailMock, recipeDetailMock, supplierInvoiceDetailMock, productionOrderConsumeMock)
        actual = service.start()

        self.assertEqual(actual.status, ProdcutionOrderStatusEnum.ERROR_MISSING_INGREDIENTS)
        self.assertEqual(len(actual.productionOrderConsumes), 0)
        self.assertEqual(len(actual.supplierInvoiceDetails), 0)
        self.assertEqual(len(actual.missingIngredients), 1)
        self.assertEqual(actual.missingIngredients[0].aggregatedTotalIngredient.ingredientId, 1)
        self.assertEqual(actual.missingIngredients[0].totalQuantityInStock, 11)
        self.assertEqual(actual.missingIngredients[0].totalToConsume, 12)
        






