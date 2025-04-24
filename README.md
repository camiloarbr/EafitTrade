# Eafit Trade 

## 📋 Descripción del Proyecto
Actualmente, los estudiantes y personal de EAFIT carecen de una fuente confiable y organizada de información sobre los vendedores en el campus. Esto dificulta encontrar opciones de compra, comparar precios y acceder a productos específicos. Nuestra aplicación resuelve esto proporcionando un catálogo digital con información detallada de los vendedores, mejorando la conexión entre compradores y vendedores.

## 🛠️ Tecnologías Utilizadas

- **Backend:** Django 5.1.6
- **Frontend:** HTML5, CSS3, JavaScript, Bootstrap
- **Base de datos:** SQLite (desarrollo), PostgreSQL (recomendado para producción)
- **Autenticación:** Sistema de autenticación de Django
- **Manejo de imágenes:** Pillow
- **Integración IA:** Google Gemini API para búsqueda inteligente
- **Despliegue:** Gunicorn, Whitenoise

## 🚀 Instrucciones de Instalación y Ejecución

### Prerrequisitos
- Python 3.8 o superior
- pip (gestor de paquetes de Python)
- Git

### 1. Crear y preparar el directorio del proyecto

```bash
# Crear un directorio para el proyecto (puedes usar el nombre que prefieras)
mkdir EafitTrade1
cd EafitTrade1

# Clonar el repositorio
git clone https://github.com/camiloarbr/EafitTrade.git

# Entrar al directorio del proyecto clonado
cd EafitTrade
```

### 2. Configurar el entorno virtual

```bash
# Crear el entorno virtual
python -m venv env

# Activar el entorno virtual en Windows
env\Scripts\activate

# Activar el entorno virtual en macOS/Linux
source env/bin/activate
```

### 3. Instalar dependencias
Con el entorno virtual activado (deberías ver `(env)` al inicio de la línea de comandos):

```bash
# Actualizar pip a la última versión
python -m pip install --upgrade pip

# Instalar las dependencias del proyecto desde requirements.txt
pip install -r requirements.txt
```

### 4. Configurar variables de entorno
Crear un archivo `.env` en el directorio raíz del proyecto con las siguientes variables:

```
GEMINI_API_KEY=tu_clave_de_api_google_gemini
```

### 5. Ejecutar migraciones de la base de datos

```bash
python manage.py migrate
```

### 6. Crear un superusuario (opcional)

```bash
python manage.py createsuperuser
```

### 7. Ejecutar el servidor de desarrollo

```bash
python manage.py runserver
```

La aplicación estará disponible en: http://127.0.0.1:8000/

## 📂 Estructura del Proyecto

```
EafitTrade/
├── eafit_trade/          # Configuración principal del proyecto
│   ├── settings.py       # Configuración de Django
│   ├── urls.py           # URLs principales
│   └── ...
├── products/             # Aplicación para gestión de productos
│   ├── models.py         # Modelos de datos
│   ├── views.py          # Lógica de vistas
│   ├── templates/        # Plantillas HTML
│   └── ...
├── seller_profiles/      # Aplicación para gestión de perfiles de vendedores
│   ├── models.py         # Modelos de datos
│   ├── views.py          # Lógica de vistas
│   ├── templates/        # Plantillas HTML
│   └── ...
├── media/                # Archivos subidos por usuarios
├── staticfiles/          # Archivos estáticos recopilados
├── requirements.txt      # Dependencias del proyecto
└── manage.py             # Script de gestión de Django
```

## 🔧 Solución de problemas comunes

### Error: "No such file or directory: 'requirements.txt'"
Si recibes este error, verifica que:
1. Estés en el directorio correcto (debe ser el directorio `EafitTrade` que contiene el archivo `requirements.txt`)
2. El archivo `requirements.txt` exista en tu directorio actual
3. Usa el comando `dir` (Windows) o `ls` (macOS/Linux) para verificar los archivos en tu directorio actual

### Error: "No module named 'django'"
Si recibes este error:
1. Verifica que el entorno virtual esté activado (deberías ver `(env)` al inicio de tu línea de comandos)
2. Asegúrate de haber instalado las dependencias correctamente con `pip install -r requirements.txt`

### Error: "manage.py not found"
Si recibes este error:
1. Asegúrate de estar en el directorio correcto (debe ser el directorio `EafitTrade` que contiene el archivo `manage.py`)
2. Usa `dir` o `ls` para verificar que `manage.py` existe en tu directorio actual

## 👥 Contribuir al Proyecto

1. Crea un fork del repositorio
2. Crea una rama para tu funcionalidad (`git checkout -b feature/nueva-funcionalidad`)
3. Realiza tus cambios y haz commits (`git commit -am 'Añade nueva funcionalidad'`)
4. Sube tus cambios (`git push origin feature/nueva-funcionalidad`)
5. Crea un Pull Request

## 📜 Licencia

Este proyecto está licenciado bajo la licencia MIT - ver el archivo LICENSE para más detalles.

## 📞 Contacto

Si tienes preguntas sobre el proyecto, puedes contactar a:
- Email: info@eafittrade.com
- GitHub: [camiloarbr](https://github.com/camiloarbr/EafitTrade)

