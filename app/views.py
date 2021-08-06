from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django import template
from . import models
from django.contrib.auth.models import User
from .models import Profile, Product, Mother_Station, Material, Station, Tree, Ticket, Notice, Inventory_history, Station_exit_history, Order_confirmation, Order
from .forms import ProfileForm, UserForm, TicketForm, InventoryForm, Exit_stationForm, OrderForm, Order_confirmation_Form, Add_Order_Form
from itertools import chain
from django.contrib.auth import get_user_model
from django.db import transaction
from django.urls import reverse
from django.db.models import Q
import datetime





#------------------------------------------------------------------------------
@login_required()
def index(request):
    n_material = models.Material.objects.all()
    context = {'n_material':n_material}
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
  n_material = models.Material.objects.all()
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
            context = {'profile': profile,'user_form': user_form,'profile_form': profile_form }
            return render(request, 'page-user.html', context)
  else:
      user_form = UserForm(instance=request.user)
      profile_form = ProfileForm(instance=request.user.profile)

  context = {
  'profile': profile,
  'user_form': user_form,
  'profile_form': profile_form,
  'n_material':n_material }
  return render(request, 'page-user.html', context)





#------------------------------------------------------------------------------
@login_required
def search(request):
    if request.method=="POST":
        search = request.POST['q']
        if search:
            material = models.Material.objects.filter(Q(name__icontains=search) | Q(description__icontains=search))
            product = models.Product.objects.filter(Q(name__icontains=search))
            station = models.Station.objects.filter(Q(name__icontains=search) | Q(description__icontains=search))
            match = chain(material, product, station)
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
    n_material = models.Material.objects.all()
    products = models.Product.objects.all()
    return render(request, 'products.html', {'products': products, 'n_material':n_material})


@login_required()
def products_detail(request, id):
    n_material = models.Material.objects.all()
    product = get_object_or_404(models.Product, id=id)
    order = models.Order.objects.filter(product=product)
    tree = models.Tree.objects.filter(relatedProduct=product)
    bom = models.Bom_product.objects.filter(relatedProduct=product).exclude(material__position='اقلام مصرفی')
    bom_masrafi = models.Bom_product.objects.filter(relatedProduct=product, material__position='اقلام مصرفی')
    material_bom = models.Bom_material.objects.all()
    context = {'product': product, 'tree':tree, 'bom':bom, 'bom_masrafi':bom_masrafi, 'material_bom':material_bom, 'order':order, 'n_material':n_material}
    return render(request, 'products_detail.html', context)




#------------------------------------------------------------------------------
@login_required()
def materials(request):
    n_material = models.Material.objects.all()
    materials = models.Material.objects.all()
    return render(request, 'materials.html', {'materials': materials, 'n_material':n_material})


@login_required()
def materials_detail(request, id):
    n_material = models.Material.objects.all()
    material = get_object_or_404(models.Material, id=id)
    bom = models.Bom_material.objects.filter(relatedProduct=material)
    stations = models.Station.objects.filter(input_material__material__name=material.name)
    exit_station = models.Station.objects.filter(output_material__name=material.name).exclude(position='حمل و نقل')
    bom_material = models.Bom_material.objects.filter(name__name=material.name)
    tree = models.Tree.objects.filter(station__input_material__material__name=material.name)

    context = {
    'material': material,
    'bom':bom,
    'tree':tree,
    'stations':stations,
    'exit_station':exit_station,
    'bom_material':bom_material,
    'n_material':n_material
    }
    return render(request, 'materials_detail.html', context)




#------------------------------------------------------------------------------
@login_required()
def stations(request):
    n_material = models.Material.objects.all()
    stations = models.Station.objects.all()
    return render(request, 'stations.html', {'stations': stations, 'n_material':n_material})


@login_required()
def stations_detail(request, id):
    n_material = models.Material.objects.all()
    station = get_object_or_404(models.Station, id=id)
    products = models.Tree.objects.filter(station__name=station.name)
    inventory_form = InventoryForm(request.POST)
    exit_station_form = Exit_stationForm(request.POST)
    order_confirmation_form = Order_confirmation_Form(request.POST)
    inventory_history = models.Inventory_history.objects.filter(station=station).order_by('-time')
    station_exit_history = models.Station_exit_history.objects.filter(station=station).order_by('-time')
    input = models.Tree.objects.filter(station=station)
    station_products = models.Tree.objects.filter(station=station).values('relatedProduct__name')
    orders = models.Order.objects.filter(product__name__in=station_products)
    order_confirmation_history = models.Order_confirmation.objects.filter(station=station)

    if request.method == 'POST':
        if inventory_form.is_valid():
            obj = get_object_or_404(models.Station, id=id)
            added_value = inventory_form.cleaned_data['inventory_field']
            obj.inventory += added_value
            for input_material in obj.input_material.all():
                material_obj = models.Material.objects.filter(name=input_material.material)
                for Material in material_obj:
                    Material.inventory -= ( input_material.inventory * added_value )
                Material.save()
            obj.save()
            history = Inventory_history()
            history.material = station.output_material
            history.quantity = added_value
            history.manager = station.manager
            history.description = inventory_form.cleaned_data['inventory_description_field']
            history.station = station
            history.save()
            return redirect(obj.get_absolute_url())
        if exit_station_form.is_valid():
            obj = get_object_or_404(models.Station, id=id)
            exit_value = exit_station_form.cleaned_data['exit_station_field']
            obj.inventory -= exit_value
            material_obj = models.Material.objects.filter(name=obj.output_material)
            for Material in material_obj:
                Material.inventory += exit_value
                Material.save()
            obj.save()
            history = Station_exit_history()
            history.material = station.output_material
            history.quantity = exit_value
            history.manager = station.manager
            history.station = station
            history.order_code = exit_station_form.cleaned_data['order_code']
            history.description = exit_station_form.cleaned_data['exit_station_description_field']
            history.save()
            return redirect(obj.get_absolute_url())

        if order_confirmation_form.is_valid():
            obj = Order_confirmation()
            obj.order = order_confirmation_form.cleaned_data['order']
            obj.station = get_object_or_404(models.Station, id=id)
            obj.confirmed = True
            obj.save()
            obj = get_object_or_404(models.Station, id=id)
            return redirect(obj.get_absolute_url())


    context = {'station': station,
    'products':products,
    'inventory_form':inventory_form,
    'exit_station_form':exit_station_form,
    'order_confirmation_form': order_confirmation_form,
    'inventory_history':inventory_history,
    'station_exit_history':station_exit_history,
    'order_confirmation_history':order_confirmation_history,
    'input':input,
    'station_products':station_products,
    'orders':orders,
    'n_material':n_material
    }
    return render(request, 'stations_detail.html', context)




#------------------------------------------------------------------------------
@login_required()
@transaction.atomic
def ticket(request):
    n_material = models.Material.objects.all()
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
            context = {'ticket_form': ticket_form, 'ticket':ticket, 'users':users }
            return render(request, 'ticket.html', context)
        else:
            return HttpResponse("Form Failed to Validate")
    else:
      ticket_form=TicketForm(request.POST, request.FILES, instance=request.user)
      context = {'ticket_form': ticket_form, 'ticket':ticket, 'users':users, 'n_material':n_material }
      return render(request, 'ticket.html', context)




#------------------------------------------------------------------------------
@login_required()
def mother_station(request):
    n_material = models.Material.objects.all()
    mother_station = models.Mother_Station.objects.all()
    return render(request, 'mother_station.html', {'mother_station': mother_station, 'n_material':n_material})



@login_required()
def mother_station_detail(request, id):
    n_material = models.Material.objects.all()
    mother_stations = get_object_or_404(models.Mother_Station, id=id)
    sub_stations = models.Station.objects.filter(mother_station=mother_stations)
    return render(request, 'mother_station_detail.html', {'mother_stations':mother_stations, 'sub_stations':sub_stations, 'n_material':n_material })




#------------------------------------------------------------------------------
@login_required()
def notices(request):
    n_material = models.Material.objects.all()
    notices = models.Notice.objects.all().order_by('-created_on')
    context = {'notices':notices, 'n_material':n_material}
    return render(request, 'notices.html', context)




#------------------------------------------------------------------------------
@login_required()
def orders(request):
    n_material = models.Material.objects.all()
    orders = models.Order.objects.all()
    return render(request, 'orders.html', {'orders': orders, 'n_material':n_material})


@login_required()
def orders_detail(request, id):
    n_material = models.Material.objects.all()
    order = get_object_or_404(models.Order, id=id)
    involved_stations = models.Tree.objects.filter(relatedProduct=order.product)
    involved_materials = models.Tree.objects.filter(relatedProduct=order.product).exclude(station__position='حمل و نقل').exclude(station__position= 'انبار')
    order_form = OrderForm(request.POST)
    order_confirmation = models.Order_confirmation.objects.filter(order=order)
    exit_order = models.Station_exit_history.objects.filter(order_code=order.code)

    if request.method == 'POST':
        if order_form.is_valid():
            obj = get_object_or_404(models.Order, id=id)
            obj.confirmed = order_form.cleaned_data['confirmed']
            obj.completed = order_form.cleaned_data['completed']
            obj.start_time = datetime.datetime.now()
            obj.save()
            return redirect(obj.get_absolute_url())

    context = { 'order': order, 'involved_stations':involved_stations, 'involved_materials':involved_materials, 'order_form':order_form, 'order_confirmation':order_confirmation, 'exit_order':exit_order, 'n_material':n_material }
    return render(request, 'orders_detail.html', context)


@login_required()
def add_order(request):
    n_material = models.Material.objects.all()
    add_order_form = Add_Order_Form(request.POST)
    if request.method == 'POST':
        if add_order_form.is_valid():
            obj = Order()
            obj.product = add_order_form.cleaned_data['product']
            obj.code = add_order_form.cleaned_data['code']
            obj.description = add_order_form.cleaned_data['description']
            obj.circulation = add_order_form.cleaned_data['circulation']
            obj.save()
            return redirect(obj.get_absolute_url())
    else:
        return render(request, 'add_order.html', {'add_order_form': add_order_form, 'n_material':n_material })










# End
