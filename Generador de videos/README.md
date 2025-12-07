# Video Generator (Vidazor)

## Overview
Creates synchronized educational videos with dynamic slides from text transcripts/scripts and audio files. Automatically generates slides with timestamps, applies professional styling, and synchronizes with audio narration.

<img width="1104" height="533" alt="image" src="https://github.com/user-attachments/assets/9cf828f5-c353-41c2-9bc5-6f1afe9c9d7f" />

## N8N Workflow

### Input
- **Text File**: Transcript or script with timing information (`.txt`)
- **Audio File**: MP3 or WAV narration (referenced in workflow)
- **Location**: Configurable file path (default: `/home/maximo/Descargas/`)

### Workflow Steps

1. **Manual Trigger**
   - Execute workflow on demand

2. **File Reading**
   - Reads text transcript/script file from disk

3. **Text Extraction**
   - Extracts plain text content

4. **Intelligent Text Chunking**
   - Splits text into 4000-character chunks
   - **No overlap** (maintains temporal precision)
   - Respects narrative boundaries

5. **AI Slide Generation (Ollama qwen3:8b)**
   - **System Prompt**: Converts narrative to presentation slides
   - **Model Configuration**:
     - Context: 10240 tokens (extended)
   - **Key Instructions**:
     - Process as **continuous fragment** (not beginning/end)
     - Create **single continuous JSON array**
     - Generate clear titles and 3-5 key points per slide
     - **Maximum 3 words per point** (ideal: 1-2 conceptual words)
     - Sequential timestamps without gaps or overlaps
     - Format: `MM:SS`
     - No artificial greetings/farewells
     - Pure JSON output (no markdown code blocks)
   - **Strict Timing Rules**:
     - No time gaps between slides
     - No timestamp overlaps
     - No duplicate time ranges
     - Continuous timeline from first to last second
   - **Memory**: Minimal 2-item window (focuses on current segment)

6. **Metadata Cleaning**
   - Removes `<think>` tags from AI responses
   - Cleans reasoning artifacts

7. **JSON Aggregation**
   - Merges all slide arrays into single structure
   - Maintains temporal sequence

8. **File Export**
   - Saves slides JSON to text file
   - Location: `/home/maximo/Descargas/Escrito_presentación.txt`

9. **Video Generation**
   - Executes Python script: `generate_video.py`
   - **Script Parameters**:
     - Input text file (slides JSON)
     - Audio file path
     - Output video path
   - **Processing**:
     - Parses slides JSON with timestamps
     - Validates slide structure against schema
     - Generates slide images with selected style
     - Creates individual video segments
     - Synchronizes slides with audio timestamps
     - Merges all segments into final video
   - **Output**: MP4 video with timestamp
   - Format: `Video_YYYYMMDD_HHMMSS.mp4`

### AI Model Configuration
- **Model**: Ollama qwen3:8b
- **Context Window**: 10240 tokens (extended)
- **Memory Type**: Buffer Window (2 items - minimal)
- **Session Key**: Based on input text

### Video Styles

The Vidazor engine supports multiple professional styles:

- **Minimal Clean** (multiple color variants)
  - Clean backgrounds
  - Simple typography
  - Color options: default, green, orange, purple
- **Geometric Boxes**
  - Structured layouts
  - Box-based design
- **Modern Gradient**
  - Dynamic gradient backgrounds
  - Contemporary look
- **Split Screen**
  - Dual-panel layouts
- **And more...**

Styles are automatically selected or can be configured in the Python script.

### Python Components

**generate_video.py**
- Main video generation engine
- Slide parsing and validation
- Image generation with multiple styles
- Video segment creation
- FFmpeg integration for final rendering
- Comprehensive error handling

**fix_script.py**
- Script validation and correction
- Fixes timing issues
- Validates slide structure

**slides.schema.json**
- JSON schema for slide validation
- Defines required structure:
  - `inicio`: Start time (MM:SS or HH:MM:SS)
  - `fin`: End time (MM:SS or HH:MM:SS)
  - `titulo`: Slide title
  - `puntos`: Array of bullet points
  - `notas`: Optional presenter notes

**test_styles.json**
- Style configuration examples
- Template definitions

### Output
- **Format**: MP4 video
- **Resolution**: Configurable (default: 1920x1080)
- **Features**:
  - Synchronized audio-visual content
  - Professional slide designs
  - Smooth transitions
  - Timestamp-based slide changes
  - High-quality rendering

## Usage

1. Prepare your transcript/script text file
2. Have your audio narration ready (MP3/WAV)
3. Update file paths in N8N workflow if needed
4. Execute the N8N workflow manually
5. Wait for slide generation and video rendering
6. Find your video in `/home/maximo/Descargas/`

## Slide Format Example

```json
[
  {
    "inicio": "00:00",
    "fin": "00:15",
    "titulo": "Introduction",
    "puntos": [
      "Main Topic",
      "Key Concept",
      "Overview"
    ]
  },
  {
    "inicio": "00:15",
    "fin": "00:45",
    "titulo": "First Point",
    "puntos": [
      "Detail One",
      "Detail Two",
      "Summary"
    ]
  }
]
```

## Best Practices

- **Keep points concise**: Maximum 3 words per bullet point
- **Sequential timing**: Ensure no gaps or overlaps in timestamps
- **Clear titles**: Use descriptive but brief slide titles
- **Consistent style**: Let the engine handle styling automatically
- **Audio quality**: Use clear, high-quality audio narration

## Notes

- The workflow is optimized for continuous narration (podcasts, lectures)
- Minimal context window prevents artificial transitions
- Timestamps must be sequential and gap-free
- The AI is specifically instructed to avoid introductions/conclusions per chunk
- Video generation can take time depending on content length
- All outputs are timestamped to preserve multiple versions
- The Python script includes comprehensive error handling and validation
