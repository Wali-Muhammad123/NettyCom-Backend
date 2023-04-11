import json
import requests
from django.conf import settings
from rest_framework.response import Response
from .utilfunc import geourlmaker, parsegeojson, matrixrouter, matrix_parser
from .exceptions import FailedGeoJSONError, TimeOutError
from .models import Directories
class BankDetails:
    '''
    This class is used to store bank details of a customer.
    '''
    def __init__(self, account_number, bank_name):
        self.account_number = account_number
        self.bank_name=bank_name
    def __str__(self) -> str:
        return f'{self.account_number},{self.bank_name}'

class MatrixRouter:
    '''
    This class is used to make a matrix router request to the TomTom API.
    '''
    API_KEY = settings.API_KEY
    def __init__(self,*args,**kwargs):
        if kwargs['postal_code']:
            self.postal_code=kwargs['postal_code']
        if kwargs['state']:
            self.state=kwargs['state']
        if kwargs['city']:
            self.city=kwargs['city']
        self.geocustomer,self.geocustloc=self.geocodecustomer(kwargs) #coordinates of the customer's geocode, geocustloc: Is a list that contains the state and postal code of the customer's location
    def geocodecustomer(self,*args,**kwargs): 
        '''
        This method is used to geocode the customer's address. 
        '''
        try:
            url=geourlmaker(kwargs)
            response=requests.get(url=url, timeout=10)
            geocode=parsegeojson(response)
            if geocode[0] and geocode[1]:
                return [geocode[0],geocode[1]],[geocode[2],geocode[3]]
            else:
                raise FailedGeoJSONError
        except FailedGeoJSONError:
            return Response({'msg':'Failed fetching geocode for customer'},status=400) 
        except TimeoutError:
            return Response({'msg':'Fetching GeoCode timed out.'}, status=400)
    def fullsearch(self,*args,**kwargs):
        queryset=Directories.objects.filter(state=self.geocustloc[0])
        if queryset is None:
            return Response({'msg':'We do not currently work in the state of customer address'},status=201)
        else:
            try:
                json_param=matrixrouter(directories=queryset,customergeocode=self.geocustomer)
                matrix=requests.post(
                    url=f'https://api.tomtom.com/routing/matrix/2?key={self.API_KEY}',
                    headers={'Content-Type' : 'application/json' },
                    json=json_param,
                    timeout=7
                )
                if matrix.status_code==200: 
                    #more conditionals and rigorous handling of exceptions must be added here for case handling
                    minRoute=matrix_parser(matrix.json())
                    return minRoute
                #rigorous handling of more http-codes must be added from here on
            except TimeoutError:
                raise TimeOutError
    def __str__(self) -> str:
        return f'{self.postal_code},{self.state},{self.city}'