from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from . import serializers, models


# Create your views here.
class SensorReadOnlyViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Sensor APIs. This viewset automatically provides `list` and `retrieve` actions.
    """
    queryset = models.Sensor.objects.all().order_by('device')
    serializer_class = serializers.SensorGenericSerializer
    permission_classes = [AllowAny]
    search_fields = ['device', ]
