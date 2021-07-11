from django import forms
from allauth.account.forms import SignupForm
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from .models import Profile, Product, Mother_Station, Material, Station, Tree, Ticket, Notice
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm




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
	b = forms.DecimalField(max_digits=30, decimal_places=4)


#------------------------------------------------------------------------------
class Exit_stationForm(forms.Form):
	a = forms.DecimalField(max_digits=30, decimal_places=4)















# Form End
