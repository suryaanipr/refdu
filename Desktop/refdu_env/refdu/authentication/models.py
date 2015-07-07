from django.db import models
import binascii
import os


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



class Token(models.Model):

    user = models.ForeignKey(Person)
    token = models.CharField(max_length=40, primary_key=True)
    created = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.token:
            self.token = self.generate_token()
        return super(Token, self).save(*args, **kwargs)

    def generate_token(self):
        return binascii.hexlify(os.urandom(20)).decode()

    def __unicode__(self):
        return self.token