from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import status
from rest_framework.decorators import action
from django.core import serializers
from .serializer import MeasureUnitSerializer, IngredientSerializer, FixedCostSerializer, RecipeSerializer, RecipeDetailSerializer
from .models import MeasureUnit, Ingredient, FixedCost, Recipe, RecipeDetail

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

class RecipeDetailView(viewsets.ModelViewSet):
    serializer_class = RecipeDetailSerializer
    queryset = RecipeDetail.objects.all()

