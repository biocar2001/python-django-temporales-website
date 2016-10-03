from django import forms
from personas.models import *
from django.db import models
from django.forms import ModelForm

class EmpresasForm(ModelForm):

	#Campos
	nombre= forms.CharField(widget=forms.widgets.TextInput(attrs={'class':'form-control'}), required=True)
	ett= forms.CharField(widget=forms.widgets.TextInput(attrs={'class':'form-control'}), required=True)
	localizacion= forms.CharField(widget=forms.widgets.TextInput(attrs={'class':'form-control'}), required=True)
	id = forms.CharField(widget=forms.HiddenInput(), required=False)

	class Meta:
	    model = Empresa
	    fields = ('nombre', 'ett', 'localizacion', 'id')

