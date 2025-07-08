from django import forms

#class para procesar formularios
class AutorForm(forms.Form):
    nombre = forms.CharField(max_length=100)
    edad = forms.IntegerField(min_value=1)
    password = forms.CharField(max_length=12, widget=forms.PasswordInput)
    Nacionalidad = forms.CharField(max_length=50)
    
    
class LectorForm(forms.Form):
    nombre = forms.CharField(max_length=100)
    edad = forms.IntegerField(min_value=1)
    password = forms.CharField(max_length=12, widget=forms.PasswordInput)
    direccion = forms.CharField(max_length=50)
    
    
class ArticuloForm(forms.Form):
    titulo = forms.CharField(max_length=100)
    contenido = forms.CharField(widget=forms.Textarea)
    fecha_publicacion = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    ##autor = forms.ModelChoiceField(queryset=Autor.objects.all())  # Asegúrate de importar el modelo Autor
    
    
class LoginForm(forms.Form):
    nombre = forms.CharField(max_length=100, label='Nombre de usuario')
    password = forms.CharField(widget=forms.PasswordInput, label='Contraseña')
    tipo = forms.ChoiceField(
        choices=[('autor', 'Autor'), ('lector', 'Lector')],
        label='Tipo de usuario'
    )
    

    