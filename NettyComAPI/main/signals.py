from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.db.utils import IntegrityError
from rest_framework.response import Response
from rest_framework import status
from .models import AddressCheckerUsage, Teams, TeamMembers, AgentProfile
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
@receiver(post_save, sender=Teams)
def team_trans(sender,instance,**kwargs):
    #create a new team member when a new team is created
    team_name=instance.team_name
    team_member=instance.teamleader
    try:
        teamTrans=TeamMembers.objects.create(team_name=team_name,team_lead=team_member)
        agent=AgentProfile.objects.get(uuid=team_member)
        agent.isTeamLeader=True
        agent.save()
        teamTrans.save()
    except IntegrityError as e: 
        return Response({'msg':'Error Creating Team'}, status=status.HTTP_400_BAD_REQUEST)

