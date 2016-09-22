# -*- coding: utf-8 -*-
from django.http import *
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils import timezone
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, Context, loader
from django.contrib.auth.decorators import login_required
from datetime import date, datetime
from django.db.models import *


import math
import locale
import json

#######################################################################################
# Nombre: aplicaFiltroPers                                                            #
# Parametros: request                                                                 #
# Respuesta: HttpResponse - content_type=text/plain                                   #
# Descripcion:Dentro de cualquier listado de procesos, en cualquiera de los 4 modulos #
# Podemos generar nuevos filtros de busquedas pulsando el boton filtrar, donde se abre#
# una nueva ventana donde aplicar nuevos filtros, una vez seleccionado lo que queremos
# al pulsar Filtrar invocamos a esta funcion                                          #
#######################################################################################
@login_required
def aplicaFiltroPers(request):
	#Comprobamos que se trata de una llamada ajax y no una llamada realizada desde un navegador o c�digo malicioso
	if request.is_ajax():
		idFiltro = request.POST['idFiltro']
		filtroPers = FiltroPers.objects.get(pk=idFiltro)

		filtro = filtroPers.filtro.split('$')
		listaSalida = []
		for f in filtro:
			listaSalida.append(f)
		listaSalida = listaSalida[0:len(listaSalida) - 1] # para quitar el ?ltimo caracter '$'
		listaSalida = json.dumps(listaSalida)
		return HttpResponse(listaSalida, content_type="application/json")
	else:
		meta = request.META
		ruta = meta['SCRIPT_NAME']
		messages.error(request, "No tiene permisos para realizar esta llamada, se trata de una llamada para el sistema")
		print ('Acceso AJAX en comun.aplicaFiltroPers incorrecto por detras del sistema')
		return HttpResponseRedirect(ruta)