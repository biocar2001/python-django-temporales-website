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
    SEXO_CHOICES = (
        ('', '-----'),
        ('1', 'Hombre'),
        ('2', 'Mujer'),
    )
    #FILTROS
    nombre= forms.CharField(widget=forms.widgets.TextInput(attrs={'class':'form-control'}), required=False)
    apellidos= forms.CharField(widget=forms.widgets.TextInput(attrs={'class':'form-control'}), required=False)
    ingles= forms.CharField(widget=forms.Select(choices=MY_CHOICES, attrs={'class':'form-control'}), required= False)
    sexo= forms.CharField(widget=forms.Select(choices=SEXO_CHOICES, attrs={'class':'form-control'}), required= False)
    edad= forms.CharField(widget=forms.widgets.TextInput(attrs={'class':'form-control','placeholder':'ejemplos de opciones: >25, <23, 17-23, 23'}), required=False)
    empresa = forms.ModelMultipleChoiceField(label="ETT",queryset=Empresa.objects.all().order_by('nombre'),widget=forms.SelectMultiple(attrs={'class':'form-control'}),required=False)
    activo= forms.BooleanField(required=False,initial=False, label='Activo')


class PersonasForm(ModelForm):

    MY_CHOICES = (
        ('', '-----'),
        ('1', 'Bajo'),
        ('2', 'Medio'),
        ('3', 'Alto'),
    )
    SEXO_CHOICES = (
        ('', '-----'),
        ('1', 'Hombre'),
        ('2', 'Mujer'),
    )
    #Campos
    nombre= forms.CharField(widget=forms.widgets.TextInput(attrs={'class':'form-control'}), required=True)
    apellidos= forms.CharField(widget=forms.widgets.TextInput(attrs={'class':'form-control'}), required=True)
    telefono= forms.CharField(widget=forms.widgets.TextInput(attrs={'class':'form-control'}), required=True)
    empresa= forms.ModelChoiceField(queryset=Empresa.objects.all().order_by('nombre'), widget=forms.Select(attrs={'class':'form-control'}),required=False)
    english_level= forms.CharField(widget=forms.Select(choices=MY_CHOICES, attrs={'class':'form-control'}), required= True,label='Nivel de Ingles')
    sexo= forms.CharField(widget=forms.Select(choices=SEXO_CHOICES, attrs={'class':'form-control'}), required= True,label='Sexo')
    is_active= forms.BooleanField(widget=forms.CheckboxInput(),required=False,label='Activo')
    date_born= forms.DateField(widget=forms.DateInput(format=('%Y-%m-%d'),attrs={'class':'form-control','placeholder':'Rellena una fecha con formato yyyy-mm-dd'}),required=True)
    observaciones= forms.CharField(widget=forms.widgets.Textarea(attrs={'class':'form-control'}), required=False)
    id = forms.CharField(widget=forms.HiddenInput(), required=False)
    class Meta:
	    model = Persona
	    fields = ('nombre', 'apellidos', 'telefono', 'empresa', 'english_level', 'sexo','is_active', 'date_born', 'observaciones', 'id')


