# API Docs

## How to run

Para correr la aplicacion hace falta poseer docker instalado en el equipo, ademas se debe crear una copia de `.env.sample` y renombrarla como `.env` para que docker sea capaz de cargar las configuraciones.

Una vez realizado esto, para correr el proyeco, se debe usar:

```bash
docker compose up -d --build
 ```

Esto levantara la base de datos, la api y el gestor web de mongo (Este ultimo se debe retirar en entornos de produccion o retirarle el acceso a la web)
 
El tag `--build` fuerza a que con cada inicio del deploy se re cree la imagen de la api. No seria necesario en un simple reinicio.

Para parar la infraestructura se debe usar:

```bash
docker compose down
```

En caso de querer correr en modo desarollo, se debe iniciar el deploy y luego utilizar:

```bash
docker compose down api
```

El cual dara de baja el contenedor de la api y la api debera ser iniciada con el comando:

```bash
# Usando poetry
poetry run uvicorn app.main:app --reload

# o si la terminal ya se encuentra en el entorno virtual
uvicorn app.main:app --reload
```

## Estructura

Para mejor organizacion del proyecto, este se organizara internamente por carpetas:

* `api`: contendra toda la logica corespondiente a las rutas de las API's y que deben hacer estas. 
* `core`: contendra utilidades generales al protecto, como configuraciones globales y utilidades de todo tipo.
* `crud`: Contendra las funciones CRUD (Create, Read, Update, Delete).
* `db`: Contiene utilidades referidas a la conexion con la base de datos.
* `models`: Contiene las clases de datos, ya sean las guardades dentro de la base de datos como las clases que se utilizan en las respuestas o peticiones a la API.

## API_V1

Dentro de esta carpeta se colocaran todos los enpoints correspondientes al desarollo. 

Actualmente, el unico endpoint creado y no completo es auth.

### Auth endpoints

- `/api/users/login`: Endpoint **post** donde se envia email y contraseña para iniciar sesion.
- `/api/users/add`: Endpoint **post** donde se envian los datos de un nuevo usuario para registrarlo en la base de datos, se requiere *email*, *username*, *password*.

## Core

Dentro de esta carpeta se encuentran utilidades generales:

* `config`: Manejo de variables de entorno y variables constantes para todo el proyecto.
* `errors`: Funciones callback para el manejo de errores de FastAPI.
* `jwt`: Manejo de Json Web Token. Creacion, verificacion, etc.
* `security`: Manejo del algoritmo de hash de las contraseñas, por motivos de seguridad, la contraseñas se guardan en bcrypt, el cual es un algorimo de hasheado muy dificil de romper, la contraseña viajara en texto plano hasta la api para ser verificada contra la version hasheada y guardada en la base de datos.

## Crud

Esta carpeta contiene las funciones correspondientes a las operaciones CRUD de cada uno de los modelos de datos que manejara la api, cada uno de estos debe corresponder a uno o varios endpoints.

* `user`: Contiene las funciones de creado, borrado, lectura y actualizacion de usuarios en la base de datos.

## db

Esta carpeta contiene la logica de conexión con la base de datos.

* `mongodb`: Contiene la clase que almacena la conexion con la base de datos.
* `mongodb_utils`: Contiene las funciones de conexion y desconexion. Ojo con el string de conexion que se usa dentro de este archivo en la funcion `connect_to_mongo` en mi caso tuve problemas al tratarse del usuario administrador de mongo, lo cual no es una buena practica, para eso debi agregar al final del string que se encuentra en `core/config/MONGODB_URL` lo siguiente: `?authSource=admin`. para poder establecer la conexion correctamente con la base de datos.

## Models

Esta carpeta contiene las clases de datos a utilizar por los endpoints y las funciones CRUD. Puede contener las clases de los objetos que se guardan en base de datos, como las clases que son utilizadas en las respuestas de los endpoints o como entrada de estos.

* `dbmodel`: Contiene las clases padre de las cuales las diferentes clases que requieran uso de la base de datos tienen que heredar.
* `rwmodel`: Contiene la clase padre cruda, de la cual tienen que heredar las clases que son utilizadas como respuesta o entrada de los endpoints.
* `token`: Contiene la clase cruda de jwt.
* `user`: Contiene todas las clases referidas al usuario, desde la que se guarda en base de datos hasta las diferentes clases utilizadas por los enpoints.

## main.py

Se trata del core de la aplicacion, donde se inicializa el logging de informacion y errores, ademas de los midelware de la aplicacion y el router de la API.

