# urls.py

from django.urls import path
from .views import (
    MainView,
    LogoutView,
    CrearAutorView,
    CrearLectorView,
    CrearPublicacionView,
    LoginView,
    ArticulosListView
)

urlpatterns = [
    path('', MainView.as_view(), name='inicio'),
    path('logout/', LogoutView.as_view(), name='logout'), # La vista 'prueba' ahora es 'logout'
    path('crear_lector/', CrearLectorView.as_view(), name='crear_lector'),
    path('crear_publicacion/', CrearPublicacionView.as_view(), name='crear_publicacion'),
    path('crear_autor/', CrearAutorView.as_view(), name='crear_autor'),
    path('login/', LoginView.as_view(), name='login'),
    path('articulos/', ArticulosListView.as_view(), name='articulos'),
    # La URL 'buscar_articulos' ya no es necesaria, su lógica está en ArticulosListView
]