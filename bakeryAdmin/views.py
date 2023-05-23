from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import viewsets, status
from .serializer import MeasureUnitSerializer, IngredientSerializer, FixedCostSerializer, RecipeSerializer, RecipeDetailSerializer, SupplierSerializer
from .models import MeasureUnit, Ingredient, FixedCost, Recipe, RecipeDetail, Supplier

# Create your views here.
class MeasureUnitView(viewsets.ModelViewSet):
    serializer_class = MeasureUnitSerializer
    queryset = MeasureUnit.objects.all()

class IngredientView(viewsets.ModelViewSet):
    serializer_class = IngredientSerializer
    queryset = Ingredient.objects.all()

class FixedCostView(viewsets.ModelViewSet):
    serializer_class = FixedCostSerializer
    queryset = FixedCost.objects.all()

class RecipeView(viewsets.ModelViewSet):
    serializer_class = RecipeSerializer
    queryset = Recipe.objects.all()

    @action(detail=True, url_path='get-details')
    def get_recipe_details(self, request, pk=None):
        recipe = RecipeDetail.objects.filter(recipe_id = pk)
        serializer = RecipeDetailSerializer(recipe, many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    @action(detail=True, url_path='calculate-total')
    def calculate_total(self, request, pk=None):
        details = list(RecipeDetail.objects.filter(recipe_id = pk))
        for detail in details:
            # Should get Ingredient stock the last one available from batch and exp date
            # This is not the right place for this functionality. Probable it's part of production module.
            ing = Ingredient.objects.get(id=detail.ingredient_id)
            print(repr(ing))
        
        return Response({"message":"done"},status=status.HTTP_200_OK)


class RecipeDetailView(viewsets.ModelViewSet):
    serializer_class = RecipeDetailSerializer
    queryset = RecipeDetail.objects.all()

class SupplierView(viewsets.ModelViewSet):
    serializer_class = SupplierSerializer
    queryset = Supplier.objects.all()

