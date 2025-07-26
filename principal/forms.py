# forms.py

from django import forms
from .models import Autor, Lector, Articulo, Comentario
from django import forms
from .models import Articulo
from ckeditor.widgets import CKEditorWidget

ICONOS_CHOICES = [
    ("assets/icono1.png", "Icono 1"),
    ("assets/icono2.png", "Icono 2"),
    ("assets/icono3.png", "Icono 3"),
]

class IconoRadioSelect(forms.RadioSelect):
    option_template_name = 'widgets/icono_radio.html' 

class PerfilForm(forms.Form):
    nombre = forms.CharField(label='Nuevo nombre', max_length=100, required=False)
    password = forms.CharField(label='Nueva contraseña', widget=forms.PasswordInput, required=False)
    icono = forms.ChoiceField(choices=ICONOS_CHOICES, required=False)

class AutorModelForm(forms.ModelForm):
    password = forms.CharField(max_length=12, widget=forms.PasswordInput)
    
    class Meta:
        model = Autor
        fields = ['nombre', 'edad', 'password', 'Nacionalidad', 'icono']  
        widgets = {
            'icono': IconoRadioSelect
        }
        
class LectorModelForm(forms.ModelForm):
    password = forms.CharField(max_length=12, widget=forms.PasswordInput)
    
    class Meta:
        model = Lector
        fields = ['nombre', 'edad', 'password', 'direccion', 'icono'] 
        widgets = {
            'icono': IconoRadioSelect
        }
class ArticuloModelForm(forms.ModelForm):
    fecha_publicacion = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    
    class Meta:
        model = Articulo
        fields = ['titulo', 'contenido', 'fecha_publicacion']

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


class FormularioArticulo(forms.ModelForm):
    contenido = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = Articulo
        fields = ['titulo', 'contenido', 'imagen', 'fecha_publicacion']
        
class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ['contenido']
        widgets = {
            'contenido': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Escribe un comentario...'}),
        }

