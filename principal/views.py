# views.py

from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import TemplateView, FormView, CreateView, ListView, DetailView, UpdateView, DeleteView, View
from django.contrib import messages
from django.utils.timezone import now

from .models import Articulo, Autor, Lector, Usuario
from .forms import ArticuloModelForm, LoginForm, BuscarForm, FormularioArticulo, AutorModelForm, LectorModelForm, PerfilForm, ComentarioForm



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
    success_url = reverse_lazy('main') 

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
            self.request.session['icono'] = user.icono 
            
            
            if tipo == 'autor':
                self.request.session['idAutor'] = user.id
            else:
                self.request.session['idLector'] = user.id
            return super().form_valid(form)
        except user_model.DoesNotExist:
            form.add_error(None, f"{tipo.capitalize()} no encontrado o contraseña incorrecta.")
            return self.form_invalid(form)


class LogoutView(View):
    def get(self, request, *args, **kwargs):
        request.session['logeado'] = False
        request.session.flush() 
        return redirect('main')



class AboutView(TemplateView):
    template_name = 'vista/about.html'



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


class ArticuloDetailView(DetailView):
    model = Articulo
    template_name = 'vista/articulo_detail.html'
    context_object_name = 'articulo'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.session.get('tipo') == 'lector':
            context['comentario_form'] = ComentarioForm()
        context['comentarios'] = self.object.comentarios.order_by('-fecha')
        return context

    def post(self, request, *args, **kwargs):
        if request.session.get('tipo') != 'lector':
            return redirect('login')

        self.object = self.get_object()
        form = ComentarioForm(request.POST)
        if form.is_valid():
            comentario = form.save(commit=False)
            comentario.articulo = self.object
            comentario.lector = Lector.objects.get(id=request.session.get('idLector'))
            comentario.save()
            return redirect('articulo-detail', pk=self.object.pk)

        context = self.get_context_data(object=self.object)
        context['comentario_form'] = form
        return self.render_to_response(context)




class ArticuloUpdateView(UpdateView):
    model = Articulo
    form_class = ArticuloModelForm
    template_name = 'vista/articulo_form.html'
    success_url = reverse_lazy('articulo-list')

    def dispatch(self, request, *args, **kwargs):
        if not request.session.get('logeado') or request.session.get('tipo') != 'autor':
            return redirect('login')
        return super().dispatch(request, *args, **kwargs)

class ArticuloDeleteView(DeleteView):
    model = Articulo
    template_name = 'vista/articulo_confirm_delete.html'
    success_url = reverse_lazy('articulo-list')

    def dispatch(self, request, *args, **kwargs):
        if not request.session.get('logeado') or request.session.get('tipo') != 'autor':
            return redirect('login')
        return super().dispatch(request, *args, **kwargs)
    
    
def profile_view(request):
    usuario_tipo = request.session.get('tipo')  # 'autor' o 'lector'

    if usuario_tipo == 'autor':
        usuario_id = request.session.get('idAutor')
    else:
        usuario_id = request.session.get('idLector')

    if not usuario_id or not usuario_tipo:
        return redirect('main')

    Modelo = Autor if usuario_tipo == 'autor' else Lector
    usuario = Modelo.objects.get(id=usuario_id)

    if request.method == 'POST':
        form = PerfilForm(request.POST)
        if form.is_valid():
            nombre = form.cleaned_data['nombre']
            password = form.cleaned_data['password']
            icono = form.cleaned_data['icono']

            if nombre:
                usuario.nombre = nombre
                request.session['nombre'] = nombre  # Actualiza la sesión
            if password:
                usuario.password = password
            if icono:
                usuario.icono = icono
                request.session['icono'] = icono  # Actualiza la sesión

            usuario.save()
            return redirect('main')
    else:
        form = PerfilForm(initial={
            'nombre': usuario.nombre,
            'icono': usuario.icono,
        })

    return render(request, 'vista/profile.html', {
        'form': form,
        'icono_actual': usuario.icono
    })
