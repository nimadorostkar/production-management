from django.urls import path, re_path
from app import views

app_name='app'




urlpatterns = [
    # Matches any html file
    re_path(r'^.*\.html', views.pages, name='pages'),
    # The home page
    path('', views.index, name='home'),
    # products
    path('products', views.products, name='products'),
    path('products_detail/<int:id>/',views.products_detail,name='products_detail'),
    # material
    path('materials', views.materials, name='materials'),
    path('materials_detail/<int:id>/',views.materials_detail,name='materials_detail'),
    # stations
    path('stations', views.stations, name='stations'),
    path('stations_detail/<int:id>/',views.stations_detail,name='stations_detail'),
    # mother stations
    path('mother_station', views.mother_station, name='mother_station'),
    path('mother_station_detail/<int:id>/',views.mother_station_detail,name='mother_station_detail'),
    # other
    path('profile', views.profile, name='profile'),
    path('search',views.search,name='search'),
    path('ticket',views.ticket,name='ticket'),
    path('notices',views.notices,name='notices'),
    ]
