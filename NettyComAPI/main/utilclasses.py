import requests
from django.conf import settings
import json 
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
    def __str__(self) -> str:
        return f'{self.postal_code},{self.state},{self.city}'


