#from django.shortcuts import render
from django.views.generic import ListView

from tracker.models import Application

# Create your views here.

class ListApplicationView(ListView):
    model = Application
