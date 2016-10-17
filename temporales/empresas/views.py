
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
            descripcion = request.POST.get('descripcion', '')
            idEmpresa = request.POST.get('id', '')
            ofertas=None

            if idEmpresa !="":
                try:
                    newEmpresa = Empresa.objects.get(pk = idEmpresa)
                    newEmpresa.nombre = nombre
                    newEmpresa.descripcion = descripcion
                    newEmpresa.save()

                except:
                    print "Error in get for saving empresa"
            else:
                newEmpresa = Empresa(nombre = nombre, descripcion = descripcion)
                newEmpresa.save()

            #except:
            #    print "Error in save persona"
            personas = Empresa.objects.order_by('nombre')
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
            if idEmpresa !="":
                return render(request, 'indexEmpresas.html', {'empresas':contacts,})
            else:
                form = EmpresasForm(instance=newEmpresa)
                return render(request, 'newEmpresa.html', {'form':form,})
    else:
        form = EmpresasForm()
    return render(request, 'newEmpresa.html', {'form':form,})

@login_required
def detailEmpresa(request, idempresa):
    meta = request.META
    ruta = meta['SCRIPT_NAME']
    empresa = Empresa.objects.get(pk = idempresa)
    form = EmpresasForm(instance=empresa)
    return render(request, 'newEmpresa.html', {'form':form,'ofertas':empresa.oferta_set.all(),})

@login_required
def new_oferta(request, idempresa):
    meta = request.META
    ruta = meta['SCRIPT_NAME']
    if request.method == 'POST':
        form = OfertaForm(data=request.POST)
        if form.is_valid():
            #try:
            puesto = request.POST.get('puesto', '')
            hours_week = request.POST.get('hours_week', '')
            idOferta = request.POST.get('id', '')
            salarios=request.POST.get('salarios', '')
            time_contract = request.POST.get('time_contract', '')
            prize_home = request.POST.get('prize_home', '')
            prize_healthcare = request.POST.get('prize_healthcare', '')
            empresa = Empresa.objects.get(pk = idempresa)
            if idOferta !="":
                try:
                    newOferta = Oferta.objects.get(pk = idOferta)
                    newOferta.puesto = puesto
                    newOferta.hours_week = hours_week
                    newOferta.time_contract = time_contract
                    newOferta.prize_home = prize_home
                    newOferta.prize_healthcare = prize_healthcare
                    newOferta.save()

                except:
                    print "Error in get for saving empresa"
            else:
                newOferta = Oferta(puesto = puesto, hours_week = hours_week, salarios = salarios, time_contract = time_contract, prize_home = prize_home, prize_healthcare = prize_healthcare, empresa = empresa)
                newOferta.save()

            form = EmpresasForm(instance=empresa)
            '''
            paginator = Paginator(ofertas, 10)
            page = request.GET.get('page')
            try:
                contacts = paginator.page(page)
            except PageNotAnInteger:
                # If page is not an integer, deliver first page.
                contacts = paginator.page(1)
            except EmptyPage:
                # If page is out of range (e.g. 9999), deliver last page of results.
                contacts = paginator.page(paginator.num_pages)'''
            return render(request, 'newEmpresa.html', {'form':form, 'ofertas':empresa.oferta_set.all(),})
    else:
        form = OfertaForm()
    return render(request, 'newOferta.html', {'form':form,'idEmpresa':idempresa,})

@login_required
def detailOferta(request, idoferta, idempresa):
    meta = request.META
    ruta = meta['SCRIPT_NAME']
    oferta = Oferta.objects.get(pk = idoferta)
    form = OfertaForm(instance=oferta)
    return render(request, 'newOferta.html', {'form':form,'idEmpresa':idempresa,})
