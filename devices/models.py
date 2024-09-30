from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta
from django.utils import timezone

class Project(models.Model):
    user = models.ForeignKey(User, related_name='projects', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)  # Optional description

    def __str__(self):
        return f"Project {self.name} by {self.user.username}"

class Device(models.Model):
    project = models.ForeignKey(Project, related_name='devices', on_delete=models.CASCADE, default=1)
    user = models.ForeignKey(User, related_name='devices', on_delete=models.CASCADE, default = 1)
    device_id = models.CharField(max_length=100)
    name = models.CharField(max_length=100, null=True, blank=True)  # Optional name for device
    
    def __str__(self):
        return f"Device {self.device_id} owned by {self.user.username}"


class MillisecondDateTimeField(models.DateTimeField):
    def pre_save(self, model_instance, add):
        value = super().pre_save(model_instance, add)
        # Truncate microseconds
        return value - timedelta(microseconds=value.microsecond % 1000)
    

class DataEntry(models.Model):
    packetID = models.CharField(default=0.0) 
    device = models.ForeignKey(Device, related_name='data_entries', on_delete=models.CASCADE)
    timestamp = MillisecondDateTimeField(default=timezone.now)
    
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
    
    def save(self, *args, **kwargs):
        # Truncate microseconds to milliseconds
        if self.timestamp:
            self.timestamp = self.timestamp.replace(microsecond=0)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Data from {self.device.device_id} at {self.timestamp}"
