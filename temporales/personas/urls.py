from django.conf.urls import url
from . import views
from . import ajax

# We are adding a URL called /home
urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^personas/$', views.indexPersonas, name='personas'),
    url(r'^aplicaFiltroPers/$', ajax.aplicaFiltroPers, name='filtraPersonas'),
    url(r'^newPersona/$', views.new_persona, name='newPersona'),
    url(r'^detailPersona/(?P<idpersona>\d+)/$', views.detailPersona, name='detailPersona'),
    #url(r'^savePersona/$', views.savePersona, name='savePersona'),
]