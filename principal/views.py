from django.shortcuts import render 
from django.http import HttpResponse

# Create your views here.
def main(request):
    #return HttpResponse("Hola")
    return render(request, 'vista/main.html') # Renderiza la plantilla index.html en la carpeta principal
                                            #toma automaticamente el archivo de la carpeta templates

def prueba(request):
    return HttpResponse("<h1>Hola, esta es una prueba</h1>") # Respuesta simple de prueba