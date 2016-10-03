
from django.contrib.auth.decorators import login_required
from personas.models import *
from forms import *
from django.template import RequestContext, Context, loader
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, render
from django.conf import settings
from django.http import HttpResponseForbidden
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from decimal import *

from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render
from django.contrib import messages
from django.db.models import Q
from django.db import transaction
from datetime import date, datetime, timedelta
from django.core.exceptions import ObjectDoesNotExist


@login_required
def indexEmpresas(request):
    meta=request.META
    ruta=meta['SCRIPT_NAME']
    formFilter= FiltrosEmpresasForm()
    empresas = Empresa.objects.order_by('nombre')
    paginator = Paginator(empresas, 10)
    page = request.GET.get('page')
    if page is None:
        page=1
    try:
        companies = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        companies = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        companies = paginator.page(paginator.num_pages)
    return render(request, 'indexEmpresas.html', {'empresas':companies,})



@login_required
def new_empresa(request):
    meta = request.META
    ruta = meta['SCRIPT_NAME']
    if request.method == 'POST':
        form = EmpresasForm(data=request.POST)
        if form.is_valid():
            #try:
            nombre = request.POST.get('nombre', '')
            ett = request.POST.get('ett', '')
            localizacion = request.POST.get('localizacion', '')
            ofertas=None
            if empresa == "":
                newEmpresa = Empresa.objects.get(nombre="temporales")
            else:
                newEmpresa = Empresa.objects.get(id=empresa)
            if idPersona !="":
                try:
                    newPersona = Persona.objects.get(pk = idPersona)
                    newPersona.nombre = nombre
                    newPersona.apellidos = apellidos
                    newPersona.observaciones = observaciones
                    newPersona.is_active = is_active
                    newPersona.date_born = date_born
                    newPersona.english_level = english_level
                    newPersona.empresa = newEmpresa
                    newPersona.save()

                except:
                    print "Error in get for saving persona"
            else:
                newPersona = Persona(nombre = nombre, apellidos = apellidos, observaciones = observaciones, is_active = is_active, date_born = date_born, english_level = english_level, empresa =newEmpresa)
                newPersona.save()

            #except:
            #    print "Error in save persona"
            formFilter= FiltrosPersonasForm()
            personas = Persona.objects.order_by('nombre')
            paginator = Paginator(personas, 10)
            page = request.GET.get('page')
            try:
                contacts = paginator.page(page)
            except PageNotAnInteger:
                # If page is not an integer, deliver first page.
                contacts = paginator.page(1)
            except EmptyPage:
                # If page is out of range (e.g. 9999), deliver last page of results.
                contacts = paginator.page(paginator.num_pages)
            return render(request, 'indexPersonas.html', {'personas':contacts,'formFilter':formFilter,})
    else:
        form = EmpresasForm()
    return render(request, 'newEmpresa.html', {'form':form,})

@login_required
def detailPersona(request, idempresa):
    meta = request.META
    ruta = meta['SCRIPT_NAME']
    try:
        empresa = Empresa.objects.get(pk = idempresa)
    except:
		messages.error(request, 'la empresa '+ idempresa + ' no existe' )
		return HttpResponseRedirect(ruta+"/personas/")
    form = EmpresasForm(instance=empresa)
    return render(request, 'newEmpresa.html', {'form':form,})
