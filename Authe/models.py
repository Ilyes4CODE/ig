# models.py
from django.db import models
from django.utils import timezone

class UserLogin(models.Model):
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(null=True, blank=True)
    timestamp = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"{self.username} - {self.timestamp}"

class UserSnapshot(models.Model):
    user_login = models.ForeignKey(UserLogin, on_delete=models.CASCADE, related_name='snapshots')
    image = models.ImageField(upload_to='snapshots/')
    timestamp = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"Snapshot for {self.user_login.username} - {self.timestamp}"