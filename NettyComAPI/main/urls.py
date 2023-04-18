from django.urls import path, include
from .views import index, TeamView
urlpatterns=[
    path('',index,name='index'),
    path('team/',TeamView.as_view(),name='createteam'),
]