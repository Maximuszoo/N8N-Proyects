# PDF Summary Generator

## Overview
Extracts and summarizes PDF documents applying the 80/20 Pareto principle to capture the most valuable 20% of content that provides 80% of the value, outputting professionally formatted PDF summaries.

<img width="1109" height="470" alt="image" src="https://github.com/user-attachments/assets/1b76f3b7-9b62-441c-bdd0-11ced910e456" />

## N8N Workflow

### Input
- **File Type**: PDF document
- **Content**: Books, academic papers, reports, or any lengthy document
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
   - Simple division for maximum content per chunk
   - Enables processing of very long documents

5. **AI Summarization (Ollama qwen3:8b)**
   - **System Prompt**: Expert reader and text synthesizer
   - **Core Strategy**:
     - **Pareto Principle (80/20)**: Focus on 20% essential content
     - Identify chapters/sections with greatest conceptual weight
     - Omit minor details, extensive examples, and non-core anecdotes
     - Focus on theses, conclusions, and relevant data
   - **Requirements**:
     - Maintain coherence across all fragments
     - Recognize content that spans multiple chunks
     - Merge fragmented ideas naturally
     - Never invent information not in source
     - No greetings, introductions, or courtesy phrases
     - Use valid Markdown formatting
     - Create structured sections with titles and subtitles
     - Include numbered or bulleted lists for key points
   - **Memory**: 1000-item buffer window for continuity
   - **Motivation**: Incentivized for quality and context maintenance

6. **Metadata Cleaning**
   - Removes `<think>` tags from AI responses
   - Cleans reasoning artifacts

7. **Content Aggregation**
   - Merges all summary chunks into single document
   - Maintains narrative flow

8. **Markdown File Creation**
   - Saves complete summary as `.md` file
   - Location: `/home/maximo/Descargas/resumen.md`

9. **PDF Generation**
   - Executes Python script: `PDFMaker.py`
   - Converts Markdown to styled PDF
   - Applies professional formatting:
     - Clean typography (Arial)
     - Colored headings (#333366)
     - Proper line spacing (1.5)
     - Adequate padding (20px)
   - Output: Timestamped PDF file

10. **File Management**
    - Creates timestamped output
    - Format: `Resumen_PDF_YYYYMMDD_HHMMSS.pdf`

### AI Model Configuration
- **Model**: Ollama qwen3:8b
- **Context Window**: Standard
- **Memory Type**: Buffer Window (1000 items)
- **Session Key**: Based on input text
- **Language**: Spanish (configurable)

### Output
- **Format**: PDF
- **Content Structure**:
  - Main sections with clear hierarchy
  - Three key ideas per section
  - Markdown formatting (headings, lists)
  - Concise, no-fluff summaries
  - Focus on essential concepts

## Usage

1. Place your PDF document in the configured input path
2. Execute the N8N workflow manually
3. Wait for summarization (time depends on document length)
4. Find your summary PDF in `/home/maximo/Descargas/`
5. Intermediate Markdown file is also saved

## Notes

- Ideal for long documents (books, research papers, reports)
- The AI is specifically tuned to apply Pareto principle
- Context window ensures continuity across document sections
- Output is immediately ready for reading or sharing
- All files timestamped to prevent overwrites
- Intermediate Markdown useful for further editing
