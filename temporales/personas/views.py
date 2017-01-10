
from django.contrib.auth.decorators import login_required
from models import *
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
import pickle

@login_required(login_url="login/")
def home(request):
    return render(request,"home.html")

@login_required
def indexPersonas(request):
    meta=request.META
    ruta=meta['SCRIPT_NAME']
    formFilterAux= FiltrosPersonasForm()
    page = request.GET.get('page')
    if page is None:
        page=1
        try:
            del request.session['qFiltro']
            del request.session['setPersonasFilterd']
        except KeyError:
            pass
        #request.session.pop('setPersonasFilterd')
    if request.method == 'POST':
        form = FiltrosPersonasForm(data=request.POST)
        personas = buildQueryFilter(form,request)
        formFilter = form
        request.session['qFiltro'] = request.POST
        request.session['setPersonasFilterd'] = pickle.dumps(personas.query)
    else:
        if 'qFiltro' in request.session:
            rPost = request.session['qFiltro']
            formFilter = FiltrosPersonasForm(data=rPost)
            personas = Persona.objects.order_by('nombre')
            personas.query = pickle.loads(request.session['setPersonasFilterd'])
        else:
            personas = Persona.objects.order_by('nombre')
            formFilter = formFilterAux
    paginator = Paginator(personas, 10)

    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        contacts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        contacts = paginator.page(paginator.num_pages)
    return render(request, 'indexPersonas.html', {'personas':contacts,'formFilter':formFilter,})

def buildQueryFilter(form,request):
    if form.is_valid():
        queryFinal = Q()
        nombre = request.POST.get('nombre', '')
        if nombre != "":
            queryParcial = Q(nombre__icontains=nombre)
            queryFinal = queryFinal & (queryParcial)
        apellidos = request.POST.get('apellidos', '')
        if apellidos != "":
            queryParcial = Q(apellidos__icontains=apellidos)
            queryFinal = queryFinal & (queryParcial)
        empresa = request.POST.getlist('empresa')
        empresas = map(int, empresa)

        if len(empresas)>0:
            empresasObjetos = Empresa.objects.filter(Q(id__in=empresas))
            queryParcial = Q(empresa__in=empresasObjetos)
            queryFinal = queryFinal & (queryParcial)
        ingles = request.POST.get('ingles', '')
        if ingles != "":
            queryParcial = Q(english_level=ingles)
            queryFinal = queryFinal & (queryParcial)
        sexo = request.POST.get('sexo', '')
        if sexo != "":
            queryParcial = Q(sexo=sexo)
            queryFinal = queryFinal & (queryParcial)

        edad = request.POST.get('edad', '')
        edad = edad.strip()
        if edad != "":
            simbolo= edad[:1]
            if simbolo == '>':
                edad=int(edad[1:])
                max_date = getDateEdad(edad)
                queryParcial = Q(date_born__lte=max_date)
                queryFinal = queryFinal & (queryParcial)
            elif simbolo == '<':
                edad=int(edad[1:])
                max_date = getDateEdad(edad)
                queryParcial = Q(date_born__gte=max_date)
                queryFinal = queryFinal & (queryParcial)
            elif "-"  in edad:
                # rangos
                rangos = edad.split('-')
                max_dateInit = getDateEdad(int(rangos[0]))
                max_dateEnd = getDateEdad(int(rangos[1]))
                init1=datetime(max_dateInit.year,1,1)
                init2=datetime(max_dateEnd.year,1,1)
                queryParcial = Q(date_born__range=(init2,init1))
                queryFinal = queryFinal & (queryParcial)

            else:
                # edad exacta
                edad=int(edad)
                max_date = getDateEdad(edad)
                queryParcial = Q(date_born__year=max_date.year)
                queryFinal = queryFinal & (queryParcial)

        activo = request.POST.get('activo', '')
        if activo == '':
            activo= False
        else:
            activo= True
        queryParcial = Q(is_active=activo)
        queryFinal = queryFinal & (queryParcial)
        personas = Persona.objects.filter(queryFinal).order_by('nombre')
    return personas

def getDateEdad(edad):
    max_date = date.today()
    try:
        max_date = max_date.replace(year=max_date.year - edad)
    except ValueError: # 29th of february and not a leap year
        assert max_date.month == 2 and max_date.day == 29
        max_date = max_date.replace(year=max_date.year - edad, month=2, day=28)
    return max_date

@login_required
def new_persona(request):
    meta = request.META
    ruta = meta['SCRIPT_NAME']
    if request.method == 'POST':
        try:
            del request.session['qFiltro']
            del request.session['setPersonasFilterd']
        except KeyError:
            pass
        form = PersonasForm(data=request.POST)
        if form.is_valid():
            try:
                nombre = request.POST.get('nombre', '')
                apellidos = request.POST.get('apellidos', '')
                telefono = request.POST.get('telefono', '')
                observaciones = request.POST.get('observaciones', '')
                is_active = request.POST.get('is_active', '')
                idPersona = request.POST.get('id', '')
                if is_active == '':
                    is_active= False
                else:
                    is_active= True
                date_born = request.POST.get('date_born', '')
                english_level = request.POST.get('english_level', '')
                sexo = request.POST.get('sexo', '')
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
                        newPersona.telefono = telefono
                        newPersona.observaciones = observaciones
                        newPersona.is_active = is_active
                        newPersona.date_born = date_born
                        newPersona.english_level = english_level
                        newPersona.empresa = newEmpresa
                        newPersona.sexo = sexo
                        newPersona.save()

                    except:
                        print "Error in get for saving persona"
                else:
                    try:
                        newPersona = Persona(nombre = nombre, apellidos = apellidos, telefono = telefono, observaciones = observaciones, is_active = is_active, date_born = date_born, english_level = english_level, empresa =newEmpresa, sexo = sexo)
                        newPersona.save()
                    except:
                        print "Error in saving new persona"

            except Exception as e:
                print "Error in save persona"
                print e
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
            return render(request, 'newPersona.html', {'form':form,})
    else:
        form = PersonasForm()
    return render(request, 'newPersona.html', {'form':form,})

@login_required
def detailPersona(request, idpersona):
    meta = request.META
    ruta = meta['SCRIPT_NAME']
    try:
        persona = Persona.objects.get(pk = idpersona)
    except:
		messages.error(request, 'la persona '+ idpersona + ' no existe' )
		return HttpResponseRedirect(ruta+"/personas/")
    form = PersonasForm(instance=persona)
    return render(request, 'newPersona.html', {'form':form,})

@login_required
def deletePersona(request, idpersona):
    meta = request.META
    ruta = meta['SCRIPT_NAME']
    try:
        persona = Persona.objects.get(pk = idpersona)
        persona.delete()
    except:
		messages.error(request, 'la persona '+ idpersona + ' no existe' )
		return HttpResponseRedirect(ruta+"/personas/")
    return HttpResponseRedirect(ruta+"/personas/")