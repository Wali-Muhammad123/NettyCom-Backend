from django.urls import path, include
from .views import index, TeamView, SaleView, TeamSales
from rest_framework.routers import DefaultRouter
r=DefaultRouter()
r.register(prefix='teamsales',viewset=TeamSales,basename='teamsales')
urlpatterns=[
    path('',index,name='index'),
    path('team/',TeamView.as_view(),name='createteam'),
    path('sales/',SaleView.as_view(),name='sales'),
]