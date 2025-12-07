# Podcast Generator

## Overview
Converts PDF documents into dynamic, conversational podcast audio with two AI-generated speakers (VOZ1 and VOZ2), creating engaging educational content in MP3 format.

## N8N Workflow

### Input
- **File Type**: PDF document
- **Content**: Educational material, articles, or any text content
- **Location**: Configurable file path (default: `/home/maximo/Descargas/`)

### Workflow Steps

1. **Manual Trigger**
   - Execute workflow on demand

2. **File Reading**
   - Reads PDF file from disk

3. **PDF Text Extraction**
   - Extracts all text content from PDF

4. **Text Division**
   - Splits text into 8000-character chunks
   - Allows processing of large documents
   - Simple division without overlap

5. **AI Dialogue Generation (Ollama qwen3:8b)**
   - **System Prompt**: Converts content to podcast dialogue
   - **Model Configuration**: 
     - Context: 10240 tokens (extended for better continuity)
   - **Dialogue Requirements**:
     - Two speakers: VOZ1 and VOZ2
     - Natural conversational language
     - Use of filler words: "bueno", "entonces", "¿verdad?"
     - Dynamic and didactic approach
     - Educational focus
     - No greetings/farewells per fragment (maintains continuity)
   - **Output Format**: Pure JSON array
     ```json
     [
       {"hablante": "VOZ1", "texto": "dialogue here"},
       {"hablante": "VOZ2", "texto": "response here"}
     ]
     ```
   - **Memory**: 1000-item buffer window for dialogue flow

6. **Metadata Cleaning**
   - Removes `<think>` tags from AI responses
   - Cleans reasoning artifacts

7. **Text File Accumulation**
   - Appends generated dialogue JSON to cumulative text file
   - Location: `/home/maximo/Descargas/guion.txt`
   - Builds complete podcast script across all chunks

8. **Audio Generation**
   - Executes Python script: `Podcast.py`
   - **Script Functions**:
     - Parses JSON dialogue structure
     - Extracts dirty JSON from AI output (handles malformed responses)
     - Validates podcast JSON structure
     - Generates speech for each speaker with distinct voices
     - Merges audio segments into single track
   - **Output**: MP3 audio file with timestamp
   - Format: `podcast_YYYYMMDD_HHMMSS.mp3`

9. **File Management**
   - Renames script file with timestamp
   - Keeps version history of generated scripts

### AI Model Configuration
- **Model**: Ollama qwen3:8b
- **Context Window**: 10240 tokens (extended)
- **Memory Type**: Buffer Window (1000 items)
- **Session Key**: Based on input text
- **Language**: Spanish

### Python Components

**Podcast.py**
- Main podcast generation script
- Handles JSON parsing from AI output
- Manages voice synthesis
- Audio file merging

**model.py**
- Data models for podcast structure
- PodcastModel and TextBlock classes

**configurar_voces.py**
- Voice configuration utilities
- Speaker voice differentiation

**debug_parser.py**
- JSON parsing debugging tools
- Handles malformed AI responses

**fix_script.py**
- Script correction utilities
- Validates and repairs dialogue structure

### Output
- **Format**: MP3 audio
- **Features**:
  - Two distinct speaker voices
  - Natural conversation flow
  - Educational content
  - Professional audio quality
  - Timestamped filename

## Usage

1. Place your PDF content in the configured input path
2. Execute the N8N workflow manually
3. Wait for dialogue generation and audio synthesis
4. Find your podcast MP3 in `/home/maximo/Descargas/`
5. The script file is also saved for reference

## Podcast Characteristics

- **Dynamic**: Natural back-and-forth conversation
- **Educational**: Focused on learning and understanding
- **Didactic**: Clear explanations and examples
- **Conversational**: Uses natural language patterns
- **Continuous**: No interruptions between segments
- **Engaging**: Maintains listener interest

## Notes

- The workflow processes content in chunks to maintain context
- Each chunk continues the conversation naturally
- No introductions or closings per chunk for seamless continuity
- The AI is optimized for creating educational dialogue
- Voice configuration can be customized in Python scripts
- All outputs are timestamped to preserve multiple versions
