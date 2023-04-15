from django.urls import path
from .views import index, MapView
from rest_framework import routers
r=routers.DefaultRouter()
r.register('map',MapView,basename='map')
urlpatterns=[
    path('',index,name='index'),
]