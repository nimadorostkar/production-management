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






#------------------------------------------------------------------------------
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





#------------------------------------------------------------------------------
@login_required
def search(request):
    if request.method=="POST":
        search = request.POST['q']
        if search:
            process = models.Process.objects.filter(Q(name__icontains=search) | Q(description__icontains=search))
            product = models.Product.objects.filter(Q(name__icontains=search) | Q(description__icontains=search))
            match = chain(process, product)
            if match:
                return render(request,'search.html', {'sr': match})
            else:
                messages.error(request,  '   چیزی یافت نشد ، لطفا مجددا جستجو کنید ' )
        else:
            return HttpResponseRedirect('/search')
    return render(request, 'search.html', {})






#------------------------------------------------------------------------------
@login_required()
def products(request):
    products= models.Product.objects.all()
    return render(request, 'products.html', {'products': products})


@login_required()
def products_detail(request, id):
    product = get_object_or_404(models.Product, id=id)
    nodes = models.Tree.objects.filter(relatedProduct=product)
    orders = models.Order.objects.filter(product=product)
    tree = models.Tree.objects.all()
    all_orders = models.Order.objects.all()
    processes= models.Process.objects.all()

    return render(request, 'products_detail.html', {'product': product,
    'nodes': nodes,
    'orders':orders,
    'tree':tree,
    'processes':processes,
    'all_orders':all_orders
    })





#------------------------------------------------------------------------------
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





#------------------------------------------------------------------------------
@login_required()
def mother_station(request):
    mother_station = models.Mother_Station.objects.all()
    return render(request, 'mother_station.html', {'mother_station': mother_station})



@login_required()
def mother_station_detail(request, id):
    mother_stations = get_object_or_404(models.Mother_Station, id=id)
    processes = models.Process.objects.filter(mother_station=mother_stations)
    return render(request, 'mother_station_detail.html', {'mother_stations':mother_stations, 'processes':processes })





#------------------------------------------------------------------------------
@login_required()
def notices(request):
    notices = models.Notice.objects.all().order_by('-created_on')
    context = {'notices':notices}
    return render(request, 'notices.html', context)







# End
