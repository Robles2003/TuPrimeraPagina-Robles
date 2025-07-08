from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import AutorForm, LectorForm, ArticuloForm
from .models import Autor, Lector, Articulo

# Create your views here.
def main(request):
    request.session['idAutor'] = 5
    return render(request, 'vista/main.html') # Renderiza la plantilla index.html en la carpeta principal
                                            #toma automaticamente el archivo de la carpeta templates

def prueba(request):
    return HttpResponse("<h1>Hola, esta es una prueba</h1>") # Respuesta simple de prueba

def login(request):
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
    
    if request.session.get('idAutor') != None:
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
        return HttpResponse("Debes de iniciar session")##luego hacer que redirija a la vista de inicio de sesión
