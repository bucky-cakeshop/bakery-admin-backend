from rest_framework import serializers
from .models import MeasureUnit

class MeasureUnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = MeasureUnit
        # fields = ('id', 'title','symbol', 'description', 'done')
        fields = '__all__'
    
