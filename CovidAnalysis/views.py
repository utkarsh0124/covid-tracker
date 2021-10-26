

from django.http import response
from django.http import HttpResponse
from django.shortcuts import render

def home_view(request):
    params = {'SNo' : 1,
            'StateName' : 'Andaman & Nocobar',
        	'ActiveToday' : 100,
            'TotalDeaths' : 0,
            'TotalDischarged' : 100
            }
    return render(request, 'home.html', params)

