from django.db import models


# Create your models here.
class Usuario(models.Model): 
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    edad = models.IntegerField()
    password = models.CharField(max_length=12)
    ICONO_CHOICES = [
        ('assets/icono1.png', 'Icono 1'),
        ('assets/icono2.png', 'Icono 2'),
        ('assets/icono3.png', 'Icono 3'),
    ]
    icono = models.CharField(max_length=100, choices=ICONO_CHOICES, default='assets/icono1.png')
    
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
    contenido = models.TextField()
    fecha_publicacion = models.DateField()
    imagen = models.ImageField(upload_to='imagenes_articulos/', null=True, blank=True)  # ⬅️ Agregado
    autor = models.ForeignKey(Autor, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"Titulo: {self.titulo}, Contenido: {self.contenido}, Fecha de Publicacion: {self.fecha_publicacion}, Autor: {self.autor.nombre} id: {self.autor.id}"


class Comentario(models.Model):
    lector = models.ForeignKey('Lector', on_delete=models.CASCADE)
    articulo = models.ForeignKey('Articulo', on_delete=models.CASCADE, related_name='comentarios')
    contenido = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.lector.nombre} - {self.articulo.titulo}"

