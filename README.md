# Music App Frontend

Una aplicación web completa para gestionar usuarios, canciones y favoritos musicales, construida con Flask y Bootstrap. Esta aplicación actúa como frontend para una API REST de música.

## 📋 Tabla de Contenidos

- [Características](#características)
- [Tecnologías](#tecnologías)
- [Requisitos](#requisitos)
- [Instalación](#instalación)
- [Configuración](#configuración)
- [Uso](#uso)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [API Endpoints](#api-endpoints)
- [Funcionalidades](#funcionalidades)
- [Troubleshooting](#troubleshooting)
- [Contribución](#contribución)
- [Licencia](#licencia)

## ✨ Características

- **Gestión de Usuarios**: Crear, editar, eliminar y listar usuarios
- **Biblioteca Musical**: Administrar canciones con información completa (título, artista, álbum, duración, año, género)
- **Sistema de Favoritos**: Marcar canciones como favoritas por usuario
- **Autenticación**: Sistema de login basado en JWT
- **Búsqueda**: Buscar canciones por título o artista
- **Interfaz Responsive**: Diseño adaptable para móviles y escritorio
- **Dashboard Interactivo**: Panel principal con acceso rápido a todas las funciones
- **Modo Debug**: Herramientas de debugging integradas

## 🛠 Tecnologías

### Backend
- **Flask 2.3.3** - Framework web de Python
- **Python 3.8+** - Lenguaje de programación
- **Requests** - Cliente HTTP para comunicación con la API
- **python-dotenv** - Gestión de variables de entorno

### Frontend
- **Bootstrap 5.1.3** - Framework CSS
- **Font Awesome 6.0** - Iconos
- **JavaScript ES6+** - Funcionalidad del lado del cliente
- **Jinja2** - Motor de plantillas

### Herramientas
- **Git** - Control de versiones
- **Virtual Environment** - Aislamiento de dependencias

## 📋 Requisitos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)
- API REST de música ejecutándose (por defecto en puerto 5000)
- Navegador web moderno

## 🚀 Instalación

### 1. Clonar el repositorio

\`\`\`bash
git clone <url-del-repositorio>
cd music-frontend-app
\`\`\`

### 2. Crear entorno virtual

\`\`\`bash
# Windows
python -m venv venv
venv\\Scripts\\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
\`\`\`

### 3. Instalar dependencias

\`\`\`bash
pip install -r requirements.txt
\`\`\`

### 4. Configurar variables de entorno

Crea un archivo \`.env\` en la raíz del proyecto:

\`\`\`env
# API Configuration
API_BASE_URL=http://localhost:5000
SECRET_KEY=tu-clave-secreta-aqui

# Flask Configuration
FLASK_ENV=development
FLASK_DEBUG=True
\`\`\`

## ⚙️ Configuración

### Variables de Entorno

| Variable | Descripción | Valor por Defecto |
|----------|-------------|-------------------|
| \`API_BASE_URL\` | URL base de la API REST | \`http://localhost:5000\` |
| \`SECRET_KEY\` | Clave secreta para sesiones | \`your-secret-key-here\` |
| \`FLASK_ENV\` | Entorno de Flask | \`development\` |
| \`FLASK_DEBUG\` | Modo debug de Flask | \`True\` |

### Configuración de la API

La aplicación espera que la API REST tenga los siguientes endpoints:

- \`GET /api/usuarios\` - Listar usuarios
- \`POST /api/usuarios\` - Crear usuario
- \`GET/PUT/DELETE /api/usuarios/{id}\` - Operaciones con usuario específico
- \`GET /api/canciones\` - Listar canciones
- \`POST /api/canciones\` - Crear canción
- \`GET/PUT/DELETE /api/canciones/{id}\` - Operaciones con canción específica
- \`GET /api/favoritos\` - Listar favoritos
- \`POST /api/favoritos\` - Crear favorito
- \`DELETE /api/favoritos/{id}\` - Eliminar favorito
- \`POST /api/login\` - Autenticación

## 🎯 Uso

### Iniciar la aplicación

#### Opción 1: Solo Frontend
\`\`\`bash
python src/main.py
\`\`\`

#### Opción 2: Frontend + API simultáneamente
\`\`\`bash
# Usando el script de Python
python run_all.py

# Usando el script de shell (Linux/Mac)
chmod +x run_all.sh
./run_all.sh
\`\`\`

### Acceder a la aplicación

1. Abre tu navegador web
2. Ve a \`http://localhost:5001\`
3. Serás redirigido a la página de login

### Primer uso

1. **Registrar usuario**: Si no tienes cuenta, haz clic en "Regístrate aquí"
2. **Iniciar sesión**: Usa tu nombre y correo electrónico
3. **Explorar**: Una vez logueado, tendrás acceso al dashboard principal

## 📁 Estructura del Proyecto

\`\`\`
music-frontend-app/
│
├── src/                          # Código fuente principal
│   ├── components/               # Componentes de lógica de negocio
│   │   ├── user_component.py     # Gestión de usuarios
│   │   ├── song_component.py     # Gestión de canciones
│   │   └── favorite_component.py # Gestión de favoritos
│   │
│   ├── templates/                # Plantillas HTML
│   │   ├── base.html            # Plantilla base
│   │   ├── login.html           # Página de login
│   │   ├── register.html        # Página de registro
│   │   ├── dashboard.html       # Dashboard principal
│   │   ├── users.html           # Lista de usuarios
│   │   ├── user_form.html       # Formulario de usuario
│   │   ├── songs.html           # Lista de canciones
│   │   ├── song_form.html       # Formulario de canción
│   │   ├── favorites.html       # Lista de favoritos
│   │   └── api_status.html      # Estado de la API
│   │
│   ├── utils/                   # Utilidades
│   │   └── api_client.py        # Cliente para comunicación con API
│   │
│   └── main.py                  # Aplicación principal Flask
│
├── run_all.py                   # Script para ejecutar API + Frontend
├── run_all.sh                   # Script shell para Linux/Mac
├── requirements.txt             # Dependencias de Python
├── .env                        # Variables de entorno (crear)
├── .gitignore                  # Archivos ignorados por Git
└── README.md                   # Este archivo
\`\`\`

## 🔌 API Endpoints

### Usuarios
- \`GET /api/usuarios\` - Obtener todos los usuarios
- \`POST /api/usuarios\` - Crear nuevo usuario
- \`GET /api/usuarios/{id}\` - Obtener usuario específico
- \`PUT /api/usuarios/{id}\` - Actualizar usuario
- \`DELETE /api/usuarios/{id}\` - Eliminar usuario

### Canciones
- \`GET /api/canciones\` - Obtener todas las canciones
- \`POST /api/canciones\` - Crear nueva canción
- \`GET /api/canciones/{id}\` - Obtener canción específica
- \`PUT /api/canciones/{id}\` - Actualizar canción
- \`DELETE /api/canciones/{id}\` - Eliminar canción
- \`GET /api/canciones/buscar\` - Buscar canciones

### Favoritos
- \`GET /api/favoritos\` - Obtener todos los favoritos
- \`POST /api/favoritos\` - Agregar a favoritos
- \`DELETE /api/favoritos/{id}\` - Eliminar de favoritos
- \`GET /api/usuarios/{id}/favoritos\` - Favoritos de un usuario
- \`POST /api/usuarios/{id}/favoritos/{song_id}\` - Agregar favorito específico
- \`DELETE /api/usuarios/{id}/favoritos/{song_id}\` - Eliminar favorito específico

### Autenticación
- \`POST /api/login\` - Iniciar sesión
- \`GET /api/ping\` - Verificar estado de la API

## 🎵 Funcionalidades

### Dashboard Principal
- Vista general de la aplicación
- Acceso rápido a todas las secciones
- Estadísticas básicas
- Acciones rápidas (crear usuario, canción, etc.)

### Gestión de Usuarios
- **Listar usuarios**: Ver todos los usuarios registrados
- **Crear usuario**: Formulario para agregar nuevos usuarios
- **Editar usuario**: Modificar información existente
- **Eliminar usuario**: Remover usuarios del sistema
- **Búsqueda**: Filtrar usuarios por nombre o email

### Gestión de Canciones
- **Biblioteca musical**: Ver todas las canciones disponibles
- **Agregar canciones**: Formulario completo con metadatos
- **Editar canciones**: Modificar información musical
- **Eliminar canciones**: Remover canciones de la biblioteca
- **Búsqueda**: Filtrar por título o artista
- **Vista alternativa**: Cambiar entre vista de tarjetas y lista
- **Favoritos rápidos**: Marcar/desmarcar favoritos directamente

### Sistema de Favoritos
- **Favoritos por usuario**: Cada usuario tiene su lista personal
- **Agregar/Remover**: Gestión fácil desde la lista de canciones
- **Vista completa**: Página dedicada a gestionar favoritos
- **Filtros**: Filtrar favoritos por usuario
- **Búsqueda**: Buscar dentro de favoritos

### Autenticación
- **Login seguro**: Autenticación basada en JWT
- **Sesiones**: Manejo de sesiones de usuario
- **Registro**: Crear nuevas cuentas
- **Logout**: Cerrar sesión de forma segura

## 🔧 Troubleshooting

### Problemas Comunes

#### 1. Error de conexión con la API
\`\`\`
Error: No se pudo conectar a la API
\`\`\`

**Solución:**
- Verifica que la API esté ejecutándose en el puerto correcto
- Revisa la variable \`API_BASE_URL\` en el archivo \`.env\`
- Usa la página "Estado de la API" para diagnosticar

#### 2. Error de usuario no identificado
\`\`\`
Error: No se pudo identificar el usuario actual
\`\`\`

**Solución:**
- Cierra sesión y vuelve a iniciar sesión
- Verifica que el usuario existe en la base de datos
- Revisa la consola del navegador para más detalles

#### 3. Favoritos no se cargan
**Solución:**
- Activa el modo debug en la página de canciones
- Verifica los logs en la consola del navegador
- Comprueba que el endpoint de favoritos funciona

#### 4. Problemas de instalación
\`\`\`
pip install error
\`\`\`

**Solución:**
- Asegúrate de estar en el entorno virtual
- Actualiza pip: \`pip install --upgrade pip\`
- Instala dependencias una por una si es necesario

### Debugging

#### Activar modo debug
1. En la página de canciones, haz clic en "Debug"
2. Abre la consola del navegador (F12)
3. Revisa los mensajes de debug

#### Endpoints de debugging
- \`/favorites/debug\` - Información de favoritos
- \`/api-status\` - Estado de la API
- \`/api/current-user\` - Información del usuario actual