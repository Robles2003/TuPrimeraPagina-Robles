from django.contrib import admin
from .models import Autor, Lector, Articulo
# Register your models here.

registrer_models = [Autor, Lector, Articulo]

admin.site.register(registrer_models)
