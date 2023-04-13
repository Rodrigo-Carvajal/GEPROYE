GEPROYE <br>
Sistema que tiene como objetivo gestionar proyectos y sus iteraciones, actividades a realizar, requisitos e integrantes.

[![Aplicación alojada en:](https://railway.app/button.svg)]

# Requisitos

- Python 3.10
- extensión de virtualenv

Si no cuenta con esta extensión se puede agregar con el siguiente comando: `pip install virtualenv`

# 💁‍♀️ Como usar el código

# Clonar el repositorio
  `git clone "https://github.com/Rodrigo-Carvajal/Geproye.git"`

# Configurar el enterno virutal
  ### Crear el entorno
  `python -m venv env`
  ### Acceder al directorio
  `.\env\Scripts\activate`
  ### Instalar dependencias
  `pip install -r requirements.txt`
  
# Arrancar la aplicación en modo desarrollo:
  ## Al momento de arrancar la aplicación puede realizarse de dos maneras:
  ### A través del comando python
    - Una vez que se encuentre activo el entorno virtual y con las
      dependencias correctamente instaladas, ejecutamos la aplicación a través de:
      `python directorio/main.py`
  ### A través del comando flask run
    - Para ejecutar con este comando primero se deben definir las siguientes variables por consola
      -`set FLASK_APP=main` en windows
      -`export FLASK_APP=main` en linux

# Despliegue de la aplicación en producción:
  Con respecto al despliegue de la aplicación, esta fue gestionada a través de <strong>Railway</strong>, con una base de datos alojada en <strong>Supabase</strong>.
