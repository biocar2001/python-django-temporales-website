from django import forms
from personas.models import *
from django.db import models
from django.forms import ModelForm

class EmpresasForm(ModelForm):
    #Campos
    nombre= forms.CharField(widget=forms.widgets.TextInput(attrs={'class':'form-control'}), required=True)
    descripcion= forms.CharField(widget=forms.widgets.TextInput(attrs={'class':'form-control'}), required=True)
    id = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Empresa
        fields = ('nombre', 'descripcion', 'id')

class OfertaForm(ModelForm):
    puesto = forms.CharField(label="Descripcion Puesto",widget=forms.widgets.TextInput(attrs={'class':'form-control'}), required=True)
    hours_week = forms.CharField(label="Numero Horas Semana",widget=forms.widgets.TextInput(attrs={'class':'form-control'}), required=True)
    time_contract = forms.CharField(label="Numero Meses Contrato",widget=forms.widgets.TextInput(attrs={'class':'form-control'}), required=True)
    salarios = forms.CharField(label="Tabla de Salarios",widget=forms.widgets.Textarea(attrs={'class':'form-control'}), required=False)
    prize_home = forms.CharField(label="Precio Casa",widget=forms.widgets.TextInput(attrs={'class':'form-control','placeholder':'Debes usar 9 digitos maximo con 2 decimales, ejemplo: 200.00'}), required=True)
    prize_healthcare = forms.CharField(label="Precio Seguro Medico",widget=forms.widgets.TextInput(attrs={'class':'form-control','placeholder':'Debes usar 9 digitos maximo con 2 decimales, ejemplo: 200.00'}), required=True)
    id = forms.CharField(widget=forms.HiddenInput(), required=False)
    class Meta:
        model = Oferta
        fields = ('puesto', 'hours_week','time_contract','salarios','prize_home','prize_healthcare', 'id')