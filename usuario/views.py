from django.views import View
from django.shortcuts import render

class PruebaUSUARIOView(View):
    def get(self, request):
        return render(request, 'usuario/prueba_usuario.html')
