from django.core.exceptions import ObjectDoesNotExist
from rest_framework.exceptions import PermissionDenied
from .models import SalesData

def _saleRetriever(uuid):
    '''
    This method is used to retrieve sales of a particular agent. 
    '''
    try:
        queryset=SalesData.objects.get_queryset(agent=uuid)
        return len(queryset)
    except ObjectDoesNotExist:
        return 0
