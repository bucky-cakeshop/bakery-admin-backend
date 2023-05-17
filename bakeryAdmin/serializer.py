from rest_framework import serializers
from .models import MeasureUnit, Ingredient

class MeasureUnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = MeasureUnit
        fields = '__all__'

class IngredientSerializer(serializers.ModelSerializer):
    measureUnit = serializers.PrimaryKeyRelatedField(queryset=MeasureUnit.objects.all()) 
    class Meta:
        model = Ingredient
        fields = '__all__'
    
