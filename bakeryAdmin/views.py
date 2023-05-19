from requests import Response
from rest_framework import viewsets
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

class RecipeDetailView(viewsets.ModelViewSet):
    serializer_class = RecipeDetailSerializer
    queryset = RecipeDetail.objects.all()
