from rest_framework import serializers
from .models import MeasureUnit, Ingredient, FixedCost

class MeasureUnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = MeasureUnit
        fields = '__all__'

class IngredientSerializer(serializers.ModelSerializer):
    measureUnit = serializers.PrimaryKeyRelatedField(queryset=MeasureUnit.objects.all()) 
    measureUnit_object = serializers.SerializerMethodField()

    def get_measureUnit_object(self, obj):
        return {'id': obj.measureUnit.id, 'name': obj.measureUnit.title, 'symbol': obj.measureUnit.symbol}
    
    class Meta:
        model = Ingredient
        fields = '__all__'
    
class FixedCostSerializer(serializers.ModelSerializer):
    class Meta:
        model = FixedCost
        fields = '__all__'
