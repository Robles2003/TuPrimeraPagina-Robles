TuPrimeraPagina+Robles

1- El proyecto consiste en en 4 clases Autor, Lector (ambas hederan de usuario) y articulo
   Los lectores pueden Leer y Buscar Articulos
   Los Autores peuden crear y ver sus propios articulos
   Usuario es una supraclase abstracta que tiene los datos comunes de Autor y Lector

2- Uso del sistema y cumplimineto de los requerimientos 
    2.1: Por lo menos 3 clases en model / Un formulario para insertar datos a por cada model creado..
        Al iniciar el sistema deberia ser redireccionado del main al login por no tener una cuenta activa, ahi vera dos links debajo del boton de login, cada uno lo redirigira a un formulario para dar de alta un cliente o autor

        Para crear un articulo debera logearse como un autor y entrar a la tarjeta de crear articulo ademas de completar el fromulario

    2.2: Un formulario para buscar algo en la BD
        para este requisito debera estar logeado como Lector, despues entrar en la tarjeta de Buscar Articulo y poner alguna parte del titulo (o no) del articulo a buscar

3- Ubicacion de las funcionalidades
   Todo el proyecto se encuentra el la carpeta pricipal, en el archivo models.py estara la estructura la base de datos incluyendo Autor, Lector, Usuario y Articulo
   
   En el archivo forms se encutran las estructuras de los formularios usados en la entrega

   En el archivo views.py se encontraran las 3 altas de las clases crear_autor, crear_lector, crear_publicacion ademas de la funcion buscar sobre la clase articulo buscar_articulos