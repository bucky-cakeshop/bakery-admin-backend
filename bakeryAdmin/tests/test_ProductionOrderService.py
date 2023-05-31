from datetime import date
from unittest.mock import patch
from django.test import TestCase
from bakeryAdmin import models
from bakeryAdmin.services.productionOrders.ProdcutionOrderService import ProdcutionOrderService

class ProductionOrderServiceTest(TestCase):
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
    @patch('bakeryAdmin.models.SupplierInvoiceDetail.save')
    @patch('bakeryAdmin.models.SupplierInvoiceDetail.objects')
    @patch('bakeryAdmin.models.RecipeDetail.objects')
    @patch('bakeryAdmin.models.ProductionOrderDetail.objects')
    def test_getIngredientsFromStock(self,productionOrderDetailMock, recipeDetailMock, supplierInvoiceDetailMock,supplierInvoiceDetailSaveMock, productionOrderConsumeMock):
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
        siFixture = []
        siFixture.append(
            models.SupplierInvoiceDetail(
            id = 1,
            supplierInvoice = models.SupplierInvoice(1, models.Supplier(1,name = 'proveedor 1', phone='99999999')),
            ingredient = models.Ingredient(id=1,name='harina'),
            measureUnit = models.MeasureUnit(id=1,title='kilogramo',symbol='Kg.'),
            quantity = 5,
            price = 2.3,
            batch = 'L1',
            expirationDate = date(2023,8,1)
        ))
        siFixture.append(
            models.SupplierInvoiceDetail(
            id = 1,
            supplierInvoice = models.SupplierInvoice(1, models.Supplier(1,name = 'proveedor 1', phone='99999999')),
            ingredient = models.Ingredient(id=1,name='harina'),
            measureUnit = models.MeasureUnit(id=1,title='kilogramo',symbol='Kg.'),
            quantity = 5,
            price = 2.3,
            batch = 'L2',
            expirationDate = date(2023,8,2)
        ))
        siFixture.append(
            models.SupplierInvoiceDetail(
            id = 1,
            supplierInvoice = models.SupplierInvoice(1, models.Supplier(1,name = 'proveedor 1', phone='99999999')),
            ingredient = models.Ingredient(id=1,name='harina'),
            measureUnit = models.MeasureUnit(id=1,title='kilogramo',symbol='Kg.'),
            quantity = 5,
            price = 2.3,
            batch = 'L3',
            expirationDate = date(2023,8,3)
        ))
        productionOrderDetailMock.filter.return_value = podFixture
        recipeDetailMock.filter.return_value = rdFixture
        supplierInvoiceDetailMock.filter.return_value.order_by.return_value = siFixture

        service = ProdcutionOrderService(1, productionOrderDetailMock, recipeDetailMock, supplierInvoiceDetailMock, productionOrderConsumeMock)
        actual = service.getIngredientsFromStock()
        self.assertTrue(supplierInvoiceDetailSaveMock.called)
        






