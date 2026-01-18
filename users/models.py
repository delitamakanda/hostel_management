from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = "ADMIN"
        STAFF = "STAFF"
        GUEST = "GUEST"
    
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.GUEST)
    
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custome_user_set',
        blank=True,
    )
    
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custome_user_set',
        blank=True,
    )
    
