from django.contrib import admin

# Register your models here.
from .models import Persona, Empresa, Oferta
class PersonaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'apellidos','is_active','english_level')
    list_filter = ['nombre','is_active','empresa','english_level']
admin.site.register(Persona,PersonaAdmin)
class EmpresaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion')
    list_filter = ['nombre', 'descripcion']
admin.site.register(Empresa,EmpresaAdmin)

class OfertaAdmin(admin.ModelAdmin):
    list_display = ('puesto', 'hours_week','time_contract','prize_home','prize_healthcare')
    list_filter = ['puesto', 'hours_week','time_contract','prize_home','prize_healthcare']
admin.site.register(Oferta,OfertaAdmin)