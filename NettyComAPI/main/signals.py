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

