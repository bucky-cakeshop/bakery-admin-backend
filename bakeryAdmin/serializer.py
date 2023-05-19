from rest_framework import serializers
from .models import MeasureUnit, Ingredient, FixedCost, Recipe, RecipeDetail

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

class RecipeSerializer(serializers.ModelSerializer):
    measureUnit = serializers.PrimaryKeyRelatedField(queryset=MeasureUnit.objects.all()) 
    measureUnit_object = serializers.SerializerMethodField()
    ingredient = serializers.PrimaryKeyRelatedField(queryset=Ingredient.objects.all()) 
    ingredient_object = serializers.SerializerMethodField()

    def get_measureUnit_object(self, obj):
        return {'id': obj.measureUnit.id, 'name': obj.measureUnit.title, 'symbol': obj.measureUnit.symbol}

    def get_ingredient_object(self, obj):
        return {'id': obj.ingredient.id, 'name': obj.ingredient.name}

    class Meta:
        model = Recipe
        fields = '__all__'


class RecipeDetailSerializer(serializers.ModelSerializer):
    recipe = serializers.PrimaryKeyRelatedField(queryset=Recipe.objects.all()) 
    recipe_object = serializers.SerializerMethodField()

    measureUnit = serializers.PrimaryKeyRelatedField(queryset=MeasureUnit.objects.all()) 
    measureUnit_object = serializers.SerializerMethodField()

    ingredient = serializers.PrimaryKeyRelatedField(queryset=Ingredient.objects.all()) 
    ingredient_object = serializers.SerializerMethodField()

    def get_recipe_object(self, obj):
        return {'id': obj.recipe.id, 'name': obj.recipe.title, 'symbol': obj.measureUnit.symbol}

    def get_measureUnit_object(self, obj):
        return {'id': obj.measureUnit.id, 'name': obj.measureUnit.title, 'symbol': obj.measureUnit.symbol}

    def get_ingredient_object(self, obj):
        return {'id': obj.ingredient.id, 'name': obj.ingredient.name}

    class Meta:
        model = RecipeDetail
        fields = '__all__'
