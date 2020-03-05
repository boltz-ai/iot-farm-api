from rest_framework import serializers

from . import models


# Serializers
class SensorGenericSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Sensor
        fields = '__all__'
