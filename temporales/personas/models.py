# encoding: utf-8
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from datetime import date, datetime, timedelta, time
from django.utils.timezone import now


class Empresa(models.Model):
    nombre = models.CharField('nombre', max_length=250,default='no name')
    descripcion = models.CharField('Descripcion', max_length=250, default='no name')
    def __str__(self):              # __unicode__ on Python 2
        return self.nombre

class Oferta(models.Model):
    puesto = models.CharField('puest de la oferta', max_length=250,default='no name', blank=True, null=True)
    hours_week = models.IntegerField('horas por semana', blank=True, null=True)
    time_contract = models.IntegerField('duracion contrato', blank=True, null=True)
    salarios = models.CharField('Salarios Oferta', max_length=900,default='no name', blank=True, null=True)
    prize_home = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True)
    prize_healthcare = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True)
    empresa = models.ForeignKey(Empresa, blank=True, null=True)
    def __str__(self):              # __unicode__ on Python 2
        return self.puesto
    def des_hours_week(self):
        return str(self.hours_week)+" Horas"
    def des_prize_home(self):
        return str(self.prize_home) + " €"
    def des_prize_healthcare(self):
        return str(self.prize_healthcare) + " €"

class Persona(models.Model):
    nombre = models.CharField('nombre', max_length=250,default='no name')
    apellidos = models.CharField('apellidos', max_length=500)
    sexo = models.IntegerField('sexo')
    observaciones = models.TextField('observaciones', blank=True)
    is_active = models.BooleanField('usuario asignado', default=False)
    date_born = models.DateField('fecha nacimiento')
    english_level = models.IntegerField('nivel ingles')
    empresa = models.ForeignKey(Empresa, blank=True, null=True)
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
    def des_sex(self):
        sex=''
        if self.sexo == 1:
            sex='Hombre'
        elif self.english_level == 2:
            sex='Mujer'
        return sex