from django.urls import path
from .views import index, MapView
from rest_framework import routers
r=routers.DefaultRouter()
r.register('map',MapView,basename='map')
urlpatterns=[
    path('',index,name='index'),
    path('team/',TeamView.as_view(),name='createteam'),
    path('sales/',SaleView.as_view(),name='sales'),
]