# Backend con Python + Flask

Este proyecto es un backend en Python con Flask, diseñado bajo una arquitectura modular (no monolítica) para mantener la escalabilidad y organización del código.

El sistema gestiona usuarios y documentos, con autenticación mediante JWT tokens y control de permisos basado en roles (Admin y User).

# Tecnologías utilizadas

- Python 3
- Flask
- MySQL
- JWT (Json Web Tokens)
- Bcrypt → hash de contraseñas y datos sensibles
- Multer (para gestión de archivos locales)
- Postman (colección para pruebas)

# Estructura del proyecto

El proyecto sigue una estructura modular, organizada en carpetas:

```bash
├── config/ # Configuraciones generales (BD, JWT, etc.)
├── db/ # Conexión y modelos de base de datos
├── files/ # Carpeta donde se almacenan documentos
├── routes/ # Definición de endpoints (usuarios, documentos, auth)
├── services/ # Lógica de negocio y validaciones
├── tests/ # Pruebas unitarias e integración
├── .env # Variables de entorno
└── app.py # Punto de entrada de la aplicación
```

# Gestión de Usuarios

## Endpoints principales:

- POST /auth/login → Login de usuario
- POST /users → Crear un nuevo usuario
- GET /users → Listar todos los usuarios (solo Admin)
- GET /users/<id> → Obtener usuario por ID
- PUT /users/<id>/password → Cambiar contraseña
- DELETE /users/<id> → Borrar usuario (en desarrollo)

🔒 La autenticación se realiza mediante JWT.

# Gestión de Documentos

Actualmente los documentos se guardan en local, utilizando multer.

## Endpoints principales:

- POST /documents → Subir un documento
- GET /documents → Listar documentos
- DELETE /documents/<id> → Eliminar documento

```bash
Admin → todos los documentos
User → solo sus documentos
```

## Seguridad y Roles

Bcrypt para el hash de contraseñas antes de guardarlas en MySQL.
JWT tokens para autenticación de usuarios.

Validaciones de permisos según rol:

```bash
Admin → acceso a todos los usuarios y documentos.
User → acceso limitado solo a sus recursos.
```

## Configuración e instalación

1. Clonar el repositorio

```bash
git clone https://github.com/tuusuario/tu-repo.git
cd tu-repo
```

2. Crear entorno virtual

```bash
python -m venv venv
source venv/bin/activate # Linux/Mac
venv\Scripts\activate # Windows
```

3. Instalar dependencias

```bash
pip install -r requirements.txt
```

4. Configurar variables de entorno en .env

```bash
FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY=tu_clave_secreta
DATABASE_URL=mysql://usuario:password@localhost/nombre_db
```

5. Ejecutar la aplicación

```bash
flask run
```

## Pruebas

Se incluye una colección de Postman para probar los endpoints:

- Autenticación (login y registro)
- CRUD de usuarios
- CRUD de documentos

## Próximos pasos

- Finalizar funcionalidad de eliminación de usuario.
- Migrar almacenamiento de documentos de local a cloud (S3, GCP, etc.).
- Implementar tests automáticos más robustos.
