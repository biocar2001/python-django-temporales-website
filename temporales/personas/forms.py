from django.contrib.auth.forms import AuthenticationForm
from django import forms
from models import *
from django.db import models
from django.forms import ModelForm

# If you don't do this you cannot use Bootstrap CSS
class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Usuario", max_length=30,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'username'}))
    password = forms.CharField(label="Password", max_length=30,
                               widget=forms.PasswordInput(attrs={'class': 'form-control', 'name': 'password'}))

class FiltrosPersonasForm(forms.Form):
	MY_CHOICES = (
	    ('', '-----'),
        ('1', 'Bajo'),
        ('2', 'Medio'),
        ('3', 'Alto'),
    )
	#FILTROS
	empresa= forms.ModelChoiceField(queryset=Empresa.objects.all().order_by('nombre'), widget=forms.Select(attrs={'class':'form-control'}),required=False)
	ingles= forms.CharField(widget=forms.Select(choices=MY_CHOICES, attrs={'class':'form-control'}), required= False)
	edad= forms.CharField(widget=forms.widgets.TextInput(attrs={'class':'form-control','placeholder':'p. ej: 25, 17'}), required=False)
	activo= forms.BooleanField(required=False,initial=False, label='Activo')

class PersonasForm(ModelForm):

	MY_CHOICES = (
	    ('', '-----'),
        ('1', 'Bajo'),
        ('2', 'Medio'),
        ('3', 'Alto'),
    )
	#Campos
	nombre= forms.CharField(widget=forms.widgets.TextInput(attrs={'class':'form-control'}), required=True)
	apellidos= forms.CharField(widget=forms.widgets.TextInput(attrs={'class':'form-control'}), required=True)
	empresa= forms.ModelChoiceField(queryset=Empresa.objects.all().order_by('nombre'), widget=forms.Select(attrs={'class':'form-control'}),required=False)
	date_born= forms.CharField(widget=forms.Select(choices=MY_CHOICES, attrs={'class':'form-control'}), required= True,label='Nivel de Ingles')
	activo= forms.BooleanField(required=False,label='Activo')
	english_level= forms.DateField(widget=forms.DateInput(format=('%Y-%m-%d'),attrs={'class':'form-control','placeholder':'Rellena una fecha con formato yyyy-mm-dd'}),required=True)
	observaciones= forms.CharField(widget=forms.widgets.Textarea(attrs={'class':'form-control'}), required=False)
	#id = forms.CharField(widget=forms.HiddenInput(), required=False)

	class Meta:
	    model = Persona
	    fields = ('nombre', 'apellidos', 'empresa', 'date_born', 'activo', 'fecha_nac', 'observaciones')


