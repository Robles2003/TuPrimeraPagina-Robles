from django.contrib import admin
from .models import Autor, Lector, Articulo, Comentario
# Register your models here.

registrer_models = [Autor, Lector, Articulo, Comentario]

admin.site.register(registrer_models)
