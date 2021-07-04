from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django import template
from . import models
from django.contrib.auth.models import User
from .models import Profile, Product, Mother_Station, Material, Station, Tree, Ticket, Notice
#from .forms import ProfileForm, UserForm, TicketForm, MaterialForm, StationForm, RepositoryForm, TransferForm, InventoryForm, ConfirmationForm
from itertools import chain
from django.contrib.auth import get_user_model
from django.db import transaction
from django.urls import reverse









#------------------------------------------------------------------------------
@login_required()
def index(request):
    a = "a"
    context = {'a':a}
    return render(request, 'index.html', context)




#------------------------------------------------------------------------------
@login_required()
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template      = request.path.split('/')[-1]
        context['segment'] = load_template

        html_template = loader.get_template( load_template )
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template( 'page-404.html' )
        return HttpResponse(html_template.render(context, request))

    except:

        html_template = loader.get_template( 'page-500.html' )
        return HttpResponse(html_template.render(context, request))

















# End
