from rest_framework.exceptions import APIException
from rest_framework import status
class FailedGeoJSONError(Exception):
    #call function if the geojson failed to fetch successfully
    def __init__(self,message="Failed fetching geocode for customer"):
        self.message=message
        super().__init__(self.message)
class InsufficientDataError(Exception):
    #error tracing in case the data supplied to martixrouter() is insufficient
    def __init__(self, message="Insufficient or Bad data provided"):
        self.message=message
        super().__init__(self.message)
class TimeOutError(APIException):
    status_code=status.HTTP_408_REQUEST_TIMEOUT
    default_code='Request Timeout'
    default_detail='Request Timed Out. Try Again Later'

class NullQueryError(APIException):
    status_code=status.HTTP_404_NOT_FOUND
    default_code="Address not found in the working state"
    default_detail="Address not found in the working state"

class DataProcessingFailedError(APIException):
    status_code=status.HTTP_400_BAD_REQUEST
    default_code="Processing Data Matrix Failed. Retry or Try Again Later"
    default_detail="An error occured when processing data of router matrix"