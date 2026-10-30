from django.contrib import admin
from .models import Gra


@admin.register(Gra)
class GraAdmin(admin.ModelAdmin):
    list_display = ('tytul', 'gatunek', 'data_premiery', 'ocena', 'wieloosobowa', 'cena')
    list_filter = ('gatunek', 'wieloosobowa')
    search_fields = ('tytul',)
