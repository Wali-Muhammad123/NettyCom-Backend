from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.db.utils import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from logging import log
from .models import AddressCheckerUsage, Teams,TeamMembers, AgentProfile, SalesData, Finance, CommisionEarned
from .serializers import FinanceSerializer
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
    except IntegrityError: 
        return Response({'msg':'Error Creating Team'}, status=status.HTTP_400_BAD_REQUEST)
@receiver(post_save, sender=SalesData)
def sales_callback(sender,instance,created,**kwargs):
    if not created and instance.status=='Completed':
        #send mail when a sale is completed
        try:
            _instance=Finance.objects.create(user=instance.agent,associated_sale=instance)
            try:
                #check if the sale is made by agent or a team leader
                if instance.agent.isTeamLeader:
                    _instance.save()
                    send_mail(
                        subject='Sale Completed',
                        message=f'Your sale number {instance.id} has been completed. The amount deposited in your account is {_instance.amount_recieved}',
                        recipient_list=[instance.agent.email],
                        fail_silently=False,
                        from_email=None
                    )
                else:
                    agent_uuid=instance.agent.uuid
                    try:
                        #Extracting the team leader of the particular agent
                        team=TeamMembers.objects.get(member=agent_uuid)
                        team_leader=Teams.objects.get(team_name=team.team_name)
                        #Serializing the sale data for commision earned
                        finance_data=FinanceSerializer(_instance).data
                        commission=_instance.amount_recieved*0.01 #10% commission
                        #Extracting the commission profile of team leader and updating the amount earned
                        commision_profile=CommisionEarned.objects.get(teamleader=team_leader)
                        commision_profile.amount_earned+=commission
                        commision_profile.details[finance_data['id']]=finance_data
                        commision_profile.save()
                    except ObjectDoesNotExist:
                        ...
            except TypeError as e:
                pass
            except IntegrityError as e:
                pass
        except ObjectDoesNotExist:
            pass
@receiver(post_save,sender=AgentProfile)
def agent_callback(sender,instance,**kwargs):
    #create an instance of commison model if agent becomes a team leader
    if instance.isTeamLeader:
        instance.level=2
        instance.save()
        try:
            _instance=CommisionEarned.objects.create(teamleader=instance)
            _instance.save()
        except IntegrityError:
            pass
    else:
        raise PermissionDenied('You are not allowed to perform this action')


            