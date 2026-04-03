from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('viewer', 'Viewer'),
        ('analyst', 'Analyst'),
        ('admin', 'Admin'),
    ]
    role = models.CharField(max_length=20,choices=ROLE_CHOICES,default='viewer')
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if self.is_superuser:
            self.role = 'admin'
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.username} ({self.role})"