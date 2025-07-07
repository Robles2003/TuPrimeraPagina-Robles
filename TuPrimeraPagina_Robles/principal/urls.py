
from django.urls import path
from .views import main, prueba

urlpatterns = [
    path('', main, name='incio'),# Ruta para la vista principal
    path('prueba/', prueba, name='prueba'), 
    
]