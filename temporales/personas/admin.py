from django.contrib import admin

# Register your models here.
from .models import Persona, Empresa, Salario, Oferta
class PersonaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'apellidos','is_active','empresa','english_level')
    list_filter = ['nombre','is_active','empresa','english_level']
admin.site.register(Persona,PersonaAdmin)
class EmpresaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'ett','localizacion')
    list_filter = ['nombre', 'ett','localizacion']
admin.site.register(Empresa,EmpresaAdmin)
class SalarioAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'edad','amount')
    list_filter = ['nombre', 'edad','amount']
admin.site.register(Salario,SalarioAdmin)
class OfertaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'hours_week','time_contract','payment_home','payment_healthcare')
    list_filter = ['nombre', 'hours_week','time_contract','payment_home','payment_healthcare']
admin.site.register(Oferta,OfertaAdmin)