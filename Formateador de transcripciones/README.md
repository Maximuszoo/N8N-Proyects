# Transcript Formatter

## Overview
Automatically transforms raw academic transcriptions (with speech recognition errors) into clean, professionally formatted PDF documents using AI-powered text processing.

<img width="1124" height="447" alt="Screenshot_20251207_144855" src="https://github.com/user-attachments/assets/23758d08-14fa-4c11-a274-127f19508b1e" />

## N8N Workflow

### Input
- **File Type**: Plain text file (`.txt`)
- **Content**: Raw transcription with potential speech recognition errors
- **Location**: Configurable file path (default: `~/Downloads/`)

### Workflow Steps

1. **Manual Trigger**
   - Execute workflow on demand

2. **File Reading**
   - Reads the transcription text file from disk

3. **Text Extraction**
   - Extracts plain text content from file

4. **Intelligent Text Chunking**
   - Splits text into 4000-character chunks
   - Adds 200-character overlap between chunks for context preservation
   - Uses smart splitting algorithm that respects:
     - Paragraph boundaries
     - Sentence endings
     - Word boundaries

5. **AI Processing (Ollama qwen3:8b)**
   - **System Prompt**: Processes academic transcriptions
   - **Tasks**:
     - Corrects speech recognition errors based on academic context
     - Structures content using Markdown hierarchy
     - Maintains continuity between fragments
     - Creates appropriate titles, subtitles, and lists
     - Removes meta-commentary
   - **Memory**: 200-item buffer window for context

6. **Metadata Cleaning**
   - Removes `<think>` tags from AI responses
   - Cleans up AI reasoning artifacts

7. **Content Aggregation**
   - Merges all processed chunks into single Markdown document

8. **Markdown File Creation**
   - Saves processed content as `.md` file
   - Location: `~/Downloads/resumen_transcripción.md`

9. **PDF Generation**
   - Executes Python script: `PDFMaker.py`
   - Converts Markdown to styled PDF
   - Applies professional CSS styling
   - Output: Timestamped PDF file

10. **File Management**
    - Renames output file with timestamp
    - Format: `Resumen_transcripción_YYYYMMDD_HHMMSS.pdf`

### AI Model Configuration
- **Model**: Ollama qwen3:8b
- **Context Window**: Standard
- **Memory Type**: Buffer Window (200 items)
- **Session Key**: Based on input text

### Output
- **Format**: PDF
- **Styling**: Professional academic layout with:
  - Clean typography (Arial)
  - Structured headings
  - Proper spacing and margins
  - UTF-8 encoding support

## Usage

1. Place your transcription file in the configured input path
2. Execute the N8N workflow manually
3. Wait for processing (time depends on document length)
4. Find your formatted PDF in `~/Downloads/`

## Notes

- The workflow processes long documents in chunks to respect AI context limits
- Overlap between chunks ensures no loss of context
- The AI is instructed to avoid adding greetings or meta-commentary
- All output files are timestamped to prevent overwrites
