from django.core.db.signals import pre_save,post_save, m2m_changed
from django.dispatch import receiver
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
                'New Team Member',
                'A new team member has been added to your team',
                [instance.team.teamleader.email],
                fail_silently=False,
            )
        except:
            pass
    else: 
        pass



