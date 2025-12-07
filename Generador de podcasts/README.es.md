# Generador de Podcasts

## Descripción General
Convierte documentos PDF en audio de podcast dinámico y conversacional con dos hablantes generados por IA (VOZ1 y VOZ2), creando contenido educativo atractivo en formato MP3.

## Flujo de Trabajo N8N

### Entrada
- **Tipo de Archivo**: Documento PDF
- **Contenido**: Material educativo, artículos o cualquier contenido de texto
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
   - Permite procesar documentos grandes
   - División simple sin solapamiento

5. **Generación de Diálogo con IA (Ollama qwen3:8b)**
   - **Prompt del Sistema**: Convierte contenido a diálogo de podcast
   - **Configuración del Modelo**: 
     - Contexto: 10240 tokens (extendido para mejor continuidad)
   - **Requisitos del Diálogo**:
     - Dos hablantes: VOZ1 y VOZ2
     - Lenguaje conversacional natural
     - Uso de muletillas: "bueno", "entonces", "¿verdad?"
     - Enfoque dinámico y didáctico
     - Enfoque educativo
     - Sin saludos/despedidas por fragmento (mantiene continuidad)
   - **Formato de Salida**: Array JSON puro
     ```json
     [
       {"hablante": "VOZ1", "texto": "diálogo aquí"},
       {"hablante": "VOZ2", "texto": "respuesta aquí"}
     ]
     ```
   - **Memoria**: Ventana buffer de 1000 elementos para flujo del diálogo

6. **Limpieza de Metadatos**
   - Elimina etiquetas `<think>` de las respuestas de la IA
   - Limpia artefactos de razonamiento

7. **Acumulación de Archivo de Texto**
   - Añade JSON de diálogo generado a archivo de texto acumulativo
   - Ubicación: `/home/maximo/Descargas/guion.txt`
   - Construye guion completo del podcast a través de todos los fragmentos

8. **Generación de Audio**
   - Ejecuta script Python: `Podcast.py`
   - **Funciones del Script**:
     - Parsea estructura de diálogo JSON
     - Extrae JSON sucio de salida de IA (maneja respuestas malformadas)
     - Valida estructura JSON del podcast
     - Genera voz para cada hablante con voces distintas
     - Fusiona segmentos de audio en una única pista
   - **Salida**: Archivo de audio MP3 con marca de tiempo
   - Formato: `podcast_YYYYMMDD_HHMMSS.mp3`

9. **Gestión de Archivos**
   - Renombra archivo de script con marca de tiempo
   - Mantiene historial de versiones de scripts generados

### Configuración del Modelo de IA
- **Modelo**: Ollama qwen3:8b
- **Ventana de Contexto**: 10240 tokens (extendida)
- **Tipo de Memoria**: Buffer Window (1000 elementos)
- **Clave de Sesión**: Basada en texto de entrada
- **Idioma**: Español

### Componentes Python

**Podcast.py**
- Script principal de generación de podcast
- Maneja parsing de JSON desde salida de IA
- Gestiona síntesis de voz
- Mezcla de archivos de audio

**model.py**
- Modelos de datos para estructura de podcast
- Clases PodcastModel y TextBlock

**configurar_voces.py**
- Utilidades de configuración de voz
- Diferenciación de voces de hablantes

**debug_parser.py**
- Herramientas de depuración de parsing JSON
- Maneja respuestas malformadas de IA

**fix_script.py**
- Utilidades de corrección de script
- Valida y repara estructura de diálogo

### Salida
- **Formato**: Audio MP3
- **Características**:
  - Dos voces de hablantes distintas
  - Flujo de conversación natural
  - Contenido educativo
  - Calidad de audio profesional
  - Nombre de archivo con marca de tiempo

## Uso

1. Coloca tu contenido PDF en la ruta de entrada configurada
2. Ejecuta el flujo de trabajo N8N manualmente
3. Espera la generación del diálogo y síntesis de audio
4. Encuentra tu podcast MP3 en `/home/maximo/Descargas/`
5. El archivo de guion también se guarda como referencia

## Características del Podcast

- **Dinámico**: Conversación natural de ida y vuelta
- **Educativo**: Enfocado en aprendizaje y comprensión
- **Didáctico**: Explicaciones claras y ejemplos
- **Conversacional**: Usa patrones de lenguaje natural
- **Continuo**: Sin interrupciones entre segmentos
- **Atractivo**: Mantiene el interés del oyente

## Notas

- El flujo de trabajo procesa contenido en fragmentos para mantener contexto
- Cada fragmento continúa la conversación naturalmente
- Sin introducciones o cierres por fragmento para continuidad sin fisuras
- La IA está optimizada para crear diálogo educativo
- La configuración de voz se puede personalizar en scripts Python
- Todas las salidas tienen marca de tiempo para preservar múltiples versiones
