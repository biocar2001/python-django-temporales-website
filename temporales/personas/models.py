# encoding: utf-8
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User


class Salario(models.Model):
	edad = models.IntegerField('Edad salario')
	amount = models.IntegerField('salario bruto anual')

class Oferta(models.Model):
	hours_week = models.IntegerField('horas por semana')
	time_contract = models.IntegerField('duracion contrato')
	salarios = models.ForeignKey(Salario)	
	payment_home = models.BooleanField('casa pagada', default=False)
	payment_healthcare = models.BooleanField('seguro medico pagado', default=False)

class Empresa(models.Model):
	nombre = models.CharField('nombre', max_length=250)
	ett = models.CharField('ett a la que pertenece', max_length=250)
	localizacion = models.CharField('localizacion fisica de la empresa', max_length=500)
	ofertas = models.ForeignKey(Oferta)	

class Persona(models.Model):
	nombre = models.CharField('nombre', max_length=250)
	apellidos = models.CharField('apellidos', max_length=500)
	observaciones = models.TextField('observaciones', blank=True)
	is_active = models.BooleanField('usuario asignado', default=False)
	date_born = models.DateTimeField('fecha nacimiento')
	english_level = models.IntegerField('nivel ingles')
	empresa = models.OneToOneField(Empresa, blank=True)
	