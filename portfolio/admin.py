from django.contrib import admin
from .models import *

@admin.register(TFC)
class TFCAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'curso', 'ano', 'destaque')
    search_fields = ('titulo', 'autores')
    list_filter = ('curso', 'ano', 'destaque')

admin.site.register(Licenciatura)
admin.site.register(Tecnologia)
admin.site.register(UnidadeCurricular)
admin.site.register(Projeto)
admin.site.register(Competencia)
admin.site.register(Formacao)
admin.site.register(MakingOf)