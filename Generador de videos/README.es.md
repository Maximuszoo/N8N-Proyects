# Generador de Videos (Vidazor)

## Descripción General
Crea videos educativos sincronizados con diapositivas dinámicas desde transcripciones/scripts de texto y archivos de audio. Genera automáticamente diapositivas con marcas de tiempo, aplica estilos profesionales y sincroniza con narración de audio.

## Flujo de Trabajo N8N

### Entrada
- **Archivo de Texto**: Transcripción o script con información de tiempos (`.txt`)
- **Archivo de Audio**: Narración MP3 o WAV (referenciado en el flujo de trabajo)
- **Ubicación**: Ruta de archivo configurable (predeterminado: `~/Descargas/`)

### Pasos del Flujo de Trabajo

1. **Disparador Manual**
   - Ejecutar flujo de trabajo bajo demanda

2. **Lectura de Archivo**
   - Lee archivo de transcripción/script de texto desde el disco

3. **Extracción de Texto**
   - Extrae contenido de texto plano

4. **Fragmentación Inteligente de Texto**
   - Divide el texto en fragmentos de 4000 caracteres
   - **Sin solapamiento** (mantiene precisión temporal)
   - Respeta límites narrativos

5. **Generación de Diapositivas con IA (Ollama qwen3:8b)**
   - **Prompt del Sistema**: Convierte narrativa a diapositivas de presentación
   - **Configuración del Modelo**:
     - Contexto: 10240 tokens (extendido)
   - **Instrucciones Clave**:
     - Procesar como **fragmento continuo** (no inicio/final)
     - Crear **array JSON continuo único**
     - Generar títulos claros y 3-5 puntos clave por diapositiva
     - **Máximo 3 palabras por punto** (ideal: 1-2 palabras conceptuales)
     - Marcas de tiempo secuenciales sin brechas ni superposiciones
     - Formato: `MM:SS`
     - Sin saludos/despedidas artificiales
     - Salida JSON pura (sin bloques de código markdown)
   - **Reglas Estrictas de Tiempo**:
     - Sin brechas de tiempo entre diapositivas
     - Sin superposiciones de marcas de tiempo
     - Sin rangos de tiempo duplicados
     - Línea de tiempo continua desde el primer al último segundo
   - **Memoria**: Ventana mínima de 2 elementos (se enfoca en segmento actual)

6. **Limpieza de Metadatos**
   - Elimina etiquetas `<think>` de las respuestas de la IA
   - Limpia artefactos de razonamiento

7. **Agregación de JSON**
   - Fusiona todos los arrays de diapositivas en una única estructura
   - Mantiene secuencia temporal

8. **Exportación de Archivo**
   - Guarda JSON de diapositivas en archivo de texto
   - Ubicación: `~/Descargas/Escrito_presentación.txt`

9. **Generación de Video**
   - Ejecuta script Python: `generate_video.py`
   - **Parámetros del Script**:
     - Archivo de texto de entrada (JSON de diapositivas)
     - Ruta de archivo de audio
     - Ruta de video de salida
   - **Procesamiento**:
     - Parsea JSON de diapositivas con marcas de tiempo
     - Valida estructura de diapositivas contra schema
     - Genera imágenes de diapositivas con estilo seleccionado
     - Crea segmentos de video individuales
     - Sincroniza diapositivas con marcas de tiempo de audio
     - Fusiona todos los segmentos en video final
   - **Salida**: Video MP4 con marca de tiempo
   - Formato: `Video_YYYYMMDD_HHMMSS.mp4`

### Configuración del Modelo de IA
- **Modelo**: Ollama qwen3:8b
- **Ventana de Contexto**: 10240 tokens (extendida)
- **Tipo de Memoria**: Buffer Window (2 elementos - mínima)
- **Clave de Sesión**: Basada en texto de entrada

### Estilos de Video

El motor Vidazor soporta múltiples estilos profesionales:

- **Minimal Clean** (múltiples variantes de color)
  - Fondos limpios
  - Tipografía simple
  - Opciones de color: predeterminado, verde, naranja, morado
- **Geometric Boxes**
  - Diseños estructurados
  - Diseño basado en cajas
- **Modern Gradient**
  - Fondos de gradiente dinámicos
  - Aspecto contemporáneo
- **Split Screen**
  - Diseños de panel dual
- **Y más...**

Los estilos se seleccionan automáticamente o se pueden configurar en el script Python.

### Componentes Python

**generate_video.py**
- Motor principal de generación de video
- Parsing y validación de diapositivas
- Generación de imágenes con múltiples estilos
- Creación de segmentos de video
- Integración FFmpeg para renderizado final
- Manejo integral de errores

**fix_script.py**
- Validación y corrección de scripts
- Corrige problemas de tiempos
- Valida estructura de diapositivas

**slides.schema.json**
- Schema JSON para validación de diapositivas
- Define estructura requerida:
  - `inicio`: Tiempo de inicio (MM:SS o HH:MM:SS)
  - `fin`: Tiempo de fin (MM:SS o HH:MM:SS)
  - `titulo`: Título de diapositiva
  - `puntos`: Array de puntos de viñeta
  - `notas`: Notas opcionales del presentador

**test_styles.json**
- Ejemplos de configuración de estilos
- Definiciones de plantillas

### Salida
- **Formato**: Video MP4
- **Resolución**: Configurable (predeterminado: 1920x1080)
- **Características**:
  - Contenido audio-visual sincronizado
  - Diseños de diapositivas profesionales
  - Transiciones suaves
  - Cambios de diapositivas basados en marcas de tiempo
  - Renderizado de alta calidad

## Uso

1. Prepara tu archivo de texto de transcripción/script
2. Ten lista tu narración de audio (MP3/WAV)
3. Actualiza rutas de archivo en el flujo de trabajo N8N si es necesario
4. Ejecuta el flujo de trabajo N8N manualmente
5. Espera la generación de diapositivas y renderizado de video
6. Encuentra tu video en `~/Descargas/`

## Ejemplo de Formato de Diapositiva

```json
[
  {
    "inicio": "00:00",
    "fin": "00:15",
    "titulo": "Introducción",
    "puntos": [
      "Tema Principal",
      "Concepto Clave",
      "Vista General"
    ]
  },
  {
    "inicio": "00:15",
    "fin": "00:45",
    "titulo": "Primer Punto",
    "puntos": [
      "Detalle Uno",
      "Detalle Dos",
      "Resumen"
    ]
  }
]
```

## Mejores Prácticas

- **Mantén puntos concisos**: Máximo 3 palabras por punto de viñeta
- **Tiempos secuenciales**: Asegura que no haya brechas o superposiciones en marcas de tiempo
- **Títulos claros**: Usa títulos de diapositiva descriptivos pero breves
- **Estilo consistente**: Deja que el motor maneje el estilo automáticamente
- **Calidad de audio**: Usa narración de audio clara y de alta calidad

## Notas

- El flujo de trabajo está optimizado para narración continua (podcasts, conferencias)
- La ventana de contexto mínima previene transiciones artificiales
- Las marcas de tiempo deben ser secuenciales y sin brechas
- La IA está específicamente instruida para evitar introducciones/conclusiones por fragmento
- La generación de video puede llevar tiempo dependiendo de la longitud del contenido
- Todas las salidas tienen marca de tiempo para preservar múltiples versiones
- El script Python incluye manejo integral de errores y validación
