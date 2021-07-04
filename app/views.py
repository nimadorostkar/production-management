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
    tree = models.Tree.objects.all()
    orders = models.Order.objects.all()
    processes= models.Process.objects.all()

    context = {'processes':processes, 'orders':orders, 'tree':tree}
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




################################## maps ######################################
'''
class MapView(TemplateView):
    template_name = "ui-maps.html"
'''

@login_required()
def maps(request):
    maps= models.Process.objects.all()
    mapbox_access_token = 'pk.eyJ1IjoiZG9yb3N0a2FyIiwiYSI6ImNrbmVjdzg3djFkb3EycG8wZW5sdjNld3YifQ.AeDSXrxKTXAxPdIEESuPqA'
    return render(request, 'ui-maps.html', {
    'maps': maps,
    'mapbox_access_token': mapbox_access_token}
    )





################################# search #####################################

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






################################ products ####################################

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




################################ processes ###################################

@login_required()
def processes(request):
    processes= models.Process.objects.all()
    return render(request, 'processes.html', {'processes': processes})


@login_required()
def processes_detail(request, id):
    nodes = models.Tree.objects.all()
    process = get_object_or_404(models.Process, id=id)
    processes= models.Process.objects.all()
    input = models.Tree.objects.filter(name=process)
    process_products = models.Tree.objects.filter(name=process).values('relatedProduct__name')
    orders = models.Order.objects.filter(product__name__in=process_products)
    confirmation_history =  models.Confirmation.objects.filter(process=process, order__confirmed=False, order__completed=False)
    if request.method == 'POST':
          confirmation_form=ConfirmationForm(request.POST)
          if confirmation_form.is_valid():
              obj = Confirmation() #gets new object
              obj.order = confirmation_form.cleaned_data['order']
              obj.process = process
              obj.confirmed = True
              obj.save()
              return redirect(process.get_absolute_url())

          inventory_form = InventoryForm(request.POST)
          if inventory_form.is_valid():
              obj = get_object_or_404(models.Process, id=id)
              obj.inventory = inventory_form.cleaned_data['inventory']
              obj.save()
              return redirect(obj.get_absolute_url())
    else:
        confirmation_form=ConfirmationForm(request.POST)
        inventory_form = InventoryForm(request.POST)

    context = { 'process': process,
    'processes': processes,
    'orders': orders,
    'nodes': nodes,
    'input': input,
    'inventory_form':inventory_form,
    'confirmation_form':confirmation_form,
    'confirmation_history':confirmation_history
    }
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
    tree = models.Tree.objects.all()
    orders = models.Order.objects.all()

    context = {'orders':orders, 'tree':tree}
    return render(request, 'order.html', context)




########################### orders_detail ###############################

@login_required()
def orders_detail(request, id):
    order = get_object_or_404(models.Order, id=id)
    orders = models.Order.objects.all()
    nodes = models.Tree.objects.filter(relatedProduct=order.product)
    confirmation = models.Confirmation.objects.filter(order=order)

    return render(request, 'orders_detail.html', {
    'orders': orders,
    'order': order,
    'nodes': nodes,
    'confirmation': confirmation
    })





############################### supplier ##################################

@login_required()
def supplier(request):
    supplier = models.Supplier.objects.all()
    return render(request, 'supplier.html', {'supplier': supplier})




########################### supplier_detail ###############################

@login_required()
def supplier_detail(request, id):
    suppliers = get_object_or_404(models.Supplier, id=id)
    processes = models.Process.objects.filter(supplier=suppliers)
    return render(request, 'supplier_detail.html', {'suppliers':suppliers, 'processes':processes })






############################### mother_station ################################

@login_required()
def mother_station(request):
    mother_station = models.Mother_Station.objects.all()
    return render(request, 'mother_station.html', {'mother_station': mother_station})




########################### mother_station_detail #############################

@login_required()
def mother_station_detail(request, id):
    mother_stations = get_object_or_404(models.Mother_Station, id=id)
    processes = models.Process.objects.filter(mother_station=mother_stations)
    return render(request, 'mother_station_detail.html', {'mother_stations':mother_stations, 'processes':processes })





# ----------------------------------------------------------------------------
# add page for material, station, repository, transfer and product ...

@user_passes_test(lambda u: u.is_superuser)
def add_material(request):
    material = models.Process.objects.all()
    if request.method == 'POST':
          material_form = MaterialForm(request.POST, instance=request.user)
          if material_form.is_valid():
              obj = Process() #gets new object
              obj.name = material_form.cleaned_data['name']
              obj.position = 'M'
              obj.description = material_form.cleaned_data['description']
              obj.inventory = material_form.cleaned_data['inventory']
              obj.min_inventory = material_form.cleaned_data['min_inventory']
              obj.manager = material_form.cleaned_data['manager']
              obj.supplier = material_form.cleaned_data['supplier']
              obj.save()
              messages.success(request, _('Your material was successfully added!'))
              context = {'material': material,'material_form': material_form }
              return render(request, 'add_material.html', context)
          else:
              messages.error(request, _('Please correct the error below.'))
    else:
        material_form = MaterialForm(request.POST)

    context = {'material': material,'material_form': material_form }
    return render(request, 'add_material.html', context)


@user_passes_test(lambda u: u.is_superuser)
def add_station(request):
    station = models.Process.objects.all()
    if request.method == 'POST':
          station_form = StationForm(request.POST, instance=request.user)
          if station_form.is_valid():
              obj = Process() #gets new object
              obj.name = station_form.cleaned_data['name']
              obj.position = 'S'
              obj.description = station_form.cleaned_data['description']
              obj.manager = station_form.cleaned_data['manager']
              obj.pro_cap_day = station_form.cleaned_data['pro_cap_day']
              obj.percent_error = station_form.cleaned_data['percent_error']
              obj.save()
              messages.success(request, _('Your material was successfully added!'))
              context = {'station': station, 'station_form': station_form }
              return render(request, 'add_station.html', context)
          else:
              messages.error(request, _('Please correct the error below.'))
    else:
        station_form = StationForm(request.POST)

    context = {'station': station, 'station_form': station_form }
    return render(request, 'add_station.html', context)



@user_passes_test(lambda u: u.is_superuser)
def add_repository(request):
    repository = models.Process.objects.all()
    if request.method == 'POST':
          repository_form = RepositoryForm(request.POST, instance=request.user)
          if repository_form.is_valid():
              obj = Process() #gets new object
              obj.name = repository_form.cleaned_data['name']
              obj.position = 'R'
              obj.description = repository_form.cleaned_data['description']
              obj.manager = repository_form.cleaned_data['manager']
              obj.save()
              messages.success(request, _('Your material was successfully added!'))
              context = {'repository': repository,'repository_form': repository_form }
              return render(request, 'add_repository.html', context)
          else:
              messages.error(request, _('Please correct the error below.'))
    else:
        repository_form = RepositoryForm(request.POST)

    context = {'repository': repository,'repository_form': repository_form }
    return render(request, 'add_repository.html', context)



@user_passes_test(lambda u: u.is_superuser)
def add_transfer(request):
    transfer = models.Process.objects.all()
    if request.method == 'POST':
          transfer_form = TransferForm(request.POST, instance=request.user)
          if transfer_form.is_valid():
              obj = Process() #gets new object
              obj.name = transfer_form.cleaned_data['name']
              obj.position = 'T'
              obj.description = transfer_form.cleaned_data['description']
              obj.manager = transfer_form.cleaned_data['manager']
              obj.save()
              messages.success(request, _('Your material was successfully added!'))
              context = {'transfer': transfer,'transfer_form': transfer_form }
              return render(request, 'add_transfer.html', context)
          else:
              messages.error(request, _('Please correct the error below.'))
    else:
        transfer_form = TransferForm(request.POST)

    context = {'transfer': transfer,'transfer_form': transfer_form }
    return render(request, 'add_transfer.html', context)





################################# notices #####################################

@login_required()
def notices(request):
    notices = models.Notice.objects.all().order_by('-created_on')
    context = {'notices':notices}
    return render(request, 'notices.html', context)














# End
