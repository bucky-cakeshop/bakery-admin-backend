from datetime import date
from unittest.mock import patch
from django.test import TestCase
from bakeryAdmin import models
from bakeryAdmin.services.productionOrders.ProdcutionOrderService import *
from .fixtureUtilities import *

class GetIngredientConsumeByProductionOrderDetail(TestCase):
    @patch('bakeryAdmin.models.ProductionOrderConsume.objects')
    @patch('bakeryAdmin.models.RecipeDetail.objects')
    @patch('bakeryAdmin.models.ProductionOrderDetail.objects')
    def test_oneIngredientConsumeItem(self,productionOrderDetailMock, recipeDetailMock,productionOrderConsumeMock):
        podFixture = list([createProductionOrderDetail(id=i, quantity=4) for i in range(1,2)])
        recipe = createRecipe()
        recipeIngredientsFixture = list([createRecipeDetail(id=i,quantity=4,symbol="kg",ingredient="harina",recipe=recipe) for i in range(1,2)])
        ingredientConsumeFixture = list([createProductionOrderConsume(createProductionOrder(),createSupplierInvoiceDetail(expirationDate=datetime.datetime(2023,8,1)),16,id=i) for i in range(1,2)])

        productionOrderDetailMock.filter.return_value = podFixture
        recipeDetailMock.filter.return_value = recipeIngredientsFixture
        productionOrderConsumeMock.filter.return_value = ingredientConsumeFixture

        service = ProdcutionOrderService(1,None, productionOrderDetailMock, recipeDetailMock, None, productionOrderConsumeMock, None,None,None, None)
        actual = service.getIngredientConsumeByProductionOrderDetail()

        expected = [
            IngredientConsumeByProductionOrderDetail(
            productionOrderDetail_id=1,
            ingredientsConsumesByRecipeDetail=[
                IngredientConsumeByRecipeDetail(
                    productionOrderConsume_id=1,
                    recipeDetail_id=1,
                    ingredient_id=1,
                    measureUnit_id=1,
                    totalQuantity=16,
                    unitCostPrice=2.3,
                    expirationDate=datetime.datetime(2023,8,1)
                )
            ]
        )
        ]

        self.assertEqual(actual, expected)

    @patch('bakeryAdmin.models.ProductionOrderConsume.objects')
    @patch('bakeryAdmin.models.RecipeDetail.objects')
    @patch('bakeryAdmin.models.ProductionOrderDetail.objects')
    def test_twoIngredientConsumeItem(self,productionOrderDetailMock, recipeDetailMock,productionOrderConsumeMock):
        podFixture = list([createProductionOrderDetail(id=i, quantity=4) for i in range(1,2)])
        recipe = createRecipe()
        recipeIngredientsFixture = list([createRecipeDetail(id=i,quantity=4,symbol="kg",ingredient="harina",recipe=recipe) for i in range(1,2)])
        ingredientConsumeFixture = list(
            [createProductionOrderConsume(createProductionOrder(),createSupplierInvoiceDetail(expirationDate=datetime.datetime(2023,8,1)),8,id=i) for i in range(1,3)]
        )

        productionOrderDetailMock.filter.return_value = podFixture
        recipeDetailMock.filter.return_value = recipeIngredientsFixture
        productionOrderConsumeMock.filter.return_value = ingredientConsumeFixture

        service = ProdcutionOrderService(1,None, productionOrderDetailMock, recipeDetailMock, None, productionOrderConsumeMock, None,None,None, None)
        actual = service.getIngredientConsumeByProductionOrderDetail()

        expected = [
            IngredientConsumeByProductionOrderDetail(
            productionOrderDetail_id=1,
            ingredientsConsumesByRecipeDetail=[
                IngredientConsumeByRecipeDetail(
                    productionOrderConsume_id=1,
                    recipeDetail_id=1,
                    ingredient_id=1,
                    measureUnit_id=1,
                    totalQuantity=8,
                    unitCostPrice=2.3,
                    expirationDate=datetime.datetime(2023,8,1)
                ),
                IngredientConsumeByRecipeDetail(
                    productionOrderConsume_id=2,
                    recipeDetail_id=1,
                    ingredient_id=1,
                    measureUnit_id=1,
                    totalQuantity=8,
                    unitCostPrice=2.3,
                    expirationDate=datetime.datetime(2023,8,1)
                )
            ]
        )
        ]

        self.assertEqual(actual, expected)

    @patch('bakeryAdmin.models.ProductionOrderConsume.objects')
    @patch('bakeryAdmin.models.RecipeDetail.objects')
    @patch('bakeryAdmin.models.ProductionOrderDetail.objects')
    def test_twoRecipeDetailsTwoIngredientConsumeItem(self,productionOrderDetailMock, recipeDetailMock,productionOrderConsumeMock):
        podFixture = list([createProductionOrderDetail(id=i, quantity=4) for i in range(1,2)])
        recipe = createRecipe()
        recipeIngredientsFixture = []
        recipeIngredientsFixture.append(createRecipeDetail(id=1,quantity=4,symbol="kg",ingredient="harina",recipe=recipe))
        recipeIngredientsFixture.append(createRecipeDetail(id=2,quantity=2,symbol="kg",ingredient="azúcar",recipe=recipe))

        po = createProductionOrder()
        flourIngredientStock = createSupplierInvoiceDetail(expirationDate=datetime.datetime(2023,8,1))
        sugarIngredientStock = createSupplierInvoiceDetail(id=2,ingredient="azúcar",expirationDate=datetime.datetime(2023,8,1))
        ingredientConsumeFixture = []
        ingredientConsumeFixture.append(createProductionOrderConsume(po,flourIngredientStock,8,id=1))
        ingredientConsumeFixture.append(createProductionOrderConsume(po,flourIngredientStock,8,id=2))
        ingredientConsumeFixture.append(createProductionOrderConsume(po,sugarIngredientStock,8,id=3))

        productionOrderDetailMock.filter.return_value = podFixture
        recipeDetailMock.filter.return_value = recipeIngredientsFixture
        productionOrderConsumeMock.filter.return_value = ingredientConsumeFixture

        service = ProdcutionOrderService(1,None, productionOrderDetailMock, recipeDetailMock, None, productionOrderConsumeMock, None,None,None, None)
        actual = service.getIngredientConsumeByProductionOrderDetail()

        expected = [
            IngredientConsumeByProductionOrderDetail(
            productionOrderDetail_id=1,
            ingredientsConsumesByRecipeDetail=[
                IngredientConsumeByRecipeDetail(
                    productionOrderConsume_id=1,
                    recipeDetail_id=1,
                    ingredient_id=1,
                    measureUnit_id=1,
                    totalQuantity=8,
                    unitCostPrice=2.3,
                    expirationDate=datetime.datetime(2023,8,1)
                ),
                IngredientConsumeByRecipeDetail(
                    productionOrderConsume_id=2,
                    recipeDetail_id=1,
                    ingredient_id=1,
                    measureUnit_id=1,
                    totalQuantity=8,
                    unitCostPrice=2.3,
                    expirationDate=datetime.datetime(2023,8,1)
                ),
                IngredientConsumeByRecipeDetail(
                    productionOrderConsume_id=3,
                    recipeDetail_id=2,
                    ingredient_id=2,
                    measureUnit_id=1,
                    totalQuantity=8,
                    unitCostPrice=2.3,
                    expirationDate=datetime.datetime(2023,8,1)
                )
            ]
        )
        ]

        self.assertEqual(actual, expected)