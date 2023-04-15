from django.conf import settings
import pandas as pd
import numpy as np
from .serializers import DirectorySerializer
from .exceptions import InsufficientDataError, DataProcessingFailedError

def geourlmaker(*args,**kwargs):
    #making sure that all parameters are present in kwargs
    params=['postal_code','state','city']
    for param in params:
        if param not in kwargs:
            kwargs[param]=None
    if kwargs['postal_code'] and kwargs['state'] and kwargs['city']:
        return f'https://api.tomtom.com/search/2/structuredGeocode.json?countryCode=US&municipality={kwargs["city"]}&countrySubdivision={kwargs["state"]}&postalCode={kwargs["postal_code"]}&view=Unified&key={settings.API_KEY}'
    elif kwargs['postal_code'] and kwargs['state']:
        return f'https://api.tomtom.com/search/2/structuredGeocode.json?countryCode=US&countrySubdivision={kwargs["state"]}&postalCode={kwargs["postal_code"]}&view=Unified&key={settings.API_KEY}'
    elif kwargs['state'] and kwargs['city']:
        return f'https://api.tomtom.com/search/2/structuredGeocode.json?countryCode=US&municipality={kwargs["city"]}&countrySubdivision={kwargs["state"]}&view=Unified&key={settings.API_KEY}'
    elif kwargs['postal_code'] and kwargs['city']:
        return f'https://api.tomtom.com/search/2/structuredGeocode.json?countryCode=US&municipality={kwargs["city"]}&postalCode={kwargs["postal_code"]}&view=Unified&key={settings.API_KEY}'
    elif kwargs['postal_code']:
        return f'https://api.tomtom.com/search/2/structuredGeocode.json?countryCode=US&postalCode={kwargs["postal_code"]}&view=Unified&key={settings.API_KEY}'
    elif kwargs['state']:
        return f'https://api.tomtom.com/search/2/structuredGeocode.json?countryCode=US&countrySubdivision={kwargs["state"]}&view=Unified&key={settings.API_KEY}'
    elif kwargs['city']:
        return f'https://api.tomtom.com/search/2/structuredGeocode.json?countryCode=US&municipality={kwargs["city"]}&view=Unified&key={settings.API_KEY}'
    else:
        return None
def parsegeojson(response):
    '''
    This function is used to parse the json response from the TomTom API.
    '''
    if response.status_code==200:
        data=response.json()
        if data['summary']['numResults']>=1:
            return [data['results'][0]['position']['lat'], #extracting latitude 
                    data['results'][0]['position']['lon'], #extracting longitude
                    data['results'][0]['address']['countrySubdivision'], #extracting State
                    data['results'][0]['address']['postalCode'], #extract postal code
                    data['results'][0]['address']['countrySecondarySubdivision'] #extract city
                    ]
        else:
            return [None,None]
    else:
        return [None,None]
def matrixrouter(directories:list,customergeocode:list):
    try:
        json_dict={
            "origins":[],
            "destinations":[],
            "options":{
            "routeType":"fastest"
                }
        }
    #Serializing the directories relevant
        serialized_dir=DirectorySerializer(directories,many=True)
        if serialized_dir:
            for route in serialized_dir:
                
                json_dict['destinations'].append({"point":
                                                  {"latitude":route['coordinates']['lat'],
                                                   "longitude":route['coordinates']['lon']}})
            json_dict['origins'].append({"point":{
                "latitude":customergeocode[0],
                "longitude":customergeocode[1]
            }})
            return json_dict
        else:
            raise InsufficientDataError
    except (TypeError,ValueError):
        return None
    except InsufficientDataError:
        pass

def meter_to_mile(meter:float):
    return meter/1609.344
def matrix_parser(json_data):
    def _helper(data):
        if data is not np.nan:
            return meter_to_mile(data['lengthInMeters'])
        else:
            return None
    try:
        _data=pd.json_normalize(data=json_data['data'], errors=False, max_level=0)
        _data['routeSummary']=_data['routeSummary'].apply(_helper)
        _dataNew=_data[_data.routeSummary.notnull()]
        if _dataNew:
            minRoute =_dataNew[_dataNew.routeSummary==_data.routeSummary.min()]
            return [
                minRoute['originIndex'],
                minRoute['destinationIndex'],
                minRoute['routeSummary'],
            ]
    except KeyError as exc:
        raise DataProcessingFailedError from exc