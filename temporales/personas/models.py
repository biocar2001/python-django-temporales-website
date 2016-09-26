# encoding: utf-8
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from datetime import date, datetime, timedelta, time
from django.utils.timezone import now

class Salario(models.Model):
    nombre = models.CharField('nombre salario', max_length=250,default='no name')
    edad = models.IntegerField('Edad salario')
    amount = models.IntegerField('salario bruto anual')
    def __str__(self):              # __unicode__ on Python 2
        return self.nombre

class Oferta(models.Model):
    nombre = models.CharField('nombre oferta', max_length=250,default='no name')
    hours_week = models.IntegerField('horas por semana')
    time_contract = models.IntegerField('duracion contrato')
    salarios = models.ForeignKey(Salario)
    payment_home = models.BooleanField('casa pagada', default=False)
    payment_healthcare = models.BooleanField('seguro medico pagado', default=False)
    def __str__(self):              # __unicode__ on Python 2
        return self.nombre

class Empresa(models.Model):
    nombre = models.CharField('nombre', max_length=250,default='no name')
    ett = models.CharField('ett a la que pertenece', max_length=250)
    localizacion = models.CharField('localizacion fisica de la empresa', max_length=500)
    ofertas = models.ForeignKey(Oferta)
    def __str__(self):              # __unicode__ on Python 2
        return self.nombre

class Persona(models.Model):
    nombre = models.CharField('nombre', max_length=250,default='no name')
    apellidos = models.CharField('apellidos', max_length=500)
    observaciones = models.TextField('observaciones', blank=True)
    is_active = models.BooleanField('usuario asignado', default=False)
    date_born = models.DateField('fecha nacimiento')
    english_level = models.IntegerField('nivel ingles')
    empresa = models.ForeignKey(Empresa)
    def __str__(self):              # __unicode__ on Python 2
        return self.nombre
    def age(self):
        diff = (now().date().today() - self.date_born).days
        years = str(int(diff/365))
        return years
    def ingles(self):
        level=''
        if self.english_level == 1:
            level='Bajo'
        elif self.english_level == 2:
            level='Medio'
        elif self.english_level == 3:
            level='Alto'
        return level