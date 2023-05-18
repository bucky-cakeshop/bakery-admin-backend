from requests import Response
from rest_framework import viewsets
from .serializer import MeasureUnitSerializer, IngredientSerializer, FixedCostSerializer
from .models import MeasureUnit, Ingredient, FixedCost

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
