# challenge-chaindots

Este es un proyecto basado en **Python**, **Django**, **Django REST Framework**, **PostgreSQL** y **Docker**.
Permite a los usuarios crear publicaciones, seguir a otros usuarios y comentar en publicaciones.

## Requisitos

. Python 3.9
. PostgreSQL
. Poetry
. Docker

## Instalación

### 1. Clonar el repositorio
```git clone [url_del_repositorio]```
```cd Chaindots```

### 2. Instalar dependencias

Utilizá Poetry para gestionar las dependencias del proyecto. Si no tenés Poetry instalado, seguí las instrucciones en su documentación oficial.

.Chequeá tener **Python 3.9** instalado. Luego, ejecutá los siguientes comandos:

```poetry env use $(which python3)```
```poetry install```

Si es necesario, ejecutá:
```poetry install --no-root```
```poetry lock --no-update```

Ejecutá:
```poetry shell```

### 3. Configurar la base de datos y .env

- Chequeá de tener PostgreSQL instalado y configurado. Creá un .env con las variables y valores correspondientes para las siguientes variables (DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT) en el archivo settings.py:

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT'),
    }
}
#### Configuración de la variable `SECRET_KEY`

-Generar una `SECRET_KEY`:

``` python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())' ```

-Esto generará una clave secreta aleatoria que podés usar. Luego acordate deagregarla a tu archivo .env:

```SECRET_KEY=tu_clave_secreta```


### 4. Construir, ejecutar el contenedor y aplicar migraciones

```docker-compose up --build```

```docker-compose exec <Container_ID> python manage.py migrate```

### 5. Crear un superusuario

```docker-compose exec <Container_ID> python manage.py createsuperuser```

### 6. Iniciar el servidor

El servidor de Django se ejecutará automáticamente en el contenedor. Accedé a la aplicación en el navegador en http://localhost:8000.

## Uso de la API

- La API de Chaindots expone los siguientes endpoints:

### Usuarios

- ```GET /api/users/```: Recuperar una lista de todos los usuarios.
- ```GET /api/users/{id}/```: Recuperar detalles de un usuario específico.
- ```POST /api/users/```: Crear un nuevo usuario.
- ```POST /api/users/{id}/follow/{id}```: Seguir a otro usuario.

### Publicaciones

- ```GET /api/posts/```: Recuperar una lista de todas las publicaciones con filtros y paginación.
- ```GET /api/posts/{id}/```: Recuperar detalles de una publicación específica con los últimos tres comentarios.
- ```POST /api/posts/```: Crear una nueva publicación.

### Comentarios

- ```GET /api/posts/{id}/comments/```: Recuperar todos los comentarios para una publicación específica.
- ```POST /api/posts/{id}/comments/```: Agregar un nuevo comentario a una publicación.


- Gracias por la oportunidad :)