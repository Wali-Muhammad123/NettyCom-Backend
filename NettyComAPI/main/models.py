from django.db import models
from authemail.models import EmailAbstractUser, EmailUserManager
import settings
import datetime 
from .utils import US_STATES
# Create your models here.
class Agent(EmailAbstractUser):
    objects=EmailUserManager()
    def __str__(self):
        return self.email

class Profile(models.Model):
    user=models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    phone=models.CharField(max_length=20)
    level=models.IntegerField(default=1)
    referral=models.UUIDField(auto_created=True,unique=True)
    def save(self,*args,**kwargs):
        super(Profile,self).save(*args,**kwargs)

class SalesData(models.Model):
    STATUS=(
        ('Pending','Pending'),
        ('Approved','Approved'),
        ('Declined','Declined'),
        ('Cancelled','Cancelled'),
        ('Completed','Completed'),
    )
    agent=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    clientname=models.CharField(max_length=20)
    clientphone=models.CharField(max_length=20)
    clientemail=models.EmailField(default=None,blank=True,null=True)
    clientaddress=models.CharField(max_length=70)
    appointmentdate=models.DateField()
    appointmenttime=models.TimeField()
    status=models.CharField(max_length=20,choices=STATUS,default='Pending')
    
class Teams(models.Model):
    teamname=models.CharField(max_length=20)
    teamleader=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
class TeamMembers(models.Model):
    team=models.ForeignKey(Teams,on_delete=models.PROTECT)
    member=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
class Directories(models.Model):
    STATES=US_STATES
    postalcode=models.CharField(max_length=10)
    state=models.CharField(max_length=2,choices=STATES)
    city=models.CharField(max_length=20)
    radius_mile=models.IntegerField(default=0)

class AddressCheckerUsage(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    date=models.DateField()
    address_requested=models.CharField(max_length=70)
    sale_associated=models.ForeignKey(SalesData,on_delete=models.PROTECT,default=None,blank=True,null=True)
    def save(self,*args,**kwargs):
        self.date=datetime.date.today()
        super(AddressCheckerUsage,self).save(*args,**kwargs)
    
