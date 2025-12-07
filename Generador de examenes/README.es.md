# Generador de Exámenes

## Descripción General
Crea cuestionarios HTML interactivos con preguntas generadas por IA desde documentos PDF, con interfaz moderna temática de Spotify con calificación automática y temporizador.

## Flujo de Trabajo N8N

### Entrada
- **Tipo de Archivo**: Documento PDF
- **Contenido**: Material educativo, contenido de estudio o documentación
- **Ubicación**: Ruta de archivo configurable (predeterminado: `/home/maximo/Descargas/`)

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
   - No requiere solapamiento para generación de preguntas

5. **Generación de Preguntas con IA (Ollama qwen3:8b)**
   - **Prompt del Sistema**: Genera preguntas de cuestionario en formato JSON
   - **Tipos de Preguntas**:
     - **Opción Única**: Exactamente una respuesta correcta
     - **Opción Múltiple**: Más de una respuesta correcta
   - **Requisitos**:
     - Preguntas comienzan con palabras interrogativas (Qué, Cuál, Cómo, Por qué)
     - Preguntas formateadas con `¿` y `?`
     - Mínimo 4 opciones por pregunta
     - Contexto claro en cada pregunta
     - Sin viñetas o casillas de verificación en opciones
   - **Salida**: Array JSON puro (sin bloques de código markdown)
   - **Memoria**: Ventana buffer de 1000 elementos

6. **Limpieza de Metadatos**
   - Elimina etiquetas `<think>` de las respuestas de la IA
   - Limpia artefactos de razonamiento de la IA

7. **Conversión de JSON a Quizdown**
   - Transforma preguntas JSON a formato Quizdown
   - Añade etiquetas de tipo: "(Single Choice)" o "(Multiple Choice)"
   - Formatea opciones con marcado apropiado:
     - Opción única: `1. [x]` para correcto, `1. [ ]` para incorrecto
     - Opción múltiple: `- [x]` para correcto, `- [ ]` para incorrecto

8. **Agregación de Contenido**
   - Fusiona todos los bloques de preguntas Quizdown

9. **Ensamblaje HTML**
   - Envuelve contenido Quizdown en plantilla HTML completa
   - **Estilo Temático de Spotify**:
     - Fondo: `#191414` (oscuro)
     - Color de acento: `#1DB954` (verde Spotify)
     - Tipografía limpia
   - **Configuración del Cuestionario**:
     - Temporizador: 600 segundos (10 minutos)
     - Mezclar preguntas: habilitado
     - Mezclar respuestas: habilitado
   - Integra librería Quizdown desde CDN

10. **Exportación HTML**
    - Guarda examen interactivo como archivo HTML
    - Asegura codificación UTF-8
    - Salida: Archivo HTML con marca de tiempo
    - Formato: `examen_YYYYMMDD_HHMMSS.html`

### Configuración del Modelo de IA
- **Modelo**: Ollama qwen3:8b
- **Ventana de Contexto**: Estándar
- **Tipo de Memoria**: Buffer Window (1000 elementos)
- **Clave de Sesión**: Basada en texto de entrada

### Salida
- **Formato**: Archivo HTML interactivo
- **Características**:
  - Autocontenido (incluye todas las dependencias)
  - Calificación automática
  - Seguimiento de progreso
  - Cuenta regresiva del temporizador
  - Preguntas y respuestas aleatorizadas
  - Retroalimentación instantánea
  - UI moderna con tema Spotify

## Uso

1. Coloca tu material de estudio PDF en la ruta de entrada configurada
2. Ejecuta el flujo de trabajo N8N manualmente
3. Espera la generación de preguntas (depende de la longitud del documento)
4. Abre el archivo HTML generado en cualquier navegador web
5. Realiza el examen con cronometraje y calificación automática

## Características del Cuestionario

- **Interactivo**: Haz clic para seleccionar respuestas
- **Cronometrado**: Temporizador de cuenta regresiva de 10 minutos
- **Aleatorizado**: Preguntas y respuestas se mezclan en cada carga
- **Retroalimentación Instantánea**: Ve respuestas correctas/incorrectas inmediatamente
- **Barra de Progreso**: Rastrea el estado de finalización
- **UI Moderna**: Tema oscuro inspirado en Spotify

## Notas

- Las preguntas se generan basándose en la estructura del contenido del PDF
- La IA está instruida para crear preguntas bien formateadas y contextuales
- Múltiples fragmentos permiten procesar documentos grandes
- Todos los exámenes tienen marca de tiempo para mantener historial de versiones
- El archivo HTML es completamente autocontenido y portable
