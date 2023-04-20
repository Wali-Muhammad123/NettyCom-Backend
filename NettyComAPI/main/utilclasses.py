import requests
from django.conf import settings
import random
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


class FakeNameGen:
    '''
    This class is used to generate name for a team. 
    '''
    def __init__(self):
        self.response=requests.get(self.url_maker())
    def url_maker(self):
        return r'https://names.drycodes.com/10?nameOptions=starwarsCharacters'
    def random_selector(self):
        return random.choice(self.response.json())

