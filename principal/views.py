from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from .forms import AutorForm, LectorForm, ArticuloForm, LoginForm
from .models import Autor, Lector, Articulo

# Create your views here.
def main(request):
    if request.session['logeado'] == None or request.session['logeado'] == False:
        request.session['logeado'] = False
        return redirect('login')
    else:
        return render(request, 'vista/main.html', {'nombre': request.session.get('nombre'), 'tipo': request.session.get('tipo')})

def prueba(request):
    request.session['logeado'] = False
    return redirect('inicio')

def login(request):
    if request.method == 'POST' and request.session.get('logeado') == False:
        form = LoginForm(request.POST)
        if form.is_valid():
            nombre = form.cleaned_data['nombre']
            password = form.cleaned_data['password']
            tipo = form.cleaned_data['tipo']
                
            if tipo == 'autor':
                try: 
                    autor = Autor.objects.get(nombre=nombre, password=password)
                    request.session.get('idAutor', autor.id)
                    request.session['logeado'] = True
                    request.session['tipo'] = 'autor'
                    request.session['nombre'] = autor.nombre 
                    return redirect('inicio')
                except Autor.DoesNotExist:
                    return render(request, 'vista/login.html', {'form': form, 'error': 'Autor no encontrado'})
            elif tipo == 'lector':
                try:
                    lector = Lector.objects.get(nombre=nombre, password=password)
                    request.session['idLector'] = lector.id
                    request.session['logeado'] = True
                    request.session['tipo'] = 'lector'
                    request.session['nombre'] = lector.nombre  
                    return redirect('inicio')
                except Lector.DoesNotExist:
                    return render(request, 'vista/login.html', {'form': form, 'error': 'Lector no encontrado'})
    else:
        form = LoginForm()
        return render(request, 'vista/login.html', {'form': form})
        
    
    return render(request, 'vista/login.html')

def crear_autor(request):
    if request.method == 'POST':
        form = AutorForm(request.POST)
        if form.is_valid():
            autor = Autor(
                nombre = form.cleaned_data['nombre'],
                edad = form.cleaned_data['edad'],
                password = form.cleaned_data['password'],
                Nacionalidad = form.cleaned_data['Nacionalidad']
            )
            autor.save()
            return redirect('inicio')     
    else:
        form = AutorForm()
        return render(request, 'vista/crear_Autor.html', {'form' : form})
          
            

def crear_lector(request):
    if request.method == 'POST':
        form = LectorForm(request.POST)
        if form.is_valid():
            lector = Lector(
                nombre = form.cleaned_data['nombre'],
                edad = form.cleaned_data['edad'],
                password = form.cleaned_data['password'],
                direccion = form.cleaned_data['direccion']
            )
            lector.save()
            return redirect('inicio')
        
    else: 
        form = LectorForm()
        return render(request, 'vista/crear_Lector.html', {'form': form})
            

def crear_publicacion(request):
    
    if request.session.get('logeado') != False and request.session.get('tipo') == 'autor':
        if request.method == 'POST':
            form = ArticuloForm(request.POST)
            if form.is_valid(): 
                articulo = Articulo(
                    titulo = form.cleaned_data['titulo'],
                    contenido = form.cleaned_data['contenido'],
                    fecha_publicacion = form.cleaned_data['fecha_publicacion'],
                    autor = Autor.objects.get(id=request.session.get('idAutor')) ##busca el autor por su id usando
                )
                
                articulo.save()
                return redirect('inicio')
            else:
                return render(request, 'vista/crear_Publicacion.html', {'form': form, 'error': 'Formulario inválido'})
        else:
            form = ArticuloForm()
            return render(request, 'vista/crear_Publicacion.html', {'form': form})

    else:
        messages.error(request, 'debes estar logueado como autor para crear una publicación')
        return redirect('login')  # Redirige al login si no está logueado o no es autor
