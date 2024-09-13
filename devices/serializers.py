from rest_framework import serializers
from .models import DataEntry

class DataEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = DataEntry
        fields = [
            'device_id', 'timestamp', 'acceleration_x', 'acceleration_y', 'acceleration_z',
            'gyro_x', 'gyro_y', 'gyro_z', 'temperature', 'battery'
        ]
