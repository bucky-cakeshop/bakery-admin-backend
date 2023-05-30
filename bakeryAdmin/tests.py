from unittest.mock import patch
from django.test import TestCase
from mock_django.query import QuerySetMock
from bakeryAdmin import models


from .services.productionOrders.ProdcutionOrderService import ProdcutionOrderService

class SimpleTest(TestCase):
    @patch('bakeryAdmin.models.RecipeDetail')
    @patch('bakeryAdmin.models.ProductionOrderDetail.objects')
    def test_chained_query(self,mockPod,mockRd):
        podMock = models.ProductionOrderDetail(
            productionOrder=models.ProductionOrder(title='test'),
            recipe=models.Recipe(title='Recipe test'), 
            quantity=10)
        # qsm = QuerySetMock(models.ProductionOrderDetail, podMock)
        # print(qsm.return_value.filter)
        mockPod.filter.return_value = podMock
        service = ProdcutionOrderService(1, mockPod, mockRd)
        pp = service.testUnitTesting()
        print(pp.return_value)
        #self.assertEquals('hola', service.testUnitTesting())
