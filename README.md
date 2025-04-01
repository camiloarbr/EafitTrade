# Eafit Trade 

## Descripción del Problema
Actualmente, los estudiantes y personal de EAFIT carecen de una fuente confiable y organizada de información sobre los vendedores en el campus. Esto dificulta encontrar opciones de compra, comparar precios y acceder a productos específicos. Nuestra aplicación resuelve esto proporcionando un catálogo digital con información detallada de los vendedores, mejorando la conexión entre compradores y vendedores.

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

### 4. Configurar la base de datos

```bash
# Crear las migraciones
python manage.py makemigrations

# Aplicar las migraciones
python manage.py migrate
```

### 5. Ejecutar el servidor de desarrollo

```bash
python manage.py runserver
```

La aplicación estará disponible en: http://127.0.0.1:8000/

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

