from django.utils import timezone
from django.db import transaction
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import viewsets, status
from bakeryAdmin import models
from .serializer import AggregatedProductSerializer, MeasureUnitSerializer, IngredientSerializer, FixedCostSerializer, ProductStockSerializer, ProductionOrderConsumeProductSerializer, ProductionOrderConsumeSerializer, ProductionOrderStatusSerializer, RecipeSerializer, RecipeDetailSerializer, SupplierSerializer,SupplierInvoiceSerializer,SupplierInvoiceDetailSerializer, MakeSerializer, ProductionOrderSerializer,ProductionOrderDetailSerializer, AggregatedIngredientSerializer, ProductSerializer,RecipeDetailProductSerializer
from .services.productionOrders.ProdcutionOrderService import ProdcutionOrderService, ProdcutionOrderStatusEnum, ProductionOrderStatus

# Create your views here.
class MeasureUnitView(viewsets.ModelViewSet):
    serializer_class = MeasureUnitSerializer
    queryset = models.MeasureUnit.objects.all()

class IngredientView(viewsets.ModelViewSet):
    serializer_class = IngredientSerializer
    queryset = models.Ingredient.objects.all()

class FixedCostView(viewsets.ModelViewSet):
    serializer_class = FixedCostSerializer
    queryset = models.FixedCost.objects.all()

class RecipeView(viewsets.ModelViewSet):
    serializer_class = RecipeSerializer
    queryset = models.Recipe.objects.all()

    @action(detail=True, url_path='get-details')
    def get_recipe_details(self, request, pk=None):
        recipeDetails = models.RecipeDetail.objects.filter(recipe_id = pk)
        serializer = RecipeDetailSerializer(recipeDetails, many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

    @action(detail=True, url_path='get-details-products')
    def get_recipe_details_product(self, request, pk=None):
        recipeDetailsProduct = models.RecipeDetailProduct.objects.filter(recipe_id = pk)
        serializer = RecipeDetailProductSerializer(recipeDetailsProduct, many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

    @action(detail=True, url_path='calculate-total')
    def calculate_total(self, request, pk=None):
        details = list(models.RecipeDetail.objects.filter(recipe_id = pk))
        for detail in details:
            # Should get Ingredient stock the last one available from batch and exp date
            # This is not the right place for this functionality. Probable it's part of production module.
            ing = models.Ingredient.objects.get(id=detail.ingredient_id)
            print(repr(ing))
        
        return Response({"message":"done"},status=status.HTTP_200_OK)
    
    @action(detail=False, url_path='available-recipes')
    def get_available_recipes(self, request, pk=None):
        assignedRecipes = [product.recipe_id for product in models.Product.objects.all()]
        availableRecipes = models.Recipe.objects.all().exclude(id__in = assignedRecipes)

        serializer = RecipeSerializer(availableRecipes, many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)


class RecipeDetailView(viewsets.ModelViewSet):
    serializer_class = RecipeDetailSerializer
    queryset = models.RecipeDetail.objects.all()

class RecipeDetailProductView(viewsets.ModelViewSet):
    serializer_class = RecipeDetailProductSerializer
    queryset = models.RecipeDetailProduct.objects.all()
    

class SupplierView(viewsets.ModelViewSet):
    serializer_class = SupplierSerializer
    queryset = models.Supplier.objects.all()

class MakeView(viewsets.ModelViewSet):
    serializer_class = MakeSerializer
    queryset = models.Make.objects.all()

class SupplierInvoiceView(viewsets.ModelViewSet):
    serializer_class = SupplierInvoiceSerializer
    queryset = models.SupplierInvoice.objects.all()

    @action(detail=True, url_path='get-details')
    def get_supplierInvoice_details(self, request, pk=None):
        supplierInvoice = models.SupplierInvoiceDetail.objects.filter(supplierInvoice_id = pk)
        serializer = SupplierInvoiceDetailSerializer(supplierInvoice, many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    @action(detail=True, url_path='calculate-total')
    def calculate_total(self, request, pk=None):
        details = list(models.SupplierInvoiceDetail.objects.filter(supplierInvoice_id = pk))
        total = 0.0
        for detail in details:
            total = total + detail.price
            #print(repr(ing))
        
        return Response({"message":"done"},status=status.HTTP_200_OK)


class SupplierInvoiceDetailView(viewsets.ModelViewSet):
    serializer_class = SupplierInvoiceDetailSerializer
    queryset = models.SupplierInvoiceDetail.objects.all()

class ProductionOrderView(viewsets.ModelViewSet):
    serializer_class = ProductionOrderSerializer
    queryset = models.ProductionOrder.objects.all()

    @action(detail=True, url_path='get-details')
    def get_productionOrder_details(self, request, pk=None):
        productionOrder = models.ProductionOrderDetail.objects.filter(productionOrder_id = pk)
        serializer = ProductionOrderDetailSerializer(productionOrder, many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

    @action(detail=True,url_path="consumes")
    def consumes(self, request, pk=None):
        consumes = models.ProductionOrderConsume.objects.filter(productionOrder_id = pk)
        serializer = ProductionOrderConsumeSerializer(consumes, many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

    @action(detail=True,url_path="product-consumes")
    def product_consumes(self, request, pk=None):
        consumes = models.ProductionOrderConsumeProduct.objects.filter(productionOrder_id = pk)
        serializer = ProductionOrderConsumeProductSerializer(consumes, many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

    @action(detail=True, url_path='get-ingredients')
    def get_ingredients(self, request, pk=None):
        productionOrderDetails = models.ProductionOrderDetail.objects.filter(productionOrder_id = pk)
        result = models.RecipeDetail.objects.none() 
        for detail in productionOrderDetails:
            recipeDetails = models.RecipeDetail.objects.filter(recipe_id = detail.recipe.id)
            result = result | recipeDetails

        result = result.order_by("ingredient","quantity")
        serializer = RecipeDetailSerializer(result, many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

    @action(detail=True, url_path='get-aggregated-ingredients')
    def get_aggregated_ingredients(self, request, pk=None):
        result = ProdcutionOrderService(
            pk,
            models.ProductionOrder.objects, 
            models.ProductionOrderDetail.objects, 
            models.RecipeDetail.objects,
            models.SupplierInvoiceDetail.objects, 
            models.ProductionOrderConsume.objects,
            models.RecipeDetailProduct.objects,
            models.ProductStock.objects,
            models.ProductionOrderConsumeProduct.objects,
            models.Product.objects
            ).calculateAggregatedIngredients()
        serializer = AggregatedIngredientSerializer(result, many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

    @action(detail=True, url_path='get-aggregated-products')
    def get_aggregated_products(self, request, pk=None):
        result = ProdcutionOrderService(
            pk,
            models.ProductionOrder.objects, 
            models.ProductionOrderDetail.objects, 
            models.RecipeDetail.objects,
            models.SupplierInvoiceDetail.objects, 
            models.ProductionOrderConsume.objects,
            models.RecipeDetailProduct.objects,
            models.ProductStock.objects,
            models.ProductionOrderConsumeProduct.objects,
            models.Product.objects
            ).calculateAggregatedProducts()
        serializer = AggregatedProductSerializer(result, many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

    @action(detail=True, url_path='start')
    def start(self, request, pk=None):
        responseStatus = status.HTTP_400_BAD_REQUEST
        service = ProdcutionOrderService(pk,
                                        models.ProductionOrder.objects, 
                                        models.ProductionOrderDetail.objects, 
                                        models.RecipeDetail.objects, 
                                        models.SupplierInvoiceDetail.objects, 
                                        models.ProductionOrderConsume.objects,
                                        models.RecipeDetailProduct.objects,
                                        models.ProductStock.objects,
                                        models.ProductionOrderConsumeProduct.objects,
                                        models.Product.objects
                                        )
        result, productionOrder = service.canStart()

        if(result.status.code == ProdcutionOrderStatusEnum.OK):
            # responseStatus = status.HTTP_202_ACCEPTED
            # productionOrder.startedDate = timezone.now()
            # productionOrder.canceledDate = None
            # productionOrder.save()
            
            result = service.start()

            responseStatus = status.HTTP_404_NOT_FOUND
            if result.status.code == ProdcutionOrderStatusEnum.OK:
                responseStatus = status.HTTP_202_ACCEPTED
                
                with transaction.atomic():
                    for siDetail in result.supplierInvoiceDetails:
                        siDetail.save()
                    for poConsumes in result.productionOrderConsumes:
                        models.ProductionOrderConsume.objects.create(
                        productionOrder = models.ProductionOrder.objects.get(id = poConsumes.productionOrder_id),
                        supplierInvoiceDetail = models.SupplierInvoiceDetail.objects.get(id = poConsumes.supplierInvoiceDetail_id),
                        quantity = poConsumes.quantity
                        )
                    for prodStock in result.productStock:
                        prodStock.save()
                    for poProductConsumes in result.productionOrderConsumesProduct:
                        models.ProductionOrderConsumeProduct.objects.create(
                            productionOrder = models.ProductionOrder.objects.get(id = poProductConsumes.productionOrder_id),
                            productStock = models.ProductStock.objects.get(id = poProductConsumes.productStock_id),
                            quantity = poProductConsumes.quantity
                        )

                    productionOrder.startedDate = timezone.now()
                    productionOrder.canceledDate = None
                    productionOrder.save()

        serializer = ProductionOrderStatusSerializer(result, many=False)
        return Response(serializer.data,status=responseStatus)
    
    @action(detail=True,url_path="cancel")
    def cancel(self, request, pk=None):
        responseStatus = status.HTTP_400_BAD_REQUEST
        service = ProdcutionOrderService(pk,
                                        models.ProductionOrder.objects, 
                                        models.ProductionOrderDetail.objects, 
                                        models.RecipeDetail.objects, 
                                        models.SupplierInvoiceDetail.objects, 
                                        models.ProductionOrderConsume.objects,
                                        models.RecipeDetailProduct.objects,
                                        models.ProductStock.objects,
                                        models.ProductionOrderConsumeProduct.objects,
                                        models.Product.objects
                                        )
        result, productionOrder = service.canCancel()
        if result.status.code == ProdcutionOrderStatusEnum.OK:
            responseStatus = status.HTTP_202_ACCEPTED
            result = service.cancel()
            with transaction.atomic():
                for siDetail in result.supplierInvoiceDetails:
                    siDetail.save()
                for poConsumes in result.productionOrderConsumes:
                    poConsumes.delete()
                for prodStock in result.productStock:
                    prodStock.save()
                for poProdConsumes in result.productionOrderConsumesProduct:
                    poProdConsumes.delete()

                productionOrder.canceledDate = timezone.now()
                productionOrder.save()

        serializer = ProductionOrderStatusSerializer(result, many=False)
        return Response(serializer.data,status=responseStatus)

    @action(detail=True,url_path="close")
    def close(self, request, pk=None):
        responseStatus = status.HTTP_400_BAD_REQUEST
        service = ProdcutionOrderService(pk,
                                        models.ProductionOrder.objects, 
                                        models.ProductionOrderDetail.objects, 
                                        models.RecipeDetail.objects, 
                                        models.SupplierInvoiceDetail.objects, 
                                        models.ProductionOrderConsume.objects,
                                        models.RecipeDetailProduct.objects,
                                        models.ProductStock.objects,
                                        models.ProductionOrderConsumeProduct.objects,
                                        models.Product.objects
                                       )
        result, productionOrder = service.canClose()
        if result.status.code == ProdcutionOrderStatusEnum.OK:
            responseStatus = status.HTTP_202_ACCEPTED
            result = service.close()
            with transaction.atomic():
                for productStockToAdd in result.productStock:
                    models.ProductStock.objects.create(
                        product = models.Product.objects.get(id = productStockToAdd.productId),
                        measureUnit = models.MeasureUnit.objects.get(id = productStockToAdd.measureUnitId),
                        quantity=productStockToAdd.quantity,
                        quantityConsumed=productStockToAdd.quantityConsumed,
                        isForSell=productStockToAdd.isForSell,
                        batch=productStockToAdd.batch,
                        expirationDate = productStockToAdd.expirationDate,
                        unitCostPrice=productStockToAdd.unitCostPrice,
                        unitSellPrice=productStockToAdd.unitSellPrice
                    )

                productionOrder.closedDate = timezone.now()
                productionOrder.save()
        result.productStock.clear()
        serializer = ProductionOrderStatusSerializer(result, many=False)
        return Response(serializer.data,status=responseStatus)

class ProductionOrderDetailView(viewsets.ModelViewSet):
    serializer_class = ProductionOrderDetailSerializer
    queryset = models.ProductionOrderDetail.objects.all()

class ProductView(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    queryset = models.Product.objects.all()

class ProductStockView(viewsets.ModelViewSet):
    serializer_class = ProductStockSerializer
    queryset = models.ProductStock.objects.all()
