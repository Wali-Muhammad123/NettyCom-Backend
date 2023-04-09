from django.conf import settings

def geourlmaker(*args,**kwargs):
    #making sure that all parameters are present in kwargs
    params=['postal_code','state','city']
    for param in params:
        if param not in kwargs.keys():
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
