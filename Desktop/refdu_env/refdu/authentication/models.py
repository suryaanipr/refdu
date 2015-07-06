from django.db import models

# Create your models here.
class Person(models.Model):
    email = models.CharField(null=False,blank=False, max_length=30)
    password = models.CharField(null=False,default=" ", max_length=30)
    ROLES = (
        ('ad', 'Admin'),
        ('Cu', 'Customer'),
        ('Co', 'Company'),
    )

    role = models.CharField(null=False, default=" ", max_length=10, choices=ROLES)
