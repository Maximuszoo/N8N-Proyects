# N8N Projects Collection

[![License: Unlicense](https://img.shields.io/badge/license-Unlicense-blue.svg)](http://unlicense.org/)
[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![N8N](https://img.shields.io/badge/n8n-automation-orange.svg)](https://n8n.io/)
[![Ollama](https://img.shields.io/badge/-Ollama-000000?logo=ollama&logoColor=white&style=flat)](https://ollama.com/)

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

## 🤝 Contributing

Contributions are welcome! This project is released into the public domain under The Unlicense.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This is free and unencumbered software released into the public domain.

For more information, please refer to [The Unlicense](http://unlicense.org/).
