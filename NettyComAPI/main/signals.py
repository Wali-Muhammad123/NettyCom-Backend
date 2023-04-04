from django.core.db.signals import pre_save
from django.dispatch import receiver

@receiver(pre_save, sender=AddressCheckerUsage)
def address_callback(sender,**kwargs):
    print("Request finished!")


