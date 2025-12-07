# Exam Generator

## Overview
Creates interactive HTML quizzes with AI-generated questions from PDF documents, featuring a modern Spotify-themed interface with automatic grading and timer.

<img width="1114" height="478" alt="image" src="https://github.com/user-attachments/assets/231173de-dc63-401a-bf91-3c1434a0868d" />

## N8N Workflow

### Input
- **File Type**: PDF document
- **Content**: Educational material, study content, or documentation
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
   - No overlap needed for question generation

5. **AI Question Generation (Ollama qwen3:8b)**
   - **System Prompt**: Generates quiz questions in JSON format
   - **Question Types**:
     - **Single Choice**: Exactly one correct answer
     - **Multiple Choice**: More than one correct answer
   - **Requirements**:
     - Questions start with interrogative words (Qué, Cuál, Cómo, Por qué)
     - Questions formatted with `¿` and `?`
     - Minimum 4 options per question
     - Clear context in each question
     - No bullet points or checkboxes in options
   - **Output**: Pure JSON array (no markdown code blocks)
   - **Memory**: 1000-item buffer window

6. **Metadata Cleaning**
   - Removes `<think>` tags from AI responses
   - Cleans AI reasoning artifacts

7. **JSON to Quizdown Conversion**
   - Transforms JSON questions to Quizdown format
   - Adds type labels: "(Single Choice)" or "(Multiple Choice)"
   - Formats options with proper markup:
     - Single choice: `1. [x]` for correct, `1. [ ]` for incorrect
     - Multiple choice: `- [x]` for correct, `- [ ]` for incorrect

8. **Content Aggregation**
   - Merges all Quizdown question blocks

9. **HTML Assembly**
   - Wraps Quizdown content in complete HTML template
   - **Spotify Theme Styling**:
     - Background: `#191414` (dark)
     - Accent color: `#1DB954` (Spotify green)
     - Clean typography
   - **Quiz Configuration**:
     - Timer: 600 seconds (10 minutes)
     - Shuffle questions: enabled
     - Shuffle answers: enabled
   - Integrates Quizdown library from CDN

10. **HTML Export**
    - Saves interactive exam as HTML file
    - Ensures UTF-8 encoding
    - Output: Timestamped HTML file
    - Format: `examen_YYYYMMDD_HHMMSS.html`

### AI Model Configuration
- **Model**: Ollama qwen3:8b
- **Context Window**: Standard
- **Memory Type**: Buffer Window (1000 items)
- **Session Key**: Based on input text

### Output
- **Format**: Interactive HTML file
- **Features**:
  - Self-contained (includes all dependencies)
  - Automatic grading
  - Progress tracking
  - Timer countdown
  - Randomized questions and answers
  - Instant feedback
  - Modern UI with Spotify theme

## Usage

1. Place your PDF study material in the configured input path
2. Execute the N8N workflow manually
3. Wait for question generation (depends on document length)
4. Open the generated HTML file in any web browser
5. Take the exam with automatic timing and grading

## Quiz Features

- **Interactive**: Click to select answers
- **Timed**: 10-minute countdown timer
- **Randomized**: Questions and answers shuffle on each load
- **Instant Feedback**: See correct/incorrect answers immediately
- **Progress Bar**: Track completion status
- **Modern UI**: Spotify-inspired dark theme

## Notes

- Questions are generated based on the content structure of the PDF
- The AI is instructed to create well-formatted, contextual questions
- Multiple chunks allow processing of large documents
- All exams are timestamped to maintain version history
- The HTML file is completely self-contained and portable
