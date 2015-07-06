from django.db import models

# Create your models here.
class Person(models.Model):
    email = models.CharField(null=False,blank=False, max_length=200, unique=True)
    password = models.CharField(null=False,default=" ", max_length=250)
    ROLES = (
        ('ad', 'Admin'),
        ('Cu', 'Customer'),
        ('Co', 'Company'),
    )

    role = models.CharField(null=False, default=" ", max_length=200, choices=ROLES)
