from rest_framework import serializers
from bakeryAdmin import models
from bakeryAdmin.services.productionOrders.ProdcutionOrderService import ProductionOrderStatus, ProdcutionOrderStatusEnum, ResultStatus

class MeasureUnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.MeasureUnit
        fields = '__all__'

class IngredientSerializer(serializers.ModelSerializer):  
    class Meta:
        model = models.Ingredient
        fields = '__all__'
    
class FixedCostSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.FixedCost
        fields = '__all__'

class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Recipe
        fields = ['id','title', 'description']

class RecipeDetailSerializer(serializers.ModelSerializer):
    recipe = serializers.PrimaryKeyRelatedField(queryset=models.Recipe.objects.all()) 
    recipe_object = serializers.SerializerMethodField()

    measureUnit = serializers.PrimaryKeyRelatedField(queryset=models.MeasureUnit.objects.all()) 
    measureUnit_object = serializers.SerializerMethodField()

    ingredient = serializers.PrimaryKeyRelatedField(queryset=models.Ingredient.objects.all()) 
    ingredient_object = serializers.SerializerMethodField()

    def get_recipe_object(self, obj):
        return {'id': obj.recipe.id, 'name': obj.recipe.title, 'symbol': obj.measureUnit.symbol}

    def get_measureUnit_object(self, obj):
        return {'id': obj.measureUnit.id, 'name': obj.measureUnit.title, 'symbol': obj.measureUnit.symbol}

    def get_ingredient_object(self, obj):
        return {'id': obj.ingredient.id, 'name': obj.ingredient.name}

    class Meta:
        model = models.RecipeDetail
        fields = '__all__'

class RecipeDetailProductSerializer(serializers.ModelSerializer):
    recipe = serializers.PrimaryKeyRelatedField(queryset=models.Recipe.objects.all()) 
    recipe_object = serializers.SerializerMethodField()

    measureUnit = serializers.PrimaryKeyRelatedField(queryset=models.MeasureUnit.objects.all()) 
    measureUnit_object = serializers.SerializerMethodField()

    product = serializers.PrimaryKeyRelatedField(queryset=models.Product.objects.all()) 
    product_object = serializers.SerializerMethodField()

    def get_recipe_object(self, obj):
        return {'id': obj.recipe.id, 'name': obj.recipe.title, 'symbol': obj.measureUnit.symbol}

    def get_measureUnit_object(self, obj):
        return {'id': obj.measureUnit.id, 'name': obj.measureUnit.title, 'symbol': obj.measureUnit.symbol}

    def get_product_object(self, obj):
        return {'id': obj.product.id, 'name': obj.product.name}

    
    class Meta:
        model = models.RecipeDetailProduct
        fields = '__all__'

class MakeSerializer(serializers.ModelSerializer):  
    class Meta:
        model = models.Make
        fields = '__all__'

class MeasureUnitForDetailSerializaer(serializers.ModelSerializer):
    class Meta:
        model = models.MeasureUnit
        fields = ['id','title','symbol']

class IngredientForDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Ingredient
        fields = ['id','name']

class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Supplier
        fields = ['id','name','email','web','phone','description']

class SupplierInvoiceSerializer(serializers.ModelSerializer):
    supplier = serializers.PrimaryKeyRelatedField(queryset=models.Supplier.objects.all()) 
    supplier_object = serializers.SerializerMethodField()

    def get_supplier_object(self, obj):
        return {'id': obj.supplier.id, 'name': obj.supplier.name}

    class Meta:
        model = models.SupplierInvoice
        fields = '__all__'

class SupplierInvoiceDetailSerializer(serializers.ModelSerializer):
    supplierInvoice = serializers.PrimaryKeyRelatedField(queryset=models.SupplierInvoice.objects.all()) 

    measureUnit = serializers.PrimaryKeyRelatedField(queryset=models.MeasureUnit.objects.all()) 
    measureUnit_object = serializers.SerializerMethodField()

    ingredient = serializers.PrimaryKeyRelatedField(queryset=models.Ingredient.objects.all()) 
    ingredient_object = serializers.SerializerMethodField()

    make = serializers.PrimaryKeyRelatedField(queryset=models.Make.objects.all()) 
    make_object = serializers.SerializerMethodField()

    def get_measureUnit_object(self, obj):
        return {'id': obj.measureUnit.id, 'title': obj.measureUnit.title, 'symbol': obj.measureUnit.symbol}

    def get_ingredient_object(self, obj):
        return {'id': obj.ingredient.id, 'name': obj.ingredient.name}
    
    def get_make_object(self, obj):
        return {'id': obj.make.id, 'name': obj.make.name}

    class Meta:
        model = models.SupplierInvoiceDetail
        fields = '__all__'

class ProductionOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProductionOrder
        fields = '__all__'

class ProductionOrderDetailSerializer(serializers.ModelSerializer):
    productionOrder = serializers.PrimaryKeyRelatedField(queryset=models.ProductionOrder.objects.all()) 

    recipe = serializers.PrimaryKeyRelatedField(queryset=models.Recipe.objects.all()) 
    recipe_object = serializers.SerializerMethodField()

    def get_recipe_object(self, obj):
        return {'id': obj.recipe.id, 'title': obj.recipe.title}

    class Meta:
        model = models.ProductionOrderDetail
        fields = '__all__'

class ProductionOrderConsumeSerializer(serializers.ModelSerializer):
    productionOrder = serializers.PrimaryKeyRelatedField(queryset=models.ProductionOrder.objects.all()) 
    supplierInvoiceDetail = SupplierInvoiceDetailSerializer()
    
    quantity = serializers.FloatField()

    class Meta:
        model = models.ProductionOrderConsume
        fields = '__all__'

class AggregatedIngredientSerializer(serializers.Serializer):
    ingredientId = serializers.IntegerField()
    ingredientName = serializers.CharField()
    measureUnitId = serializers.IntegerField()
    measureUnitSymbol = serializers.CharField()
    total = serializers.DecimalField(max_digits=5,decimal_places=2)

    class Meta:
        fields = '__all__'

class AggregatedProductSerializer(serializers.Serializer):
    productId = serializers.IntegerField()
    productName = serializers.CharField()
    measureUnitId = serializers.IntegerField()
    measureUnitSymbol = serializers.CharField()
    total = serializers.DecimalField(max_digits=5,decimal_places=2)

    class Meta:
        fields = '__all__'

class ProductionOrderConsumeIngredientSerializer(serializers.Serializer):
    productionOrder_id = serializers.IntegerField()
    supplierInvoiceDetail_id = serializers.IntegerField()
    quantity = serializers.FloatField()

class ProductionOrderConsumeProductSerializer(serializers.Serializer):
    productionOrder_id = serializers.IntegerField()
    productStock_id = serializers.IntegerField()
    quantity = serializers.FloatField()


class supplierInvoiceDetailForPoSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    ingredient = serializers.SerializerMethodField()
    measureUnit = serializers.SerializerMethodField()
    quantity = serializers.FloatField()
    quantityConsumed = serializers.FloatField()

    def get_measureUnit(self, obj):
        return {'id': obj.measureUnit.id, 'title': obj.measureUnit.title, 'symbol': obj.measureUnit.symbol}

    def get_ingredient(self, obj):
        return {'id': obj.ingredient.id, 'name': obj.ingredient.name}

class ProductStockForPoSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    product = serializers.SerializerMethodField()
    measureUnit = serializers.SerializerMethodField()
    quantity = serializers.FloatField()
    quantityConsumed = serializers.FloatField()

    def get_measureUnit(self, obj):
        return {'id': obj.measureUnit.id, 'title': obj.measureUnit.title, 'symbol': obj.measureUnit.symbol}

    def get_product(self, obj):
        return {'id': obj.product.id, 'name': obj.product.name}

class ProductionOrderMissedIngredientSerializer(serializers.Serializer):
    aggregatedTotalIngredient = AggregatedIngredientSerializer()
    totalQuantityInStock = serializers.FloatField()
    totalToConsume = serializers.FloatField()

class ProductionOrderMissedProductSerializer(serializers.Serializer):
    aggregatedTotalProduct = AggregatedProductSerializer()
    totalQuantityInStock = serializers.FloatField()
    totalToConsume = serializers.FloatField()

class ResultStatusSerializer(serializers.Serializer):
    code = serializers.IntegerField()
    message = serializers.StringRelatedField()
    
    class Meta:
        model = ResultStatus
        fields = '__all__'


class ProductionOrderStatusSerializer(serializers.Serializer):
    status = ResultStatusSerializer()
    supplierInvoiceDetails = serializers.ListSerializer(child=supplierInvoiceDetailForPoSerializer())
    productionOrderConsumes = serializers.ListSerializer(child=ProductionOrderConsumeIngredientSerializer())
    missingIngredients = serializers.ListSerializer(child=ProductionOrderMissedIngredientSerializer())
    isOk = serializers.BooleanField()
    productStock = serializers.ListSerializer(child=ProductStockForPoSerializer())
    productionOrderConsumesProduct = serializers.ListSerializer(child=ProductionOrderConsumeProductSerializer())
    missingProducts = serializers.ListSerializer(child=ProductionOrderMissedProductSerializer())
    
    class Meta:
        model = ProductionOrderStatus
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    recipe_object = serializers.SerializerMethodField()

    def get_recipe_object(self, obj):
        return {'id': obj.recipe.id, 'title': obj.recipe.title}

    class Meta:
        model = models.Product
        fields = '__all__'

class ProductStockSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=models.Product.objects.all()) 
    product_object = serializers.SerializerMethodField()

    measureUnit_object = serializers.SerializerMethodField()

    def get_measureUnit_object(self, obj):
        return {'id': obj.measureUnit.id, 'title': obj.measureUnit.title, 'symbol': obj.measureUnit.symbol}

    def get_product_object(self, obj):
        return {'id': obj.product.id, 'name': obj.product.name}

    class Meta:
        model = models.ProductStock
        fields = '__all__'

class ProductionOrderConsumeProductSerializer(serializers.ModelSerializer):
    productionOrder = serializers.PrimaryKeyRelatedField(queryset=models.ProductionOrder.objects.all()) 
    productStock = ProductStockSerializer()
    
    quantity = serializers.FloatField()

    class Meta:
        model = models.ProductionOrderConsumeProduct
        fields = '__all__'
