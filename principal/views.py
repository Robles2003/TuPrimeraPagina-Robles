# views.py

# from django.shortcuts import render, redirect
# from django.urls import reverse_lazy
# from django.views.generic import TemplateView, FormView, CreateView, ListView, View
# from django.contrib.auth.mixins import AccessMixin, LoginRequiredMixin
# from django.contrib.auth.decorators import login_required
# from django.contrib import messages

# from .forms import AutorModelForm, LectorModelForm, ArticuloModelForm, LoginForm, BuscarForm
# from .models import Autor, Lector, Articulo


# from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
# from django.urls import reverse_lazy
# from django.contrib.auth.mixins import LoginRequiredMixin
# from .models import Articulo
# from .forms import FormularioArticulo


# # Mixin para verificar si el usuario es un autor logueado.
# # Un Mixin es una clase que nos permite reutilizar código en otras vistas.
# class AutorRequiredMixin(AccessMixin):
#     """Verifica que el usuario actual esté autenticado como autor."""
#     def dispatch(self, request, *args, **kwargs):
#         if not request.session.get('logeado') or request.session.get('tipo') != 'autor':
#             messages.error(request, 'Debes estar logueado como autor para acceder a esta página.')
#             return self.handle_no_permission()
#         return super().dispatch(request, *args, **kwargs)

# # Vista Principal
# class MainView(TemplateView):
#     template_name = 'vista/main.html'

#     def get(self, request, *args, **kwargs):
#         # Si no está logueado, lo redirigimos al login
#         if not request.session.get('logeado', False):
#             return redirect('login')
#         return super().get(request, *args, **kwargs)

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['nombre'] = self.request.session.get('nombre')
#         context['tipo'] = self.request.session.get('tipo')
#         if context['tipo'] == 'autor':
#             context['Autor'] = True
#         elif context['tipo'] == 'lector':
#             context['Lector'] = True
#         return context

# # Vista de Login


# class CrearPublicacionView(AutorRequiredMixin , CreateView):
#     model = Articulo
#     form_class = ArticuloModelForm
#     template_name = 'vista/crear_Publicacion.html'
#     success_url = reverse_lazy('inicio')

#     def form_valid(self, form):
#         # Asignamos el autor logueado al artículo antes de guardarlo.
#         form.instance.autor = Autor.objects.get(id=self.request.session.get('idAutor'))
#         return super().form_valid(form)

# # Vista para listar y buscar artículos (unificamos las dos vistas en una)
# class ArticulosListView(ListView):
#     model = Articulo
#     template_name = 'vista/articulos.html'
#     context_object_name = 'articulos' # Nombre de la variable en el template

#     def get_queryset(self):
#         queryset = super().get_queryset()
        
#         # Filtrar si el usuario es un autor
#         if self.request.session.get('tipo') == 'autor':
#             queryset = queryset.filter(autor__id=self.request.session.get('idAutor'))

#         # Filtrar por búsqueda
#         busqueda = self.request.GET.get('busqueda')
#         if busqueda:
#             queryset = queryset.filter(titulo__icontains=busqueda)
            
#         return queryset

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         # Añadimos el formulario de búsqueda al contexto
#         context['form_buscar'] = BuscarForm(self.request.GET or None)
#         # Añadimos la info del usuario al contexto
#         context['nombre'] = self.request.session.get('nombre')
#         context['tipo'] = self.request.session.get('tipo')
#         if context['tipo'] == 'autor':
#             context['Autor'] = True
#         elif context['tipo'] == 'lector':
#             context['Lector'] = True
#         return context
    
#########################################################################

from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, FormView, CreateView, ListView, DetailView, UpdateView, DeleteView, View
from django.contrib import messages
from django.utils.timezone import now

from .models import Articulo, Autor, Lector, Usuario
from .forms import ArticuloModelForm, LoginForm, BuscarForm, FormularioArticulo, AutorModelForm, LectorModelForm


# Vista principal protegida por sesión
class MainView(TemplateView):
    template_name = 'vista/main.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.session.get('logeado'):
            return redirect('login')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['nombre'] = self.request.session.get('nombre')
        context['tipo'] = self.request.session.get('tipo')
        
        if context['tipo'] == 'autor':
            context['Autor'] = True 
        elif context['tipo'] == 'lector':
            context['Lector'] = True
            
        return context


class LoginView(FormView):
    template_name = 'vista/login.html'
    form_class = LoginForm
    success_url = reverse_lazy('main') # reverse_lazy se usa en CBV para esperar a que las URLs estén listas.

    def form_valid(self, form):
        nombre = form.cleaned_data['nombre']
        password = form.cleaned_data['password']
        tipo = form.cleaned_data['tipo']
        
        user_model = Autor if tipo == 'autor' else Lector
        try:
            user = user_model.objects.get(nombre=nombre, password=password)
            self.request.session['logeado'] = True
            self.request.session['tipo'] = tipo
            self.request.session['nombre'] = user.nombre
            if tipo == 'autor':
                self.request.session['idAutor'] = user.id
            else:
                self.request.session['idLector'] = user.id
            return super().form_valid(form)
        except user_model.DoesNotExist:
            form.add_error(None, f"{tipo.capitalize()} no encontrado o contraseña incorrecta.")
            return self.form_invalid(form)


# Vista de Logout (usamos una View base porque es una acción simple)
class LogoutView(View):
    def get(self, request, *args, **kwargs):
        request.session['logeado'] = False
        request.session.flush() # Limpia toda la sesión para mayor seguridad
        return redirect('main')


# Vista About
class AboutView(TemplateView):
    template_name = 'vista/about.html'


# Vistas de Creación

class CrearAutorView(CreateView):
    model = Autor
    form_class = AutorModelForm
    template_name = 'vista/crear_Autor.html'
    success_url = reverse_lazy('main')
    
    def form_valid(self, form):
        nombre = form.cleaned_data['nombre']
        if Autor.objects.filter(nombre=nombre).exists():
            form.add_error('nombre', 'Ya existe un autor con ese nombre.')
            return self.form_invalid(form)
        return super().form_valid(form)

class CrearLectorView(CreateView):
    model = Lector
    form_class = LectorModelForm
    template_name = 'vista/crear_Lector.html'
    success_url = reverse_lazy('main')
    
    def form_valid(self, form):
        nombre = form.cleaned_data['nombre']
        if Lector.objects.filter(nombre=nombre).exists():
            form.add_error('nombre', 'Ya existe un lector con ese nombre.')
            return self.form_invalid(form)
        return super().form_valid(form)

# Crear artículo (solo para autores logueados)
class CrearPublicacionView(CreateView):
    model = Articulo
    form_class = ArticuloModelForm
    template_name = 'vista/crear-Publicacion.html'
    success_url = reverse_lazy('articulo-list')

    def dispatch(self, request, *args, **kwargs):
        if not request.session.get('logeado') or request.session.get('tipo') != 'autor':
            return redirect('login')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        autor_id = self.request.session.get('idAutor')
        if autor_id:
            form.instance.autor = Autor.objects.get(id=autor_id)
        return super().form_valid(form)

    def form_valid(self, form):
        autor_id = self.request.session.get('idAutor')
        if autor_id:
            form.instance.autor = Autor.objects.get(id=autor_id)
        return super().form_valid(form)

# Listado de artículos con búsqueda opcional
class ArticuloListView(ListView):
    model = Articulo
    template_name = 'vista/articulo_list.html'
    context_object_name = 'articulos'

    def dispatch(self, request, *args, **kwargs):
        if not request.session.get('logeado'):
            return redirect('login')
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('busqueda')
        if query:
            queryset = queryset.filter(titulo__icontains=query)
        return queryset

# Detalle de artículo
class ArticuloDetailView(DetailView):
    model = Articulo
    template_name = 'vista/articulo_detail.html'
    context_object_name = 'articulo'

    def dispatch(self, request, *args, **kwargs):
        if not request.session.get('logeado'):
            return redirect('login')
        return super().dispatch(request, *args, **kwargs)

# Actualizar artículo (requiere ser autor y estar logueado)
class ArticuloUpdateView(UpdateView):
    model = Articulo
    form_class = ArticuloModelForm
    template_name = 'vista/articulo_form.html'
    success_url = reverse_lazy('articulo-list')

    def dispatch(self, request, *args, **kwargs):
        if not request.session.get('logeado') or request.session.get('tipo') != 'autor':
            return redirect('login')
        return super().dispatch(request, *args, **kwargs)

    # def get_form_kwargs(self):
    #     kwargs = super().get_form_kwargs()
    #     autor_id = self.request.session.get('idAutor')
    #     if autor_id:
    #         kwargs['autor'] = Autor.objects.get(id=autor_id)
    #     return kwargs

# Eliminar artículo (requiere ser autor y estar logueado)
class ArticuloDeleteView(DeleteView):
    model = Articulo
    template_name = 'vista/articulo_confirm_delete.html'
    success_url = reverse_lazy('articulo-list')

    def dispatch(self, request, *args, **kwargs):
        if not request.session.get('logeado') or request.session.get('tipo') != 'autor':
            return redirect('login')
        return super().dispatch(request, *args, **kwargs)