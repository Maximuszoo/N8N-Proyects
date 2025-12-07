# Formateador de Transcripciones

## Descripción General
Transforma automáticamente transcripciones académicas en bruto (con errores de reconocimiento de voz) en documentos PDF limpios y profesionalmente formateados usando procesamiento de texto impulsado por IA.

## Flujo de Trabajo N8N

### Entrada
- **Tipo de Archivo**: Archivo de texto plano (`.txt`)
- **Contenido**: Transcripción en bruto con potenciales errores de reconocimiento de voz
- **Ubicación**: Ruta de archivo configurable (predeterminado: `/home/maximo/Descargas/`)

### Pasos del Flujo de Trabajo

1. **Disparador Manual**
   - Ejecutar flujo de trabajo bajo demanda

2. **Lectura de Archivo**
   - Lee el archivo de texto de transcripción desde el disco

3. **Extracción de Texto**
   - Extrae contenido de texto plano del archivo

4. **Fragmentación Inteligente de Texto**
   - Divide el texto en fragmentos de 4000 caracteres
   - Añade 200 caracteres de solapamiento entre fragmentos para preservar contexto
   - Usa algoritmo de división inteligente que respeta:
     - Límites de párrafos
     - Finales de oraciones
     - Límites de palabras

5. **Procesamiento con IA (Ollama qwen3:8b)**
   - **Prompt del Sistema**: Procesa transcripciones académicas
   - **Tareas**:
     - Corrige errores de reconocimiento de voz basándose en contexto académico
     - Estructura contenido usando jerarquía Markdown
     - Mantiene continuidad entre fragmentos
     - Crea títulos, subtítulos y listas apropiados
     - Elimina metacomentarios
   - **Memoria**: Ventana buffer de 200 elementos para contexto

6. **Limpieza de Metadatos**
   - Elimina etiquetas `<think>` de las respuestas de la IA
   - Limpia artefactos de razonamiento de la IA

7. **Agregación de Contenido**
   - Fusiona todos los fragmentos procesados en un único documento Markdown

8. **Creación de Archivo Markdown**
   - Guarda contenido procesado como archivo `.md`
   - Ubicación: `/home/maximo/Descargas/resumen_transcripción.md`

9. **Generación de PDF**
   - Ejecuta script Python: `PDFMaker.py`
   - Convierte Markdown a PDF estilizado
   - Aplica estilo CSS profesional
   - Salida: Archivo PDF con marca de tiempo

10. **Gestión de Archivos**
    - Renombra archivo de salida con marca de tiempo
    - Formato: `Resumen_transcripción_YYYYMMDD_HHMMSS.pdf`

### Configuración del Modelo de IA
- **Modelo**: Ollama qwen3:8b
- **Ventana de Contexto**: Estándar
- **Tipo de Memoria**: Buffer Window (200 elementos)
- **Clave de Sesión**: Basada en texto de entrada

### Salida
- **Formato**: PDF
- **Estilo**: Diseño académico profesional con:
  - Tipografía limpia (Arial)
  - Encabezados estructurados
  - Espaciado y márgenes apropiados
  - Soporte de codificación UTF-8

## Uso

1. Coloca tu archivo de transcripción en la ruta de entrada configurada
2. Ejecuta el flujo de trabajo N8N manualmente
3. Espera el procesamiento (el tiempo depende de la longitud del documento)
4. Encuentra tu PDF formateado en `/home/maximo/Descargas/`

## Notas

- El flujo de trabajo procesa documentos largos en fragmentos para respetar los límites de contexto de la IA
- El solapamiento entre fragmentos asegura que no se pierda contexto
- La IA está instruida para evitar agregar saludos o metacomentarios
- Todos los archivos de salida tienen marca de tiempo para prevenir sobrescrituras
