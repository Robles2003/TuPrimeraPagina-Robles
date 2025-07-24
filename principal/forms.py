# forms.py

from django import forms
from .models import Autor, Lector, Articulo

# Usamos ModelForm para vincular directamente el formulario al modelo.
# Esto simplifica la validación y el guardado.

class AutorModelForm(forms.ModelForm):
    password = forms.CharField(max_length=12, widget=forms.PasswordInput)
    
    class Meta:
        model = Autor
        fields = ['nombre', 'edad', 'password', 'Nacionalidad']

class LectorModelForm(forms.ModelForm):
    password = forms.CharField(max_length=12, widget=forms.PasswordInput)
    
    class Meta:
        model = Lector
        fields = ['nombre', 'edad', 'password', 'direccion']

class ArticuloModelForm(forms.ModelForm):
    fecha_publicacion = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    
    class Meta:
        model = Articulo
        # El autor se asignará automáticamente en la vista, no es necesario en el form.
        fields = ['titulo', 'contenido', 'fecha_publicacion']

# Estos formularios no están ligados a un modelo, así que se quedan como forms.Form
class LoginForm(forms.Form):
    nombre = forms.CharField(max_length=100, label='Nombre de usuario')
    password = forms.CharField(widget=forms.PasswordInput, label='Contraseña')
    tipo = forms.ChoiceField(
        choices=[('autor', 'Autor'), ('lector', 'Lector')],
        label='Tipo de usuario'
    )

class BuscarForm(forms.Form):
    busqueda = forms.CharField(max_length=100, label='Buscar Artículo', required=False)
    
class ArticuloForm(forms.Form):
    titulo = forms.CharField(max_length=100)
    contenido = forms.CharField(widget=forms.Textarea)
    fecha_publicacion = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))