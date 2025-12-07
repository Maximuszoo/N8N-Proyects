# Colección de Proyectos N8N

[![Licencia: Unlicense](https://img.shields.io/badge/licencia-Unlicense-blue.svg)](http://unlicense.org/)
[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![N8N](https://img.shields.io/badge/n8n-automatización-orange.svg)](https://n8n.io/)

> **[🇬🇧 English Version](./README.md)**

Una colección completa de flujos de trabajo de automatización N8N con integraciones de Python para creación de contenido, procesamiento de documentos y generación multimedia. Estos flujos de trabajo aprovechan las capacidades de IA para automatizar tareas complejas en la producción de contenido.

## 📋 Tabla de Contenidos

- [Descripción General](#descripción-general)
- [Proyectos](#proyectos)
  - [Formateador de Transcripciones](#formateador-de-transcripciones)
  - [Generador de Exámenes](#generador-de-exámenes)
  - [Generador de Podcasts](#generador-de-podcasts)
  - [Generador de Resúmenes PDF](#generador-de-resúmenes-pdf)
  - [Generador de Videos](#generador-de-videos)
- [Requisitos Previos](#requisitos-previos)
- [Instalación](#instalación)
- [Uso](#uso)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Contribuciones](#contribuciones)
- [Licencia](#licencia)

## 🎯 Descripción General

Este repositorio contiene un conjunto de flujos de trabajo de N8N diseñados para automatizar tareas de creación de contenido y procesamiento de documentos. Cada proyecto se integra con servicios de IA y utiliza scripts personalizados de Python para manejar tareas de procesamiento especializadas como generación de videos, creación de podcasts y formateo de documentos.

## 🚀 Proyectos

### 📝 Formateador de Transcripciones

**Directorio:** `Formateador de transcripciones/`

Transforma transcripciones en bruto en documentos PDF bellamente formateados con estilo y estructura adecuados.

**Características:**
- Convierte transcripciones Markdown a PDFs estilizados
- Formateo automático con CSS personalizable
- Soporte de codificación UTF-8 para contenido multilingüe
- Diseño de documento limpio y profesional

**Archivos:**
- `Formateador de transcripciones.json` - Configuración del flujo de trabajo N8N
- `PDFMaker.py` - Script Python para generación de PDF

### 📚 Generador de Exámenes

**Directorio:** `Generador de examenes/`

Crea cuestionarios y exámenes interactivos con preguntas generadas por IA, presentando un tema moderno inspirado en Spotify.

**Características:**
- Generación de preguntas impulsada por IA
- Interfaz de cuestionario interactiva usando Quizdown
- Diseño de UI temática de Spotify
- Temporizador configurable y mezcla de preguntas
- Preguntas de opción múltiple con calificación automática

**Archivos:**
- `Generador de examenes.json` - Flujo de trabajo N8N con lógica de generación de cuestionarios

### 🎙️ Generador de Podcasts

**Directorio:** `Generador de podcasts/Podcast_voces_mejoradas/`

Genera conversaciones de podcast realistas desde guiones de texto con múltiples voces de hablantes y ritmo natural.

**Características:**
- Generación de podcasts con múltiples hablantes
- Configuración avanzada de voces
- Análisis JSON de contenido generado por IA
- Asignación de roles de hablante y diferenciación de voces
- Mezcla automática de audio

**Archivos:**
- `Generador de podcasts.json` - Configuración del flujo de trabajo N8N
- `Podcast.py` - Script principal de generación de podcasts
- `model.py` - Modelos de datos para estructura de podcast
- `configurar_voces.py` - Utilidades de configuración de voz
- `debug_parser.py` - Herramientas de depuración de análisis JSON
- `fix_script.py` - Utilidades de corrección de scripts
- `requirements.txt` - Dependencias de Python

### 📄 Generador de Resúmenes PDF

**Directorio:** `Generador de resumenes PDF/`

Extrae texto de documentos PDF y genera resúmenes concisos y formateados.

**Características:**
- Extracción de texto de PDF
- Resumen impulsado por IA
- Conversión de Markdown a PDF
- Estilo profesional de documentos
- Soporte de codificación UTF-8

**Archivos:**
- `Generador de resumenes de PDFs.json` - Configuración del flujo de trabajo N8N
- `PDFMaker.py` - Script de generación de PDF

### 🎬 Generador de Videos (Vidazor)

**Directorio:** `Generador de videos/Vidazor/`

Crea videos educativos sincronizados con diapositivas dinámicas, narración de audio y estilo profesional.

**Características:**
- Generación automática de diapositivas desde JSON/texto
- Sincronización de audio y video
- Múltiples estilos de diseño (minimal, geométrico, degradados)
- Transiciones de diapositivas basadas en marcas de tiempo
- Salida de video MP4 con resolución personalizable
- Formateo y diseño inteligente de texto

**Archivos:**
- `Generador de videos.json` - Configuración del flujo de trabajo N8N
- `generate_video.py` - Script principal de generación de video
- `fix_script.py` - Validación y corrección de scripts
- `slides.schema.json` - Esquema JSON para validación de diapositivas
- `test_styles.json` - Ejemplos de configuración de estilos
- `requirements.txt` - Dependencias de Python

**Estilos Soportados:**
- Minimal Clean (múltiples variantes de color)
- Geometric Boxes
- Modern Gradient
- Split Screen
- Y más...

## 📦 Requisitos Previos

### Requisitos del Sistema

- **Python:** 3.8 o superior
- **N8N:** Última versión
- **FFmpeg:** Requerido para generación de video
- **Fuentes del Sistema:** Para renderizado de texto en videos

### Paquetes de Python

Diferentes proyectos requieren diferentes dependencias. Instálalas según sea necesario:

```bash
# Para generación de PDF
pip install markdown2 weasyprint

# Para generación de podcasts
pip install -r "Generador de podcasts/Podcast_voces_mejoradas/requirements.txt"

# Para generación de videos
pip install -r "Generador de videos/Vidazor/requirements.txt"
```

## 🔧 Instalación

1. **Clonar el repositorio:**
   ```bash
   git clone https://github.com/Maximuszoo/N8N-Proyects.git
   cd N8N-Proyects
   ```

2. **Importar flujos de trabajo a N8N:**
   - Abrir tu instancia de N8N
   - Navegar a Workflows → Import from File
   - Seleccionar el archivo de flujo de trabajo `.json` deseado
   - Configurar las credenciales y parámetros del flujo de trabajo

3. **Instalar dependencias de Python:**
   ```bash
   # Instalar dependencias para proyectos específicos
   cd "Generador de videos/Vidazor"
   pip install -r requirements.txt
   ```

4. **Configurar rutas:**
   - Actualizar las rutas de archivo en los flujos de trabajo de N8N para que coincidan con tu sistema
   - Asegurar que los scripts de Python tengan permisos de ejecución

## 💡 Uso

### Ejecutar Flujos de Trabajo de N8N

1. Abrir la interfaz web de N8N
2. Seleccionar el flujo de trabajo importado
3. Configurar parámetros de entrada
4. Ejecutar el flujo de trabajo manualmente o configurar disparadores

### Ejecutar Scripts de Python Directamente

#### Ejemplo del Generador de Videos:
```bash
cd "Generador de videos/Vidazor"
python generate_video.py entrada.txt audio.mp3 salida.mp4
```

#### Ejemplo del Generador de Podcasts:
```bash
cd "Generador de podcasts/Podcast_voces_mejoradas"
python Podcast.py guion_entrada.json audio_salida.mp3
```

#### Ejemplo del Formateador de PDF:
```bash
python "Formateador de transcripciones/PDFMaker.py" entrada.md salida.pdf
```

## 📁 Estructura del Proyecto

```
N8N-Proyects/
├── README.md                              # Versión en inglés
├── README.es.md                           # Este archivo (Español)
├── .gitignore                             # Reglas de ignorar Git
├── Formateador de transcripciones/        # Formateo de transcripciones
├── Generador de examenes/                 # Generación de exámenes
├── Generador de podcasts/                 # Creación de podcasts
│   └── Podcast_voces_mejoradas/          # Generador de podcasts mejorado
├── Generador de resumenes PDF/            # Resumen de PDFs
└── Generador de videos/                   # Generación de videos
    └── Vidazor/                          # Motor de generación de videos
```

## 🤝 Contribuciones

¡Las contribuciones son bienvenidas! Este proyecto se libera al dominio público bajo The Unlicense.

1. Hacer fork del repositorio
2. Crear tu rama de características (`git checkout -b feature/CaracteristicaAsombrosa`)
3. Hacer commit de tus cambios (`git commit -m 'Agregar alguna CaracteristicaAsombrosa'`)
4. Hacer push a la rama (`git push origin feature/CaracteristicaAsombrosa`)
5. Abrir un Pull Request

## 📝 Licencia

Este es software libre y sin restricciones liberado al dominio público.

Cualquiera es libre de copiar, modificar, publicar, usar, compilar, vender o distribuir este software, ya sea en forma de código fuente o como binario compilado, para cualquier propósito, comercial o no comercial, y por cualquier medio.

Para más información, consulta [The Unlicense](http://unlicense.org/).

---

**Hecho con ❤️ para la comunidad N8N**
