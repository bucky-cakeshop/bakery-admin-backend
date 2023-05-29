from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import viewsets, status
from bakeryAdmin import models
from .serializer import MeasureUnitSerializer, IngredientSerializer, FixedCostSerializer, RecipeSerializer, RecipeDetailSerializer, SupplierSerializer,SupplierInvoiceSerializer,SupplierInvoiceDetailSerializer, MakeSerializer, ProductionOrderSerializer,ProductionOrderDetailSerializer, AggregatedIngredientSerializer
from .services.productionOrders.ProdcutionOrderService import ProdcutionOrderService
import json

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
        recipe = models.RecipeDetail.objects.filter(recipe_id = pk)
        serializer = RecipeDetailSerializer(recipe, many=True)
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


class RecipeDetailView(viewsets.ModelViewSet):
    serializer_class = RecipeDetailSerializer
    queryset = models.RecipeDetail.objects.all()

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
        result = ProdcutionOrderService(pk).calculateAggregatedIngredients()
        serializer = AggregatedIngredientSerializer(result, many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

    @action(detail=True, url_path='get-ingredients-stock')
    def get_ingredients_stock(self, request, pk=None):
        result = ProdcutionOrderService(pk).getIngredientsFromStock()
        # serializer = AggregatedIngredientSerializer(result, many=True)
        # return Response(serializer.data,status=status.HTTP_200_OK)
        return Response({'message':'ok'},status=status.HTTP_200_OK)
        

class ProductionOrderDetailView(viewsets.ModelViewSet):
    serializer_class = ProductionOrderDetailSerializer
    queryset = models.ProductionOrderDetail.objects.all()
