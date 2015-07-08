from django.db import models
import binascii
import os
from datetime import datetime, timedelta
import jwt
from refdu.settings import SECRET_KEY

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
    isActive = models.BooleanField(default=False)
    activate_token = models.CharField(null=False, default=" ", max_length=250)



class Token(models.Model):

    user = models.ForeignKey(Person)
    token = models.CharField(max_length=200, primary_key=True)
    created = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.token:
            self.token = self.create_token(self.user.id)
            print self.token
        return super(Token, self).save(*args, **kwargs)

    def create_token(self, userid):
        payload = {
            'sub': str(userid),
            'iat': datetime.now(),
            'exp': datetime.now() + timedelta(days=20)
        }
        token = jwt.encode(payload, SECRET_KEY)
        return token.decode('unicode_escape')

    def __unicode__(self):
        return self.token