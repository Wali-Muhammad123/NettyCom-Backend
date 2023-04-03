from django.db import models
from authemail.models import EmailAbstractUser, EmailUserManager

# Create your models here.
class Agent(EmailAbstractUser):
    phone=models.CharField(max_length=20)
    objects=EmailUserManager()
    def __str__(self):
        return self.email
class SalesData(models.Model):
    pass
class Teams(models.Model):
    pass
class TeamMembers(models.Model):
    pass
class Directories(models.Model):
    pass
class AddressCheckerUsage(models.Model):
    pass