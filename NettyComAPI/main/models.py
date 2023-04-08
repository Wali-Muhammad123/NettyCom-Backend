from django.db import models
from authemail.models import EmailAbstractUser, EmailUserManager
import datetime 
from .constants import US_STATES
import uuid
from django.conf import settings
from .fields import BankDetailsField
# Create your models here.

class Agent(EmailAbstractUser):
    '''
    Custom User model for agents.
    '''
    id=models.UUIDField(auto_created=True,unique=True,default=uuid.uuid1,editable=False,primary_key=True)
    objects=EmailUserManager()
    def __str__(self):
        return self.email

class AgentProfile(models.Model):
    user=models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    phone=models.CharField(max_length=20)
    level=models.IntegerField(default=1)
    bank_details=BankDetailsField(max_length=100)
    referral=models.UUIDField(auto_created=True,unique=True,default=uuid.uuid1,editable=False)
    def save(self,*args,**kwargs):
        super(AgentProfile,self).save(*args,**kwargs)

class SalesData(models.Model):
    STATUS=(
        ('Pending','Pending'),
        ('Approved','Approved'),
        ('Declined','Declined'),
        ('Cancelled','Cancelled'),
        ('Completed','Completed'),
    )
    agent=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, default=None)
    clientname=models.CharField(max_length=20, default=None)
    clientphone=models.CharField(max_length=20, default=None)
    clientemail=models.EmailField(default=None,blank=True,null=True)
    clientaddress=models.CharField(max_length=70, default=None)
    appointmentdate=models.DateField(default=datetime.date.today)
    appointmenttime=models.TimeField(default=datetime.time(0,0))
    status=models.CharField(max_length=20,choices=STATUS,default='Pending')
    
class Teams(models.Model):
    id=models.UUIDField(auto_created=True,unique=True,default=uuid.uuid1,editable=False,primary_key=True)
    teamname=models.CharField(max_length=20, default=None)
    teamleader=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, default=None)

class TeamMembers(models.Model):
    team=models.ForeignKey(Teams,on_delete=models.PROTECT, default=None)
    member=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, default=None)

class Directories(models.Model):
    STATES=US_STATES
    postalcode=models.CharField(max_length=10,default=None)
    state=models.CharField(max_length=2,choices=STATES, default=None)
    city=models.CharField(max_length=20, default=None)
    radius_mile=models.IntegerField(default=0)

class AddressCheckerUsage(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, default=None)
    date=models.DateField(default=datetime.date.today)
    address_requested=models.CharField(max_length=70, default=None)
    sale_associated=models.ForeignKey(SalesData,on_delete=models.PROTECT,default=None,blank=True,null=True)
    def save(self,*args,**kwargs):
        self.date=datetime.date.today()
        super(AddressCheckerUsage,self).save(*args,**kwargs)
    
