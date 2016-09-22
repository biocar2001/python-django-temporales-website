
from django.contrib.auth.decorators import login_required
from models import *
from forms import *
from django.template import RequestContext, Context, loader
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.conf import settings
from django.http import HttpResponseForbidden


from decimal import *

from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render
from django.contrib import messages
from django.db.models import Q
from django.db import transaction
from datetime import date, datetime, timedelta
from django.core.exceptions import ObjectDoesNotExist


@login_required(login_url="login/")
def home(request):
    return render(request,"home.html")

@login_required
def indexPersonas(request):
    meta=request.META
    ruta=meta['SCRIPT_NAME']
    formFilter= FiltrosPersonasForm()
    if request.method == 'POST':
        form = FiltrosPersonasForm(data=request.POST)

        if form.is_valid():
            empresa = request.POST.get('contact_name', '')
            ingles = request.POST.get('contact_email', '')
            form_content = request.POST.get('content', '')
            # filter
    else:
        personas = Persona.objects.order_by('nombre')
    t = loader.get_template('indexPersonas.html')
    c = RequestContext(request,{'personas':personas,'formFilter':formFilter,})
    return HttpResponse(t.render(c))

@login_required
def filtraPersonas(request):
    meta=request.META
    ruta=meta['SCRIPT_NAME']
    formFilter= FiltrosPersonasForm()
    if request.method == 'POST':
        form = FiltrosPersonasForm(data=request.POST)

        if form.is_valid():
            empresa = request.POST.get('contact_name', '')
            ingles = request.POST.get('contact_email', '')
            form_content = request.POST.get('content', '')
            # filter

    t = loader.get_template('indexPersonas.html')
    c = RequestContext(request,{'personas':personas,'formFilter':formFilter,})
    return HttpResponse(t.render(c))

@login_required
def new_persona(request):
    form = PersonasForm()
    t = loader.get_template('newPersona.html')
    c = RequestContext(request,{'form':form})
    return HttpResponse(t.render(c))