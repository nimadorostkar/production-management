from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django import template
from . import models
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Profile, Supplier, Ticket, Order, Process, Mother_Station, Notice, Confirmation
from django.utils.translation import ugettext_lazy as _
from .forms import ProfileForm, UserForm, TicketForm, MaterialForm, StationForm, RepositoryForm, TransferForm, InventoryForm, ConfirmationForm
from itertools import chain
from django.contrib.auth import get_user_model
from django.db import transaction
from django.urls import reverse
from django.views.generic.base import TemplateView






################################# index ######################################

@login_required()
def index(request):
    a = 'nnn'
    context = {'a':a}
    return render(request, 'index.html', context)




################################# pages ######################################

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





################################# search #####################################

@login_required
def search(request):
    a = 'nnn'
    context = {'a':a}
    return render(request, 'search.html', context)






################################ products ####################################

@login_required()
def products(request):
    a = 'nnn'
    context = {'a':a}
    return render(request, 'products.html', context)


@login_required()
def products_detail(request, id):
    a = 'nnn'
    context = {'a':a}
    return render(request, 'products_detail.html', context)




################################ processes ###################################

@login_required()
def processes(request):
    processes= models.Process.objects.all()
    return render(request, 'processes.html', {'processes': processes})


@login_required()
def processes_detail(request, id):
    a = 'nnn'
    context = {'a':a}
    return render(request, 'processes_detail.html', context)




############################# profile ########################################

@login_required
def profile(request):
  profile = models.Profile.objects.filter(user=request.user)
  if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            username = user_form.cleaned_data['username']
            first_name = user_form.cleaned_data['first_name']
            last_name = user_form.cleaned_data['last_name']
            email = user_form.cleaned_data['email']
            password1 = user_form.cleaned_data['password1']
            password2 = user_form.cleaned_data['password2']
            phone = profile_form.cleaned_data['phone']
            address = profile_form.cleaned_data['address']
            user_photo = profile_form.cleaned_data['user_photo']
            user_form.save()
            profile_form.save()
            messages.success(request, _('Your profile was successfully updated!'))
            context = {'profile': profile,'user_form': user_form,'profile_form': profile_form }
            return render(request, 'page-user.html', context)
        else:
            messages.error(request, _('Please correct the error below.'))
  else:
      user_form = UserForm(instance=request.user)
      profile_form = ProfileForm(instance=request.user.profile)

  context = {
  'profile': profile,
  'user_form': user_form,
  'profile_form': profile_form }
  return render(request, 'page-user.html', context)





################################# ticket #####################################

@login_required()
@transaction.atomic
def ticket(request):
    send_tickets = models.Ticket.objects.filter(user=request.user).order_by('-created_on')
    received_tickets = models.Ticket.objects.filter(to=request.user).order_by('-created_on')
    ticket = chain(send_tickets, received_tickets)
    User = get_user_model()
    users = User.objects.all()
    if request.method == 'POST':
        ticket_form=TicketForm(request.POST, request.FILES, instance=request.user)
        if ticket_form.is_valid():
            obj = Ticket() #gets new object
            obj.title = ticket_form.cleaned_data['title']
            obj.descriptions = ticket_form.cleaned_data['descriptions']
            obj.to = ticket_form.cleaned_data['to']
            obj.user = ticket_form.created_by=request.user
            obj.save()
            #messages.success(request, _('done successfully !'))
            context = {'ticket_form': ticket_form, 'ticket':ticket, 'users':users }
            return render(request, 'ticket.html', context)
        else:
            return HttpResponse("Form Failed to Validate")
    else:
      ticket_form=TicketForm(request.POST, request.FILES, instance=request.user)
      context = {'ticket_form': ticket_form, 'ticket':ticket, 'users':users }
      return render(request, 'ticket.html', context)





############################### order ##################################

@login_required()
def order(request):
    a = 'nnn'
    context = {'a':a}
    return render(request, 'order.html', context)




########################### orders_detail ###############################

@login_required()
def orders_detail(request, id):
    a = 'nnn'
    context = {'a':a}
    return render(request, 'orders_detail.html', context)





############################### supplier ##################################

@login_required()
def supplier(request):
    a = 'nnn'
    context = {'a':a}
    return render(request, 'supplier.html', context)




########################### supplier_detail ###############################

@login_required()
def supplier_detail(request, id):
    a = 'nnn'
    context = {'a':a}
    return render(request, 'supplier_detail.html', context)






############################### mother_station ################################

@login_required()
def mother_station(request):
    a = 'nnn'
    context = {'a':a}
    return render(request, 'mother_station.html', context)




########################### mother_station_detail #############################

@login_required()
def mother_station_detail(request, id):
    a = 'nnn'
    context = {'a':a}
    return render(request, 'mother_station_detail.html', context)







################################# notices #####################################

@login_required()
def notices(request):
    a = 'nnn'
    context = {'a':a}
    return render(request, 'notices.html', context)














# End
