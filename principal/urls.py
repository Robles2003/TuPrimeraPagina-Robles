
from django.urls import path
from .views import main, prueba, crear_autor, crear_lector, crear_publicacion, login, Articulos

urlpatterns = [
    path('', main, name='inicio'),# Ruta para la vista principal
    path('prueba/', prueba, name='prueba'),
    path('crear_lector/', crear_lector, name='crear_lector'),
    path('crear_publicacion', crear_publicacion, name='crear_publicacion'),
    path('crear_autor/', crear_autor, name='crear_autor'),
    path('login/', login, name='login'),
    path('articulos/', Articulos, name='articulos'),
    
]