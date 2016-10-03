
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
    if request.method == 'POST':
        form = FiltrosEmpresasForm(data=request.POST)

        if form.is_valid():
            empresa = request.POST.get('empresa', '')
            queryFinal = Q()
            if empresa != "":
                newEmpresa = Empresa.objects.get(id=empresa)
                queryParcial = Q(empresa=newEmpresa)
                queryFinal = queryFinal & (queryParcial)
            ingles = request.POST.get('ingles', '')
            if ingles != "":
                queryParcial = Q(english_level=ingles)
                queryFinal = queryFinal & (queryParcial)

            edad = request.POST.get('edad', '')
            if edad != "":
                edad=int(edad)
                max_date = date.today()
                try:
                    max_date = max_date.replace(year=max_date.year - edad)
                except ValueError: # 29th of february and not a leap year
                    assert max_date.month == 2 and max_date.day == 29
                    max_date = max_date.replace(year=max_date.year - edad, month=2, day=28)
                queryParcial = Q(date_born__lte=max_date)
                queryFinal = queryFinal & (queryParcial)

            activo = request.POST.get('activo', '')
            if activo == '':
                activo= False
            else:
                activo= True
            queryParcial = Q(is_active=activo)
            queryFinal = queryFinal & (queryParcial)

            personas = Persona.objects.filter(queryFinal).order_by('nombre')

    else:
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
    return render(request, 'indexEmpresas.html', {'empresas':companies,'formFilter':formFilter,})



@login_required
def new_empresa(request):
    meta = request.META
    ruta = meta['SCRIPT_NAME']
    if request.method == 'POST':
        form = EmpresasForm(data=request.POST)
        if form.is_valid():
            #try:
            nombre = request.POST.get('nombre', '')
            apellidos = request.POST.get('apellidos', '')
            observaciones = request.POST.get('observaciones', '')
            is_active = request.POST.get('is_active', '')
            idPersona = request.POST.get('id', '')
            if is_active == '':
                is_active= False
            else:
                is_active= True
            date_born = request.POST.get('date_born', '')
            english_level = request.POST.get('english_level', '')
            empresa = request.POST.get('empresa', '')
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
