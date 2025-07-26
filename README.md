🛠️ Funcionalidades Principales
✅ General
Registro e inicio de sesión con selección de tipo de usuario (autor o lector).

Edición de perfil con campos personalizados: nombre, apellido, email, fecha de nacimiento, contraseña, icono.

✍️ Autores
Crear, editar y eliminar artículos.

Subir imágenes a los artículos.

Visualizar lista de publicaciones propias.

👁️ Lectores
Ver lista y detalle de artículos publicados.

Comentar en artículos de autores.

Ver comentarios de otros usuarios.

📦 Requisitos
Python 3.8+

Django 5.2.4

CKEditor (para contenido enriquecido)

📁 Estructura de la App
models.py: Define modelos para Usuario (abstracto), Autor, Lector, Artículo y Comentario.

forms.py: Formularios personalizados para autenticación, registro, perfil y publicación.

views.py: Controladores para login, registro, CRUD de artículos y vista de perfil.

templates/: Vistas organizadas por tipo de usuario y propósito (login.html, articulo_detail.html, etc).

static/assets/: Contiene los iconos seleccionables para el perfil de usuario.

Notas
Los iconos se muestran como opciones gráficas usando inputs tipo radio personalizados.

Los usuarios se almacenan en modelos separados (Autor, Lector), pero comparten campos a través del modelo abstracto Usuario.

Los artículos pueden incluir texto enriquecido gracias a CKEditor.

🧑‍💻 Autor
Desarrollado por Robles en el contexto del curso de CoderHouse.

Video de Explicacion: https://drive.google.com/drive/folders/1NNHwFxe66HwEDyg_ShWDteOv7hZCBLCA?usp=sharing