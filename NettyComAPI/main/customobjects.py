import cryptography

class BankDetails:
    '''
    This class is used to store bank details of a customer.
    '''
    def __init__(self, account_number, bank_name):
        self.account_number = account_number
        self.bank_name=bank_name
    def __str__(self) -> str:
        return f'{self.account_number},{self.bank_name}'
