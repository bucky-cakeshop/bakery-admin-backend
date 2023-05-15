from requests import Response
from rest_framework import viewsets
from .serializer import MeasureUnitSerializer
from .models import MeasureUnit

# Create your views here.
class MeasureUnitView(viewsets.ModelViewSet):
    serializer_class = MeasureUnitSerializer
    queryset = MeasureUnit.objects.all()