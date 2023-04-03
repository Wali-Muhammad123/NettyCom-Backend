from django.db import models
from authemail.models import EmailAbstractUser, EmailUserManager

# Create your models here.
class Agent(EmailAbstractUser):
    phone=models.CharField(max_length=20)
    is_agent=models.BooleanField(default=True)
    is_admin=models.BooleanField(default=False)
    is_active=models.BooleanField(default=True)
    is_staff=models.BooleanField(default=False)
    is_superuser=models.BooleanField(default=False)
    USERNAME_FIELD='email'
    REQUIRED_FIELDS=['username','phone']
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