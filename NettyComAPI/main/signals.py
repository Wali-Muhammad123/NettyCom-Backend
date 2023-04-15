from django.db.models.signals import pre_save,post_save
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist
from .models import AddressCheckerUsage, Teams, TeamMembers
#import sending email
from django.core.mail import send_mail

@receiver(pre_save, sender=AddressCheckerUsage)
def address_callback(sender,**kwargs):
    print("Request finished!")


@receiver(post_save, sender=TeamMembers)
def team_callback(sender,instance, **kwargs):
    if instance is not None: 
        #send email whene a new team member is added
        try:
            send_mail(
                subject='New Team Member',
                message='A new team member has been added to your team',
                recipient_list=[instance.team.teamleader.email],
                fail_silently=False,
                from_email=None
            )
        except ObjectDoesNotExist:
            pass
    else: 
        pass



