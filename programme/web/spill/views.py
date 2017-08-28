from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.clickjacking import xframe_options_exempt

import datetime
import os
import sys
from .forms import Dispatch

chemin = os.path.dirname(os.path.abspath(__file__))
programme = os.path.abspath(chemin + '/../..')
sys.path.append(programme)
import annus
import officia

lyear = annus.LiturgicalCalendar()
language = 'francais'
host = 'theochrone.fr'
# Create your views here.

@xframe_options_exempt
def main(request):
    """The only view used by the whole app.
    Every other function inframe must redirect to this one"""
    dispatch = Dispatch(request.GET or None)
    page = 'day'
    if dispatch.is_valid():
        page = dispatch.cleaned_data['page']
    return render(request, 'spill/main.html',locals())

def day(request):
    """Returns value for one date"""
    # faire un forms pour la validation
    day = None # on traite les éléments GET
    if not day:
        day = datetime.date.today()
    lyear(day.year)
    data = lyear[day] # data of requested day
    hashtag = "resultup"
    link_to_day = datetime_to_link(day,host,hashtag)
    link_to_tomorrow = datetime_to_link(day + datetime.timedelta(1),host,hashtag)
    link_to_yesterday = datetime_to_link(day - datetime.timedelta(1),host,hashtag)
    return render(request,'spill/day.html',locals())
    
def create_module(request):
    """A function to help customers
    to create modules for their blogs"""
    pass

def test(request):
    """A view to test functions online"""
    return day(request)

def datetime_to_link(day,host,hashtag='',s='s'): # should be moved to officia
    """Take a datetime.date like object
    and return a link to requested host.
    Hashtag can be set to point to a specific id on the page
    s is a s of https: default is 's'"""
    link = "http{}://{}/kalendarium/date_seule?date_seule_day={}&date_seule_month={}&date_seule_year={}#{}".format(
        s,host,day.day,day.month,day.year,hashtag)
    return link
