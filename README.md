# N8N Projects Collection

[![License: Unlicense](https://img.shields.io/badge/license-Unlicense-blue.svg)](http://unlicense.org/)
[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![N8N](https://img.shields.io/badge/n8n-automation-orange.svg)](https://n8n.io/)

> **[🇪🇸 Versión en Español](./README.es.md)**

A comprehensive collection of N8N workflow automations with Python integrations for content creation, document processing, and multimedia generation. These workflows leverage AI capabilities to automate complex tasks in content production.

## 📋 Table of Contents

- [Overview](#overview)
- [Projects](#projects)
  - [Transcript Formatter](#transcript-formatter)
  - [Exam Generator](#exam-generator)
  - [Podcast Generator](#podcast-generator)
  - [PDF Summary Generator](#pdf-summary-generator)
  - [Video Generator](#video-generator)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)

## 🎯 Overview

This repository contains a suite of N8N workflows designed to automate content creation and document processing tasks. Each project integrates with AI services and uses custom Python scripts to handle specialized processing tasks such as video generation, podcast creation, and document formatting.

## 🚀 Projects

### 📝 Transcript Formatter

**Directory:** `Formateador de transcripciones/`

Transforms raw transcripts into beautifully formatted PDF documents with proper styling and structure.

**Features:**
- Converts Markdown transcripts to styled PDFs
- Automatic formatting with customizable CSS
- UTF-8 encoding support for multilingual content
- Clean, professional document layout

**Files:**
- `Formateador de transcripciones.json` - N8N workflow configuration
- `PDFMaker.py` - Python script for PDF generation

### 📚 Exam Generator

**Directory:** `Generador de examenes/`

Creates interactive quizzes and exams with AI-generated questions, featuring a modern Spotify-inspired theme.

**Features:**
- AI-powered question generation
- Interactive quiz interface using Quizdown
- Spotify-themed UI design
- Configurable timer and question shuffling
- Multiple choice questions with automatic grading

**Files:**
- `Generador de examenes.json` - N8N workflow with quiz generation logic

### 🎙️ Podcast Generator

**Directory:** `Generador de podcasts/Podcast_voces_mejoradas/`

Generates realistic podcast conversations from text scripts with multiple speaker voices and natural pacing.

**Features:**
- Multi-speaker podcast generation
- Advanced voice configuration
- JSON parsing from AI-generated content
- Speaker role assignment and voice differentiation
- Automatic audio mixing

**Files:**
- `Generador de podcasts.json` - N8N workflow configuration
- `Podcast.py` - Main podcast generation script
- `model.py` - Data models for podcast structure
- `configurar_voces.py` - Voice configuration utilities
- `debug_parser.py` - JSON parsing debugging tools
- `fix_script.py` - Script correction utilities
- `requirements.txt` - Python dependencies

### 📄 PDF Summary Generator

**Directory:** `Generador de resumenes PDF/`

Extracts text from PDF documents and generates concise, formatted summaries.

**Features:**
- PDF text extraction
- AI-powered summarization
- Markdown to PDF conversion
- Professional document styling
- UTF-8 encoding support

**Files:**
- `Generador de resumenes de PDFs.json` - N8N workflow configuration
- `PDFMaker.py` - PDF generation script

### 🎬 Video Generator (Vidazor)

**Directory:** `Generador de videos/Vidazor/`

Creates synchronized educational videos with dynamic slides, audio narration, and professional styling.

**Features:**
- Automated slide generation from JSON/text
- Audio-video synchronization
- Multiple design styles (minimal, geometric, gradients)
- Timestamp-based slide transitions
- MP4 video output with customizable resolution
- Smart text formatting and layout

**Files:**
- `Generador de videos.json` - N8N workflow configuration
- `generate_video.py` - Main video generation script
- `fix_script.py` - Script validation and correction
- `slides.schema.json` - JSON schema for slide validation
- `test_styles.json` - Style configuration examples
- `requirements.txt` - Python dependencies

**Supported Styles:**
- Minimal Clean (multiple color variants)
- Geometric Boxes
- Modern Gradient
- Split Screen
- And more...

## 📦 Prerequisites

### System Requirements

- **Python:** 3.8 or higher
- **N8N:** Latest version
- **FFmpeg:** Required for video generation
- **System Fonts:** For text rendering in videos

### Python Packages

Different projects require different dependencies. Install them as needed:

```bash
# For PDF generation
pip install markdown2 weasyprint

# For podcast generation
pip install -r "Generador de podcasts/Podcast_voces_mejoradas/requirements.txt"

# For video generation
pip install -r "Generador de videos/Vidazor/requirements.txt"
```

## 🔧 Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Maximuszoo/N8N-Proyects.git
   cd N8N-Proyects
   ```

2. **Import workflows into N8N:**
   - Open your N8N instance
   - Navigate to Workflows → Import from File
   - Select the desired `.json` workflow file
   - Configure the workflow credentials and parameters

3. **Install Python dependencies:**
   ```bash
   # Install dependencies for specific projects
   cd "Generador de videos/Vidazor"
   pip install -r requirements.txt
   ```

4. **Configure paths:**
   - Update file paths in N8N workflows to match your system
   - Ensure Python scripts have execution permissions

## 💡 Usage

### Running N8N Workflows

1. Open N8N web interface
2. Select the imported workflow
3. Configure input parameters
4. Execute the workflow manually or set up triggers

### Running Python Scripts Directly

#### Video Generator Example:
```bash
cd "Generador de videos/Vidazor"
python generate_video.py input.txt audio.mp3 output.mp4
```

#### Podcast Generator Example:
```bash
cd "Generador de podcasts/Podcast_voces_mejoradas"
python Podcast.py input_script.json output_audio.mp3
```

#### PDF Formatter Example:
```bash
python "Formateador de transcripciones/PDFMaker.py" input.md output.pdf
```

## 📁 Project Structure

```
N8N-Proyects/
├── README.md                              # This file (English)
├── README.es.md                           # Spanish version
├── .gitignore                             # Git ignore rules
├── Formateador de transcripciones/        # Transcript formatting
├── Generador de examenes/                 # Exam generation
├── Generador de podcasts/                 # Podcast creation
│   └── Podcast_voces_mejoradas/          # Enhanced podcast generator
├── Generador de resumenes PDF/            # PDF summarization
└── Generador de videos/                   # Video generation
    └── Vidazor/                          # Video generation engine
```

## 🤝 Contributing

Contributions are welcome! This project is released into the public domain under The Unlicense.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This is free and unencumbered software released into the public domain.

Anyone is free to copy, modify, publish, use, compile, sell, or distribute this software, either in source code form or as a compiled binary, for any purpose, commercial or non-commercial, and by any means.

For more information, please refer to [The Unlicense](http://unlicense.org/).

---

**Made with ❤️ for the N8N community**
