from django.db import models

# Create your models here.
class Usuario(models.Model): 
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    edad = models.IntegerField()
    password = models.CharField(max_length=12)
    
    class Meta:
        abstract = True
        
class Lector(Usuario):
    direccion = models.CharField(max_length= 50)
    
    def __str__(self):
        return f"id:{self.id}  nombre: {self.nombre}, Edad: {self.edad}, direccion: ({self.direccion})"
    
    
class Autor(Usuario): 
    Nacionalidad = models.CharField(max_length=50)
    
    def __str__(self):
        return f"id:{self.id} nombre: {self.nombre}, Edad: {self.edad}, Nacionalidad: {self.Nacionalidad}"
    
class Articulo(models.Model):
    titulo = models.CharField(max_length=100)
    contenido= models.TextField()
    fecha_publicacion = models.DateField()
    autor = models.ForeignKey(Autor, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"Titulo: {self.titulo}, Contenido: {self.contenido}, Fecha de Publicacion: {self.fecha_publicacion}, Autor: {self.autor.nombre}"