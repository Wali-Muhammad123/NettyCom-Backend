import json
import requests
from django.conf import settings
from rest_framework.response import Response
from .utilfunc import geourlmaker, parsegeojson, matrixrouter, matrix_parser
from .exceptions import FailedGeoJSONError, TimeOutError, NullQueryError
from .models import Directories, AddressCheckerUsage
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
            customerMatrix=self.geocodecustomer(kwargs)
            self.geocustomer=customerMatrix[0]
            self.geocustloc=customerMatrix[1]
             #coordinates of the customer's geocode, geocustloc: Is a list that contains the state and postal code and city of the customer's location
    def geocodecustomer(self,*args,**kwargs): 
        '''
        This method is used to geocode the customer's address. 
        '''
        try:
            url=geourlmaker(kwargs)
            response=requests.get(url=url, timeout=10)
            geocode=parsegeojson(response)
            if geocode[0] and geocode[1]:
                return [geocode[0],geocode[1]],[geocode[2],geocode[3],geocode[4]]
            else:
                raise FailedGeoJSONError
        except FailedGeoJSONError:
            return Response({'msg':'Failed fetching geocode for customer'},status=400) 
        except TimeoutError:
            return Response({'msg':'Fetching GeoCode timed out.'}, status=400)
    def fullsearch(self,*args,**kwargs):
        '''
        This method is used to execute a full search for the customer's location in the working state.
        '''
        queryset=Directories.objects.filter(state=self.geocustloc[0])
        if queryset is None:
            raise NullQueryError
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
                    rel_dir=queryset[minRoute[0]]
                    dir_radius=rel_dir.radius_mile
                    if dir_radius:
                        if self.radiusComparer(minRoute[1],dir_radius):
                            new_dir=Directories.objects.create(postal_code=self.geocustloc[0],
                                                               state=self.geocustloc[1],
                                                               city=self.geocustloc[2],
                                                               radius_mile=None,
                                                               coordinates={'lat':self.geocustomer[0],'lon':self.geocustomer[1]})
                            new_dir.save()
                            return [queryset[minRoute[0]], self.geocustloc, minRoute[2]]
                        else:
                            return Response({'msg':'No directory found within the working radius'},status=400)
                    else:
                        raise NullQueryError
                    
                #rigorous handling of more http-codes must be added from here on
            except TimeoutError as exc:
                raise TimeOutError from exc
    def radiusComparer(self,distance,rel_radius):
        '''
        This method is used to compare the minRoute computed to the working radius of relevant directory
        '''
        if distance <= rel_radius+10:
            return True
        else:
            return False 

    def __str__(self) -> str:
        return f'{self.postal_code},{self.state},{self.city}'