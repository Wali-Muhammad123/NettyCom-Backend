from django.db import models
from authemail.models import EmailAbstractUser, EmailUserManager
from django.conf import settings
from django.core.validators import RegexValidator
import datetime 
import uuid
from .constants import US_STATES
from .fields import BankDetailsField
# Create your models here.

class Agent(EmailAbstractUser):
    '''
    Custom User model for agents.
    '''
    uuid=models.UUIDField(unique=True,default=uuid.uuid4,editable=False,primary_key=True)
    objects=EmailUserManager()
    def __str__(self):
        return str(self.email)

class AgentProfile(models.Model):
    user=models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    phone=models.CharField(max_length=20,validators=[
        RegexValidator(
        regex=r'^\+92\d{2,5}\d{7,8}$',
        message='Phone number must be entered in the format: +92XXXXXXXXXX. Up to 15 digits allowed.',
        )])
    level=models.IntegerField(default=1)
    bank_details=BankDetailsField(max_length=100)
    isTeamLeader=models.BooleanField(default=False)
    referral=models.UUIDField(auto_created=True,unique=True,default=uuid.uuid1,editable=False)
    objects=models.Manager()
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
    sale_amount=models.IntegerField(default=0)
    appointmentdate=models.DateField(default=datetime.date.today)
    appointmenttime=models.TimeField(default=datetime.time(0,0))
    status=models.CharField(max_length=20,choices=STATUS,default='Pending')
    objects=models.Manager()
    
class Teams(models.Model):
    id=models.UUIDField(auto_created=True,unique=True,default=uuid.uuid1,editable=False,primary_key=True)
    teamname=models.CharField(max_length=20, default=None,unique=True)
    teamleader=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, default=None)
    objects=models.Manager()
class TeamMembers(models.Model):
    team=models.ForeignKey(Teams,on_delete=models.PROTECT, default=None)
    member=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, default=None)
    objects=models.Manager()
    class Meta:
        unique_together=('team','member')

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

class Finance(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, default=None)
    associated_sale=models.ForeignKey(SalesData,on_delete=models.PROTECT,default=None,blank=True,null=True)
    amount_recieved=models.FloatField(default=None)
    date=models.DateField(default=datetime.date.today)
    objects=models.Manager()
    def save(self,*args,**kwargs):
        netEarning=0
        if self.associated_sale:
            netEarning=self.associated_sale.sale_amount*0.05
            self.amount_recieved=netEarning
        else:
            self.amount_recieved=0
        super(Finance,self).save(*args,**kwargs)
class CommisionEarned(models.Model):
    teamleader=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, default=None)
    commissionEarned=models.FloatField(default=0.0)
    details_data=models.JSONField(default=dict)
    objects=models.Manager()
    class Meta:
        unique='teamleader'
    def save(self,*args,**kwargs):
        self.commisionEarned=0
        self.details_data={}
        super(CommisionEarned,self).save(*args,**kwargs)
