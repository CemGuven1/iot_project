from django.db import models
from django.contrib.auth.models import User

class Device(models.Model):
    user = models.ForeignKey(User, related_name='devices', on_delete=models.CASCADE, default = 1)
    device_id = models.CharField(max_length=100)
    name = models.CharField(max_length=100, null=True, blank=True)  # Optional name for device

    def __str__(self):
        return f"Device {self.device_id} owned by {self.user.username}"


class DataEntry(models.Model):
    device = models.ForeignKey(Device, related_name='data_entries', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    # Acceleration Data (x, y, z)
    acceleration_x = models.FloatField(default=0.0)
    acceleration_y = models.FloatField(default=0.0)
    acceleration_z = models.FloatField(default=0.0)

    # Gyro Position Data (x, y, z)
    gyro_x = models.FloatField(default=0.0)
    gyro_y = models.FloatField(default=0.0)
    gyro_z = models.FloatField(default=0.0)

    # Other data
    temperature = models.FloatField(default=0.0)
    battery = models.FloatField(default=100.0)

    def __str__(self):
        return f"Data from {self.device.device_id} at {self.timestamp}"
