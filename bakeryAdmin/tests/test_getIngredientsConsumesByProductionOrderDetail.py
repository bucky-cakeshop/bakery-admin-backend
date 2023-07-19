from datetime import date
from unittest.mock import patch
from django.test import TestCase
from bakeryAdmin import models
from bakeryAdmin.services.productionOrders.ProdcutionOrderService import *
from .fixtureUtilities import *

class GetIngredientConsumeByProductionOrderDetail(TestCase):

    @patch('bakeryAdmin.models.RecipeDetailProduct.objects')
    @patch('bakeryAdmin.models.ProductionOrderConsumeProduct.objects')    
    @patch('bakeryAdmin.models.ProductionOrderConsume.objects')
    @patch('bakeryAdmin.models.RecipeDetail.objects')
    @patch('bakeryAdmin.models.ProductionOrderDetail.objects')
    def test_oneIngredientConsumeItem(self,productionOrderDetailMock, recipeDetailMock,productionOrderConsumeMock, productionOrderConsumeProductMock, recipeDetailProductMock):

        recipe = createRecipe()
        recipeIngredientsFixture = []
        recipeIngredientsFixture.append(createRecipeDetail(id=1,quantity=4,symbol="kg",ingredient="harina",recipe=recipe))

        flourIngredientStock = createSupplierInvoiceDetail(id=1,ingredient="harina",symbol="kg",quantity=25,expirationDate=datetime.datetime(2023,8,1),price=2.3)
        
        po = createProductionOrder()
        podFixture = []
        podFixture.append(createProductionOrderDetail(id=1, quantity=4,productionOrder=po,recipe=recipe)) 

        ingredientConsumeFixture = []
        ingredientConsumeFixture.append(createProductionOrderConsume(po,flourIngredientStock,16,id=1))

        productConsumeFixture = []


        productionOrderDetailMock.filter.return_value = podFixture
        recipeDetailMock.filter.return_value = recipeIngredientsFixture
        productionOrderConsumeMock.filter.return_value = ingredientConsumeFixture
        productionOrderConsumeProductMock.filter.return_value = productConsumeFixture
        recipeDetailProductMock.filter.return_value = []

        service = ProdcutionOrderService(1,None, productionOrderDetailMock, recipeDetailMock, None, productionOrderConsumeMock, recipeDetailProductMock, None, productionOrderConsumeProductMock, None)
        actual = service.getConsumesByProductionOrderDetail(podFixture[0])

        expected = ConsumeByProductionOrderDetail(
            productionOrderDetail_id=1,
            expirationDate=datetime.datetime(2023,8,1),
            costPrice=36.8,
            sellPrice=0.0,
            batch=ProdcutionOrderService.getBatchNumber(),
            consumesByRecipeDetail=[
                ConsumeByRecipeDetail(
                    recipeDetail_id=1,
                    totalQuantity=16,
                    unitCostPrice=2.3,
                    expirationDate=datetime.datetime(2023,8,1)
                )
            ]
        )

        self.assertEqual(actual, expected)

    @patch('bakeryAdmin.models.RecipeDetailProduct.objects')
    @patch('bakeryAdmin.models.ProductionOrderConsumeProduct.objects')
    @patch('bakeryAdmin.models.ProductionOrderConsume.objects')
    @patch('bakeryAdmin.models.RecipeDetail.objects')
    @patch('bakeryAdmin.models.ProductionOrderDetail.objects')
    def test_twoIngredientConsumeItem(self,productionOrderDetailMock, recipeDetailMock,productionOrderConsumeMock, productionOrderConsumeProductMock, recipeDetailProductMock):
        podFixture = list([createProductionOrderDetail(id=i, quantity=4) for i in range(1,2)])
        recipe = createRecipe()
        recipeIngredientsFixture = list([createRecipeDetail(id=i,quantity=4,symbol="kg",ingredient="harina",recipe=recipe) for i in range(1,2)])
        ingredientConsumeFixture = list(
            [createProductionOrderConsume(createProductionOrder(),createSupplierInvoiceDetail(expirationDate=datetime.datetime(2023,8,1)),8,id=i) for i in range(1,3)]
        )
        productConsumeFixture = []

        productionOrderDetailMock.filter.return_value = podFixture
        recipeDetailMock.filter.return_value = recipeIngredientsFixture
        productionOrderConsumeMock.filter.return_value = ingredientConsumeFixture
        productionOrderConsumeProductMock.filter.return_value = productConsumeFixture
        recipeDetailProductMock.filter.return_value = []

        service = ProdcutionOrderService(1,None, productionOrderDetailMock, recipeDetailMock, None, productionOrderConsumeMock, recipeDetailProductMock, None, productionOrderConsumeProductMock, None)
        actual = service.getConsumesByProductionOrderDetail(podFixture[0])

        expected = ConsumeByProductionOrderDetail(
            productionOrderDetail_id=1,
            expirationDate=datetime.datetime(2023,8,1),
            costPrice=36.8,
            sellPrice=0.0,
            batch=ProdcutionOrderService.getBatchNumber(),
            consumesByRecipeDetail=[
                ConsumeByRecipeDetail(
                    recipeDetail_id=1,
                    totalQuantity=8,
                    unitCostPrice=2.3,
                    expirationDate=datetime.datetime(2023,8,1)
                ),
                ConsumeByRecipeDetail(
                    recipeDetail_id=1,
                    totalQuantity=8,
                    unitCostPrice=2.3,
                    expirationDate=datetime.datetime(2023,8,1)
                )
            ]
        )

        self.assertEqual(actual, expected)

    @patch('bakeryAdmin.models.RecipeDetailProduct.objects')
    @patch('bakeryAdmin.models.ProductionOrderConsumeProduct.objects')
    @patch('bakeryAdmin.models.ProductionOrderConsume.objects')
    @patch('bakeryAdmin.models.RecipeDetail.objects')
    @patch('bakeryAdmin.models.ProductionOrderDetail.objects')
    def test_twoRecipeDetailsTwoIngredientConsumeItem(self,productionOrderDetailMock, recipeDetailMock,productionOrderConsumeMock, productionOrderConsumeProductMock, recipeDetailProductMock):
                
        recipe = createRecipe()
        recipeIngredientsFixture = []
        recipeIngredientsFixture.append(createRecipeDetail(id=1,quantity=4,symbol="kg",ingredient="harina",recipe=recipe))
        recipeIngredientsFixture.append(createRecipeDetail(id=2,quantity=2,symbol="kg",ingredient="azúcar",recipe=recipe))

        flourIngredientStock = createSupplierInvoiceDetail(id=1,ingredient="harina",symbol="kg",quantity=25,expirationDate=datetime.datetime(2023,8,1), price=2.3)
        sugarIngredientStock = createSupplierInvoiceDetail(id=2,ingredient="azúcar",symbol="kg",quantity=20,expirationDate=datetime.datetime(2023,8,1), price=3.2)
        
        po = createProductionOrder()
        podFixture = []
        podFixture.append(createProductionOrderDetail(id=1, quantity=4,productionOrder=po,recipe=recipe)) 

        ingredientConsumeFixture = []
        ingredientConsumeFixture.append(createProductionOrderConsume(po,flourIngredientStock,8,id=1))
        ingredientConsumeFixture.append(createProductionOrderConsume(po,flourIngredientStock,8,id=2))
        ingredientConsumeFixture.append(createProductionOrderConsume(po,sugarIngredientStock,8,id=3))

        productConsumeFixture = []

        productionOrderDetailMock.filter.return_value = podFixture
        recipeDetailMock.filter.return_value = recipeIngredientsFixture
        productionOrderConsumeMock.filter.return_value = ingredientConsumeFixture
        productionOrderConsumeProductMock.filter.return_value = productConsumeFixture
        recipeDetailProductMock.filter.return_value = []        

        service = ProdcutionOrderService(1,None, productionOrderDetailMock, recipeDetailMock, None, productionOrderConsumeMock, recipeDetailProductMock, None, productionOrderConsumeProductMock, None)
        actual = service.getConsumesByProductionOrderDetail(podFixture[0])

        expected = ConsumeByProductionOrderDetail(
            productionOrderDetail_id=1,
            expirationDate=datetime.datetime(2023,8,1),
            costPrice=62.4,
            sellPrice=0.0,
            batch=ProdcutionOrderService.getBatchNumber(),
            consumesByRecipeDetail=[
                ConsumeByRecipeDetail(
                    recipeDetail_id=1,
                    totalQuantity=8,
                    unitCostPrice=2.3,
                    expirationDate=datetime.datetime(2023,8,1)
                ),
                ConsumeByRecipeDetail(
                    recipeDetail_id=1,
                    totalQuantity=8,
                    unitCostPrice=2.3,
                    expirationDate=datetime.datetime(2023,8,1)
                ),
                ConsumeByRecipeDetail(
                    recipeDetail_id=2,
                    totalQuantity=8,
                    unitCostPrice=3.2,
                    expirationDate=datetime.datetime(2023,8,1)
                )
            ]
        )

        self.assertEqual(actual, expected)
    
    @patch('bakeryAdmin.models.RecipeDetailProduct.objects')    
    @patch('bakeryAdmin.models.ProductionOrderConsumeProduct.objects')    
    @patch('bakeryAdmin.models.ProductionOrderConsume.objects')
    @patch('bakeryAdmin.models.RecipeDetail.objects')
    @patch('bakeryAdmin.models.ProductionOrderDetail.objects')
    def test_twoRecipeDetailsTwoIngredientConsumeItem_expirationDate(self,productionOrderDetailMock, recipeDetailMock,productionOrderConsumeMock, productionOrderConsumeProductMock, recipeDetailProductMock):
                
        recipe = createRecipe()
        recipeIngredientsFixture = []
        recipeIngredientsFixture.append(createRecipeDetail(id=1,quantity=4,symbol="kg",ingredient="harina",recipe=recipe))
        recipeIngredientsFixture.append(createRecipeDetail(id=2,quantity=2,symbol="kg",ingredient="azúcar",recipe=recipe))

        flour1IngredientStock = createSupplierInvoiceDetail(id=1,ingredient="harina",symbol="kg",quantity=8,expirationDate=datetime.datetime(2023,7,1), price=2.3)
        flour2IngredientStock = createSupplierInvoiceDetail(id=3,ingredient="harina",symbol="kg",quantity=8,expirationDate=datetime.datetime(2023,8,1), price=2.3)
        sugarIngredientStock = createSupplierInvoiceDetail(id=2,ingredient="azúcar",symbol="kg",quantity=20,expirationDate=datetime.datetime(2023,8,1), price=3.2)
        
        po = createProductionOrder()
        podFixture = []
        podFixture.append(createProductionOrderDetail(id=1, quantity=4,productionOrder=po,recipe=recipe)) 

        ingredientConsumeFixture = []
        ingredientConsumeFixture.append(createProductionOrderConsume(po,flour1IngredientStock,8,id=1))
        ingredientConsumeFixture.append(createProductionOrderConsume(po,flour2IngredientStock,8,id=2))
        ingredientConsumeFixture.append(createProductionOrderConsume(po,sugarIngredientStock,8,id=3))

        productConsumeFixture = []


        productionOrderDetailMock.filter.return_value = podFixture
        recipeDetailMock.filter.return_value = recipeIngredientsFixture
        productionOrderConsumeMock.filter.return_value = ingredientConsumeFixture
        productionOrderConsumeProductMock.filter.return_value = productConsumeFixture
        recipeDetailProductMock.filter.return_value = []        

        service = ProdcutionOrderService(1,None, productionOrderDetailMock, recipeDetailMock, None, productionOrderConsumeMock, recipeDetailProductMock, None, productionOrderConsumeProductMock, None)
        actual = service.getConsumesByProductionOrderDetail(podFixture[0])

        expected = ConsumeByProductionOrderDetail(
            productionOrderDetail_id=1,
            expirationDate=datetime.datetime(2023,7,1),
            costPrice=62.4,
            sellPrice=0.0,
            batch=ProdcutionOrderService.getBatchNumber(),
            consumesByRecipeDetail=[
                ConsumeByRecipeDetail(
                    recipeDetail_id=1,
                    totalQuantity=8,
                    unitCostPrice=2.3,
                    expirationDate=datetime.datetime(2023,7,1)
                ),
                ConsumeByRecipeDetail(
                    recipeDetail_id=1,
                    totalQuantity=8,
                    unitCostPrice=2.3,
                    expirationDate=datetime.datetime(2023,8,1)
                ),
                ConsumeByRecipeDetail(
                    recipeDetail_id=2,
                    totalQuantity=8,
                    unitCostPrice=3.2,
                    expirationDate=datetime.datetime(2023,8,1)
                )
            ]
        )

        self.assertEqual(actual, expected)

    @patch('bakeryAdmin.models.RecipeDetailProduct.objects')
    @patch('bakeryAdmin.models.ProductionOrderConsumeProduct.objects')
    @patch('bakeryAdmin.models.ProductionOrderConsume.objects')
    @patch('bakeryAdmin.models.RecipeDetail.objects')
    @patch('bakeryAdmin.models.ProductionOrderDetail.objects')
    def test_twoRecipeDetailsOneIngredientConsumeOnePRoductConsumeItem(self,productionOrderDetailMock, recipeDetailMock,productionOrderConsumeMock, productionOrderConsumeProductMock, recipeDetailProductMock):
                
        recipe = createRecipe()
        recipeIngredientsFixture = []
        recipeIngredientsFixture.append(createRecipeDetail(id=1,quantity=16,symbol="kg",ingredient="harina",recipe=recipe))

        recipeProductsFixture = []
        recipeProductsFixture.append(createRecipeDetailProduct(id=2,quantity=5,symbol="kg",product="masa base tarta",recipe=recipe))

        flourIngredientStock = createSupplierInvoiceDetail(id=1,ingredient="harina",symbol="kg",quantity=25,expirationDate=datetime.datetime(2023,8,1), price=2.3)
        cakeBaseProductStock = createProductStock(id=2,product='masa base tarta',symbol="kg",quantity=20,expirationDate=datetime.datetime(2023,7,1), costPrice=4.1)
        
        po = createProductionOrder()
        podFixture = []
        podFixture.append(createProductionOrderDetail(id=1, quantity=4,productionOrder=po,recipe=recipe)) 

        ingredientConsumeFixture = []
        ingredientConsumeFixture.append(createProductionOrderConsume(po,flourIngredientStock,8,id=1))
        ingredientConsumeFixture.append(createProductionOrderConsume(po,flourIngredientStock,8,id=2))

        productConsumeFixture = []
        productConsumeFixture.append(createProductionOrderConsumeProduct(po,cakeBaseProductStock,20))

        productionOrderDetailMock.filter.return_value = podFixture
        recipeDetailMock.filter.return_value = recipeIngredientsFixture
        productionOrderConsumeMock.filter.return_value = ingredientConsumeFixture
        productionOrderConsumeProductMock.filter.return_value = productConsumeFixture
        recipeDetailProductMock.filter.return_value = recipeProductsFixture        

        service = ProdcutionOrderService(1,None, productionOrderDetailMock, recipeDetailMock, None, productionOrderConsumeMock, recipeDetailProductMock, None, productionOrderConsumeProductMock, None)
        actual = service.getConsumesByProductionOrderDetail(podFixture[0])

        expected = ConsumeByProductionOrderDetail(
            productionOrderDetail_id=1,
            expirationDate=datetime.datetime(2023,7,1),
            costPrice=118.8,
            sellPrice=0.0,
            batch=ProdcutionOrderService.getBatchNumber(),
            consumesByRecipeDetail=[
                ConsumeByRecipeDetail(
                    recipeDetail_id=1,
                    totalQuantity=8,
                    unitCostPrice=2.3,
                    expirationDate=datetime.datetime(2023,8,1)
                ),
                ConsumeByRecipeDetail(
                    recipeDetail_id=1,
                    totalQuantity=8,
                    unitCostPrice=2.3,
                    expirationDate=datetime.datetime(2023,8,1)
                ),
                ConsumeByRecipeDetail(
                    recipeDetail_id=2,
                    totalQuantity=20,
                    unitCostPrice=4.1,
                    expirationDate=datetime.datetime(2023,7,1)
                )
            ]
        )

        self.assertEqual(actual, expected)

