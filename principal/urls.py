from django.urls import path
from .views import (
    MainView, AboutView, CrearPublicacionView,
    ArticuloListView, ArticuloDetailView,
    ArticuloUpdateView, ArticuloDeleteView,
    LoginView, LogoutView,
    CrearAutorView, CrearLectorView
)

urlpatterns = [
    path('', MainView.as_view(), name='main'),

    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

    path('crear_autor/', CrearAutorView.as_view(), name='crear_autor'),
    path('crear_lector/', CrearLectorView.as_view(), name='crear_lector'),

    path('crear/', CrearPublicacionView.as_view(), name='crear-publicacion'),

    path('about/', AboutView.as_view(), name='about'),

    #path('articulos/', ArticuloListView.as_view(), name='articulos'),

    path('articulos/', ArticuloListView.as_view(), name='articulo-list'),
    path('articulo/<int:pk>/', ArticuloDetailView.as_view(), name='articulo-detail'),
    path('articulo/<int:pk>/editar/', ArticuloUpdateView.as_view(), name='articulo-edit'),
    path('articulo/<int:pk>/eliminar/', ArticuloDeleteView.as_view(), name='articulo-delete'),
    
    
    path('profile/',),
]
