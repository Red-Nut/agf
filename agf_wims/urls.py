
from django.urls import path

from . import views

urlpatterns = [
    path('wells', views.WellPage, name='wells'),
]
