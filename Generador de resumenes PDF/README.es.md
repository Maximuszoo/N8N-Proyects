# Generador de Resúmenes PDF

## Descripción General
Extrae y resume documentos PDF aplicando el principio de Pareto 80/20 para capturar el 20% más valioso del contenido que proporciona el 80% del valor, generando resúmenes PDF profesionalmente formateados.

## Flujo de Trabajo N8N

### Entrada
- **Tipo de Archivo**: Documento PDF
- **Contenido**: Libros, artículos académicos, informes o cualquier documento extenso
- **Ubicación**: Ruta de archivo configurable (predeterminado: `~/Descargas/`)

### Pasos del Flujo de Trabajo

1. **Disparador Manual**
   - Ejecutar flujo de trabajo bajo demanda

2. **Lectura de Archivo**
   - Lee archivo PDF desde el disco

3. **Extracción de Texto del PDF**
   - Extrae todo el contenido de texto del PDF

4. **División de Texto**
   - Divide el texto en fragmentos de 8000 caracteres
   - División simple para máximo contenido por fragmento
   - Permite procesar documentos muy largos

5. **Resumen con IA (Ollama qwen3:8b)**
   - **Prompt del Sistema**: Lector experto y sintetizador de textos
   - **Estrategia Central**:
     - **Principio de Pareto (80/20)**: Enfocarse en 20% de contenido esencial
     - Identificar capítulos/secciones con mayor peso conceptual
     - Omitir detalles menores, ejemplos extensos y anécdotas no centrales
     - Enfocarse en tesis, conclusiones y datos relevantes
   - **Requisitos**:
     - Mantener coherencia a través de todos los fragmentos
     - Reconocer contenido que abarca múltiples fragmentos
     - Fusionar ideas fragmentadas naturalmente
     - Nunca inventar información no presente en la fuente
     - Sin saludos, introducciones o frases de cortesía
     - Usar formateo Markdown válido
     - Crear secciones estructuradas con títulos y subtítulos
     - Incluir listas numeradas o con viñetas para puntos clave
   - **Memoria**: Ventana buffer de 1000 elementos para continuidad
   - **Motivación**: Incentivado por calidad y mantenimiento de contexto

6. **Limpieza de Metadatos**
   - Elimina etiquetas `<think>` de las respuestas de la IA
   - Limpia artefactos de razonamiento

7. **Agregación de Contenido**
   - Fusiona todos los fragmentos de resumen en un único documento
   - Mantiene flujo narrativo

8. **Creación de Archivo Markdown**
   - Guarda resumen completo como archivo `.md`
   - Ubicación: `~/Descargas/resumen.md`

9. **Generación de PDF**
   - Ejecuta script Python: `PDFMaker.py`
   - Convierte Markdown a PDF estilizado
   - Aplica formateo profesional:
     - Tipografía limpia (Arial)
     - Encabezados coloreados (#333366)
     - Espaciado de línea apropiado (1.5)
     - Padding adecuado (20px)
   - Salida: Archivo PDF con marca de tiempo

10. **Gestión de Archivos**
    - Crea salida con marca de tiempo
    - Formato: `Resumen_PDF_YYYYMMDD_HHMMSS.pdf`

### Configuración del Modelo de IA
- **Modelo**: Ollama qwen3:8b
- **Ventana de Contexto**: Estándar
- **Tipo de Memoria**: Buffer Window (1000 elementos)
- **Clave de Sesión**: Basada en texto de entrada
- **Idioma**: Español (configurable)

### Salida
- **Formato**: PDF
- **Estructura del Contenido**:
  - Secciones principales con jerarquía clara
  - Tres ideas clave por sección
  - Formateo Markdown (encabezados, listas)
  - Resúmenes concisos, sin relleno
  - Enfoque en conceptos esenciales

## Uso

1. Coloca tu documento PDF en la ruta de entrada configurada
2. Ejecuta el flujo de trabajo N8N manualmente
3. Espera el resumen (el tiempo depende de la longitud del documento)
4. Encuentra tu PDF de resumen en `~/Descargas/`
5. El archivo Markdown intermedio también se guarda

## Notas

- Ideal para documentos largos (libros, artículos de investigación, informes)
- La IA está específicamente ajustada para aplicar el principio de Pareto
- La ventana de contexto asegura continuidad a través de secciones del documento
- La salida está inmediatamente lista para lectura o compartir
- Todos los archivos con marca de tiempo para prevenir sobrescrituras
- El Markdown intermedio es útil para edición adicional
