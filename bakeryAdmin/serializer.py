from rest_framework import serializers
from .models import MeasureUnit, Ingredient, FixedCost, Recipe, RecipeDetail, Supplier,BuyOrder,BuyOrderDetail,Make

class MeasureUnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = MeasureUnit
        fields = '__all__'

class IngredientSerializer(serializers.ModelSerializer):  
    class Meta:
        model = Ingredient
        fields = '__all__'
    
class FixedCostSerializer(serializers.ModelSerializer):
    class Meta:
        model = FixedCost
        fields = '__all__'

class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ['id','title', 'description']#'recipeDetail'

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

class MakeSerializer(serializers.ModelSerializer):  
    class Meta:
        model = Make
        fields = '__all__'

class MeasureUnitForDetailSerializaer(serializers.ModelSerializer):
    class Meta:
        model = MeasureUnit
        fields = ['id','title','symbol']

class IngredientForDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ['id','name']

class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = ['id','name','email','web','phone','description']

class BuyOrderSerializer(serializers.ModelSerializer):
    supplier = serializers.PrimaryKeyRelatedField(queryset=Supplier.objects.all()) 
    supplier_object = serializers.SerializerMethodField()

    def get_supplier_object(self, obj):
        return {'id': obj.supplier.id, 'name': obj.supplier.name}

    class Meta:
        model = BuyOrder
        fields = '__all__'#['id','supplier','description']

class BuyOrderDetailSerializer(serializers.ModelSerializer):
    buyOrder = serializers.PrimaryKeyRelatedField(queryset=BuyOrder.objects.all()) 

    measureUnit = serializers.PrimaryKeyRelatedField(queryset=MeasureUnit.objects.all()) 
    measureUnit_object = serializers.SerializerMethodField()

    ingredient = serializers.PrimaryKeyRelatedField(queryset=Ingredient.objects.all()) 
    ingredient_object = serializers.SerializerMethodField()

    make = serializers.PrimaryKeyRelatedField(queryset=Make.objects.all()) 
    make_object = serializers.SerializerMethodField()

    def get_measureUnit_object(self, obj):
        return {'id': obj.measureUnit.id, 'title': obj.measureUnit.title, 'symbol': obj.measureUnit.symbol}

    def get_ingredient_object(self, obj):
        return {'id': obj.ingredient.id, 'name': obj.ingredient.name}
    
    def get_make_object(self, obj):
        return {'id': obj.make.id, 'name': obj.make.name}

    class Meta:
        model = BuyOrderDetail
        fields = '__all__'
