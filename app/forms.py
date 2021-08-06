from django import forms
from allauth.account.forms import SignupForm
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from .models import Profile, Product, Mother_Station, Material, Station, Tree, Ticket, Notice, Order, Order_confirmation
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, get_object_or_404, redirect
from . import models


#------------------------------------------------------------------------------
class ProfileForm(forms.ModelForm):
	class Meta:
		model = Profile
		fields = ['phone','address','user_photo']


#------------------------------------------------------------------------------
class UserForm(UserCreationForm):
	class Meta:
		model = User
		fields = ['username','first_name','last_name','email','password1','password2']


#------------------------------------------------------------------------------
class TicketForm(forms.ModelForm):
	to = forms.ModelChoiceField(queryset=User.objects.all(), widget=forms.Select(), error_messages={'required': 'این فیلد ضروری است'} )

	class Meta:
		model = Ticket
		fields = ['to','title','descriptions']


#------------------------------------------------------------------------------
class InventoryForm(forms.Form):
	inventory_field = forms.IntegerField()
	inventory_description_field = forms.CharField(max_length=300)


#------------------------------------------------------------------------------
class Exit_stationForm(forms.Form):
	exit_station_field = forms.IntegerField()
	order_code = forms.CharField(max_length=200)
	exit_station_description_field = forms.CharField(max_length=300)


#------------------------------------------------------------------------------
class OrderForm(forms.ModelForm):
	class Meta:
		model = Order
		fields = ['confirmed', 'completed']



#------------------------------------------------------------------------------
class Order_confirmation_Form(forms.ModelForm):
	order = forms.ModelChoiceField(queryset=Order.objects.filter(confirmed=False, completed=False), widget=forms.Select(), error_messages={'required': 'این فیلد ضروری است'} )

	class Meta:
		model = Order_confirmation
		fields = ['order']


#------------------------------------------------------------------------------
class Add_Order_Form(forms.ModelForm):
	class Meta:
		model = Order
		fields = ['product', 'code', 'description', 'circulation']





# Form End
