#!/usr/bin/env python3
"""
Script para generar videos MP4 sincronizados con diapositivas desde texto/JSON y audio.

Uso:
    python generate_video.py input_txt_path audio_path output_video_path

Args:
    input_txt_path: Ruta completa al archivo TXT/MD con JSON o texto con bloques [HH:MM - HH:MM]
    audio_path: Ruta completa al archivo de audio (mp3/wav)
    output_video_path: Ruta completa donde guardar el video MP4 generado
"""

import argparse
import json
import os
import re
import subprocess
import sys
import hashlib
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Any, Tuple, Optional

# Dependencias externas
try:
    from PIL import Image, ImageDraw, ImageFont
    import jsonschema
except ImportError as e:
    print(f"Error: Falta instalar dependencias. Ejecuta: pip install -r requirements.txt")
    print(f"Error específico: {e}")
    sys.exit(1)


class VideoGeneratorError(Exception):
    """Excepción personalizada para errores del generador de video."""
    pass


class StyleManager:
    """Maneja los diferentes estilos de diapositivas y su selección aleatoria."""
    
    def __init__(self):
        # Solo estilos universales que funcionan con cualquier cantidad de conceptos
        self.available_styles = [
            'minimal_clean',
            'minimal_clean_green',
            'minimal_clean_orange', 
            'minimal_clean_purple',
            'geometric_boxes',
            'banner_style',
            'banner_style_green',
            'banner_style_orange',
            'banner_style_purple'
        ]
        
        self.last_style = None
        # Contadores para distribución uniforme
        self.usage_count = {style: 0 for style in self.available_styles}
        self.total_selections = 0
        
        # Paletas de colores para modo oscuro
        self.color_palettes = {
            'blue': {
                'bg': (25, 25, 35),
                'primary': (100, 149, 237),
                'secondary': (70, 130, 220),
                'text': (255, 255, 255),
                'accent': (135, 175, 255)
            },
            'green': {
                'bg': (20, 35, 25),
                'primary': (76, 175, 80),
                'secondary': (56, 155, 60),
                'text': (255, 255, 255),
                'accent': (129, 199, 132)
            },
            'orange': {
                'bg': (35, 25, 20),
                'primary': (255, 152, 0),
                'secondary': (245, 124, 0),
                'text': (255, 255, 255),
                'accent': (255, 183, 77)
            },
            'purple': {
                'bg': (30, 25, 40),
                'primary': (156, 39, 176),
                'secondary': (123, 31, 162),
                'text': (255, 255, 255),
                'accent': (186, 104, 200)
            },
            'cyan': {
                'bg': (20, 35, 35),
                'primary': (0, 188, 212),
                'secondary': (0, 172, 193),
                'text': (255, 255, 255),
                'accent': (77, 208, 225)
            }
        }
    
    def get_next_style(self):
        """Obtiene el próximo estilo con distribución uniforme pero aleatoria."""
        import random
        
        self.total_selections += 1
        
        # Calcular cuántas veces debería haber aparecido cada estilo
        expected_count = self.total_selections / len(self.available_styles)
        
        # Encontrar estilos que están por debajo del promedio esperado
        underused_styles = [
            style for style in self.available_styles 
            if (self.usage_count[style] < expected_count and 
                style != self.last_style)
        ]
        
        # Si no hay estilos subutilizados, usar cualquiera excepto el anterior
        if not underused_styles:
            available = [s for s in self.available_styles if s != self.last_style]
            if not available:
                available = self.available_styles
            selected_style = random.choice(available)
        else:
            # Elegir aleatoriamente entre los estilos subutilizados
            selected_style = random.choice(underused_styles)
        
        # Actualizar contadores
        self.usage_count[selected_style] += 1
        self.last_style = selected_style
        
        return selected_style
    
    def get_style_statistics(self):
        """Devuelve estadísticas de uso para debugging."""
        expected = self.total_selections / len(self.available_styles) if self.available_styles else 0
        return {
            'total_selections': self.total_selections,
            'usage_count': self.usage_count.copy(),
            'expected_per_style': expected,
            'variance': {style: count - expected for style, count in self.usage_count.items()}
        }

    def get_random_palette(self):
        """Obtiene una paleta de colores aleatoria."""
        import random
        return random.choice(list(self.color_palettes.values()))


class SlideRenderer:
    """Clase para renderizar slides como imágenes PNG."""
    
    def __init__(self, width: int = 1280, height: int = 720):
        self.width = width
        self.height = height
        
        # Inicializar StyleManager
        self.style_manager = StyleManager()
        
        # Colores base (se actualizarán por slide)
        self.bg_color = (25, 25, 35)
        self.title_color = (255, 255, 255)
        self.bullet_color = (220, 220, 225)
        self.accent_color = (100, 149, 237)
        
    def _get_font(self, size: int) -> ImageFont.ImageFont:
        """Obtiene fuente con fallback a fuente por defecto."""
        try:
            # Intentar fuentes comunes en Linux
            for font_path in [
                "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
                "/usr/share/fonts/TTF/DejaVuSans-Bold.ttf",
                "/System/Library/Fonts/Arial.ttf",  # macOS
                "C:/Windows/Fonts/arial.ttf"  # Windows
            ]:
                if os.path.exists(font_path):
                    return ImageFont.truetype(font_path, size)
        except:
            pass
        # Fallback a fuente por defecto
        return ImageFont.load_default()
    
    # ====== MÉTODOS DE ESTILOS DE DIAPOSITIVAS ======
    
    def _render_minimal_clean(self, draw, title: str, concepts: List[str], palette: dict):
        """Estilo 1: Minimal Clean - Texto centrado con elementos decorativos de fondo."""
        # Elementos decorativos de fondo (formas geométricas sutiles)
        import random
        random.seed(42)  # Para consistencia
        
        # Círculos decorativos de fondo
        for i in range(6):
            x = random.randint(100, self.width - 100)
            y = random.randint(100, self.height - 100)
            radius = random.randint(30, 80)
            # Usar color secondary con baja opacidad visual (círculo grande + pequeño)
            draw.ellipse([x-radius, y-radius, x+radius, y+radius], 
                        outline=palette['secondary'], width=2)
        
        # Rectángulos decorativos en las esquinas
        draw.rectangle([50, 50, 200, 120], outline=palette['accent'], width=3)
        draw.rectangle([self.width-200, self.height-120, self.width-50, self.height-50], 
                      outline=palette['accent'], width=3)
        
        # Título centrado
        title_font = self._get_font(52)
        title_bbox = draw.textbbox((0, 0), title, font=title_font)
        title_width = title_bbox[2] - title_bbox[0]
        title_x = (self.width - title_width) // 2
        title_y = 120
        
        draw.text((title_x, title_y), title, fill=palette['text'], font=title_font)
        
        # Línea decorativa bajo el título
        line_y = title_y + 80
        line_margin = 300
        draw.line([(line_margin, line_y), (self.width - line_margin, line_y)], 
                 fill=palette['primary'], width=4)
        
        # Conceptos centrados verticalmente (acepta cualquier cantidad)
        concept_font = self._get_font(36)
        concept_spacing = 60
        start_y = line_y + 100
        
        # Ajustar espaciado si hay muchos conceptos
        if len(concepts) > 4:
            concept_spacing = min(60, (self.height - start_y - 100) // len(concepts))
        
        for i, concept in enumerate(concepts):
            concept_bbox = draw.textbbox((0, 0), concept, font=concept_font)
            concept_width = concept_bbox[2] - concept_bbox[0]
            concept_x = (self.width - concept_width) // 2
            concept_y = start_y + (i * concept_spacing)
            
            # Bullet point minimalista
            bullet_x = concept_x - 30
            draw.ellipse([bullet_x, concept_y + 12, bullet_x + 8, concept_y + 20], 
                        fill=palette['accent'])
            
            draw.text((concept_x, concept_y), concept, fill=palette['text'], font=concept_font)
    
    def _render_minimal_clean_green(self, draw, title: str, concepts: List[str], palette: dict):
        """Variación Verde de Minimal Clean - Modo oscuro con tonos verdes."""
        green_palette = {
            'bg': (15, 25, 15),
            'primary': (46, 125, 50),
            'secondary': (76, 175, 80),
            'text': (255, 255, 255),
            'accent': (129, 199, 132)
        }
        
        # Reutilizar la lógica del minimal_clean original con nueva paleta
        self._render_minimal_clean_base(draw, title, concepts, green_palette)
    
    def _render_minimal_clean_orange(self, draw, title: str, concepts: List[str], palette: dict):
        """Variación Naranja de Minimal Clean - Modo oscuro con tonos naranjas."""
        orange_palette = {
            'bg': (25, 15, 10),
            'primary': (255, 152, 0),
            'secondary': (255, 183, 77),
            'text': (255, 255, 255),
            'accent': (255, 204, 128)
        }
        
        # Reutilizar la lógica del minimal_clean original con nueva paleta
        self._render_minimal_clean_base(draw, title, concepts, orange_palette)
    
    def _render_minimal_clean_purple(self, draw, title: str, concepts: List[str], palette: dict):
        """Variación Púrpura de Minimal Clean - Modo oscuro con tonos púrpuras."""
        purple_palette = {
            'bg': (20, 15, 25),
            'primary': (156, 39, 176),
            'secondary': (186, 104, 200),
            'text': (255, 255, 255),
            'accent': (206, 147, 216)
        }
        
        # Reutilizar la lógica del minimal_clean original con nueva paleta
        self._render_minimal_clean_base(draw, title, concepts, purple_palette)
    
    def _render_minimal_clean_base(self, draw, title: str, concepts: List[str], palette: dict):
        """Método base para todas las variaciones de minimal_clean."""
        # Elementos decorativos de fondo (formas geométricas sutiles)
        import random
        random.seed(42)  # Para consistencia
        
        # Círculos decorativos de fondo
        for i in range(6):
            x = random.randint(100, self.width - 100)
            y = random.randint(100, self.height - 100)
            radius = random.randint(30, 80)
            # Usar color secondary con baja opacidad visual (círculo grande + pequeño)
            draw.ellipse([x-radius, y-radius, x+radius, y+radius], 
                        outline=palette['secondary'], width=2)
        
        # Rectángulos decorativos en las esquinas
        draw.rectangle([50, 50, 200, 120], outline=palette['accent'], width=3)
        draw.rectangle([self.width-200, self.height-120, self.width-50, self.height-50], 
                      outline=palette['accent'], width=3)
        
        # Título centrado
        title_font = self._get_font(52)
        title_bbox = draw.textbbox((0, 0), title, font=title_font)
        title_width = title_bbox[2] - title_bbox[0]
        title_x = (self.width - title_width) // 2
        title_y = 120
        
        draw.text((title_x, title_y), title, fill=palette['text'], font=title_font)
        
        # Línea decorativa bajo el título
        line_y = title_y + 80
        line_margin = 300
        draw.line([(line_margin, line_y), (self.width - line_margin, line_y)], 
                 fill=palette['primary'], width=4)
        
        # Conceptos centrados verticalmente (acepta cualquier cantidad)
        concept_font = self._get_font(36)
        concept_spacing = 60
        start_y = line_y + 100
        
        # Ajustar espaciado si hay muchos conceptos
        if len(concepts) > 4:
            concept_spacing = min(60, (self.height - start_y - 100) // len(concepts))
        
        for i, concept in enumerate(concepts):
            concept_bbox = draw.textbbox((0, 0), concept, font=concept_font)
            concept_width = concept_bbox[2] - concept_bbox[0]
            concept_x = (self.width - concept_width) // 2
            concept_y = start_y + (i * concept_spacing)
            
            # Bullet point minimalista
            bullet_x = concept_x - 30
            draw.ellipse([bullet_x, concept_y + 12, bullet_x + 8, concept_y + 20], 
                        fill=palette['accent'])
            
            draw.text((concept_x, concept_y), concept, fill=palette['text'], font=concept_font)
    
    def _render_geometric_boxes(self, draw, title: str, concepts: List[str], palette: dict):
        """Estilo 2: Geometric Boxes - Lista flexible con rectángulos decorativos de fondo."""
        # Rectángulos decorativos de fondo
        import random
        random.seed(123)  # Para consistencia diferente al minimal
        
        # Rectángulos decorativos en posiciones aleatorias
        for i in range(8):
            x = random.randint(50, self.width - 200)
            y = random.randint(50, self.height - 100)
            w = random.randint(100, 180)
            h = random.randint(40, 80)
            # Solo bordes para no interferir con el texto
            draw.rectangle([x, y, x + w, y + h], outline=palette['secondary'], width=2)
        
        # Triángulos decorativos en las esquinas
        # Triángulo superior izquierdo
        triangle_points = [(100, 100), (160, 50), (160, 100)]
        draw.polygon(triangle_points, fill=palette['accent'])
        
        # Triángulo inferior derecho
        triangle_points = [(self.width-160, self.height-100), (self.width-100, self.height-100), (self.width-100, self.height-50)]
        draw.polygon(triangle_points, fill=palette['accent'])
        
        # Título en la parte superior
        title_font = self._get_font(48)
        title_bbox = draw.textbbox((0, 0), title, font=title_font)
        title_width = title_bbox[2] - title_bbox[0]
        title_x = (self.width - title_width) // 2
        title_y = 80
        
        draw.text((title_x, title_y), title, fill=palette['text'], font=title_font)
        
        # Lista de conceptos flexible (no limitada por rectángulos)
        concept_font = self._get_font(32)
        start_y = title_y + 120
        concept_spacing = 70
        
        # Ajustar espaciado si hay muchos conceptos
        if len(concepts) > 6:
            concept_spacing = min(70, (self.height - start_y - 100) // len(concepts))
        
        for i, concept in enumerate(concepts):
            concept_y = start_y + (i * concept_spacing)
            
            # Bullet decorativo (rectángulo pequeño)
            bullet_x = 300
            draw.rectangle([bullet_x, concept_y + 8, bullet_x + 20, concept_y + 28], 
                          fill=palette['primary'])
            
            # Texto del concepto
            text_x = bullet_x + 40
            draw.text((text_x, concept_y), concept, fill=palette['text'], font=concept_font)
    
    def _render_circle_network(self, draw, title: str, concepts: List[str], palette: dict):
        """Estilo 3: Circle Network - Ideas en círculos conectados con líneas."""
        import math
        
        # Título en la parte superior
        title_font = self._get_font(48)
        title_bbox = draw.textbbox((0, 0), title, font=title_font)
        title_width = title_bbox[2] - title_bbox[0]
        title_x = (self.width - title_width) // 2
        title_y = 70
        
        draw.text((title_x, title_y), title, fill=palette['text'], font=title_font)
        
        # Círculos distribuidos en un patrón
        concept_font = self._get_font(24)
        circle_radius = 60
        center_x = self.width // 2
        center_y = self.height // 2 + 50
        
        # Posiciones para los círculos (patrón distribuido)
        positions = [
            (center_x, center_y - 120),  # Centro superior
            (center_x - 200, center_y),  # Izquierda
            (center_x + 200, center_y),  # Derecha
            (center_x, center_y + 120),  # Centro inferior
        ]
        
        # Dibujar líneas de conexión primero
        for i in range(len(concepts[:4])):
            for j in range(i + 1, len(concepts[:4])):
                if i < len(positions) and j < len(positions):
                    x1, y1 = positions[i]
                    x2, y2 = positions[j]
                    draw.line([(x1, y1), (x2, y2)], fill=palette['secondary'], width=2)
        
        # Dibujar círculos y texto
        for i, concept in enumerate(concepts[:4]):
            if i < len(positions):
                cx, cy = positions[i]
                
                # Círculo
                draw.ellipse([cx - circle_radius, cy - circle_radius, 
                             cx + circle_radius, cy + circle_radius], 
                            fill=palette['primary'], outline=palette['accent'], width=3)
                
                # Texto centrado en el círculo
                text_bbox = draw.textbbox((0, 0), concept, font=concept_font)
                text_width = text_bbox[2] - text_bbox[0]
                text_height = text_bbox[3] - text_bbox[1]
                
                text_x = cx - text_width // 2
                text_y = cy - text_height // 2
                
                draw.text((text_x, text_y), concept, fill=palette['text'], font=concept_font)
    
    def _render_split_screen(self, draw, title: str, concepts: List[str], palette: dict):
        """Estilo 4: Split Screen - Título a un lado, conceptos en formas al otro."""
        # Dividir pantalla verticalmente
        split_x = self.width // 2
        
        # Título en la mitad izquierda
        title_font = self._get_font(42)
        title_lines = []
        words = title.split()
        current_line = ""
        
        # Dividir título en líneas para que quepa en media pantalla
        for word in words:
            test_line = current_line + " " + word if current_line else word
            bbox = draw.textbbox((0, 0), test_line, font=title_font)
            if bbox[2] - bbox[0] < split_x - 80:
                current_line = test_line
            else:
                if current_line:
                    title_lines.append(current_line)
                current_line = word
        if current_line:
            title_lines.append(current_line)
        
        # Renderizar título centrado en la mitad izquierda
        title_start_y = (self.height - len(title_lines) * 60) // 2
        for i, line in enumerate(title_lines):
            bbox = draw.textbbox((0, 0), line, font=title_font)
            line_width = bbox[2] - bbox[0]
            title_x = (split_x - line_width) // 2
            title_y = title_start_y + i * 60
            draw.text((title_x, title_y), line, fill=palette['text'], font=title_font)
        
        # Línea divisoria
        draw.line([(split_x, 50), (split_x, self.height - 50)], 
                 fill=palette['primary'], width=4)
        
        # Conceptos en la mitad derecha como hexágonos
        concept_font = self._get_font(26)
        hex_size = 70
        start_x = split_x + 150
        start_y = 150
        spacing = 140
        
        for i, concept in enumerate(concepts[:3]):
            hex_x = start_x
            hex_y = start_y + i * spacing
            
            # Dibujar hexágono (simulado con rectángulo con esquinas cortadas)
            points = [
                (hex_x - hex_size, hex_y),
                (hex_x - hex_size//2, hex_y - hex_size//2),
                (hex_x + hex_size//2, hex_y - hex_size//2),
                (hex_x + hex_size, hex_y),
                (hex_x + hex_size//2, hex_y + hex_size//2),
                (hex_x - hex_size//2, hex_y + hex_size//2)
            ]
            draw.polygon(points, fill=palette['primary'], outline=palette['accent'])
            
            # Texto centrado en el hexágono
            text_bbox = draw.textbbox((0, 0), concept, font=concept_font)
            text_width = text_bbox[2] - text_bbox[0]
            text_height = text_bbox[3] - text_bbox[1]
            
            text_x = hex_x - text_width // 2
            text_y = hex_y - text_height // 2
            
            draw.text((text_x, text_y), concept, fill=palette['text'], font=concept_font)
    
    def _render_timeline_flow(self, draw, title: str, concepts: List[str], palette: dict):
        """Estilo 5: Timeline Flow - Conceptos en secuencia horizontal con conectores."""
        # Título centrado arriba
        title_font = self._get_font(48)
        title_bbox = draw.textbbox((0, 0), title, font=title_font)
        title_width = title_bbox[2] - title_bbox[0]
        title_x = (self.width - title_width) // 2
        title_y = 80
        
        draw.text((title_x, title_y), title, fill=palette['text'], font=title_font)
        
        # Timeline horizontal
        timeline_y = self.height // 2
        timeline_start = 100
        timeline_end = self.width - 100
        
        # Línea base del timeline
        draw.line([(timeline_start, timeline_y), (timeline_end, timeline_y)], 
                 fill=palette['secondary'], width=6)
        
        # Distribuir conceptos a lo largo del timeline
        concept_font = self._get_font(24)
        num_concepts = min(len(concepts), 4)
        if num_concepts > 1:
            spacing = (timeline_end - timeline_start) / (num_concepts - 1)
        else:
            spacing = 0
            
        for i, concept in enumerate(concepts[:4]):
            if num_concepts == 1:
                concept_x = (timeline_start + timeline_end) // 2
            else:
                concept_x = timeline_start + i * spacing
            
            # Círculo en el timeline
            circle_radius = 25
            draw.ellipse([concept_x - circle_radius, timeline_y - circle_radius,
                         concept_x + circle_radius, timeline_y + circle_radius],
                        fill=palette['primary'], outline=palette['accent'], width=3)
            
            # Número en el círculo
            num_font = self._get_font(20)
            num_text = str(i + 1)
            num_bbox = draw.textbbox((0, 0), num_text, font=num_font)
            num_width = num_bbox[2] - num_bbox[0]
            num_height = num_bbox[3] - num_bbox[1]
            
            num_x = concept_x - num_width // 2
            num_y = timeline_y - num_height // 2
            
            draw.text((num_x, num_y), num_text, fill=palette['text'], font=num_font)
            
            # Concepto debajo del círculo
            text_bbox = draw.textbbox((0, 0), concept, font=concept_font)
            text_width = text_bbox[2] - text_bbox[0]
            
            text_x = concept_x - text_width // 2
            text_y = timeline_y + 50
            
            draw.text((text_x, text_y), concept, fill=palette['text'], font=concept_font)
            
            # Flecha hacia el siguiente (excepto el último)
            if i < num_concepts - 1 and num_concepts > 1:
                arrow_start = concept_x + circle_radius + 10
                arrow_end = concept_x + spacing - circle_radius - 10
                arrow_y = timeline_y
                
                # Línea de flecha
                draw.line([(arrow_start, arrow_y), (arrow_end, arrow_y)], 
                         fill=palette['accent'], width=3)
                
                # Punta de flecha
                arrow_points = [
                    (arrow_end, arrow_y),
                    (arrow_end - 15, arrow_y - 8),
                    (arrow_end - 15, arrow_y + 8)
                ]
                draw.polygon(arrow_points, fill=palette['accent'])
    
    def _render_grid_layout(self, draw, title: str, concepts: List[str], palette: dict):
        """Estilo 6: Grid Layout - Conceptos en cuadrícula de formas geométricas."""
        # Título arriba
        title_font = self._get_font(48)
        title_bbox = draw.textbbox((0, 0), title, font=title_font)
        title_width = title_bbox[2] - title_bbox[0]
        title_x = (self.width - title_width) // 2
        title_y = 70
        
        draw.text((title_x, title_y), title, fill=palette['text'], font=title_font)
        
        # Grid 2x2 de formas
        concept_font = self._get_font(26)
        grid_size = 200
        spacing = 40
        start_x = (self.width - (2 * grid_size + spacing)) // 2
        start_y = title_y + 120
        
        # Formas alternativas para variedad
        shapes = ['circle', 'square', 'diamond', 'triangle']
        
        for i, concept in enumerate(concepts[:4]):
            row = i // 2
            col = i % 2
            
            center_x = start_x + col * (grid_size + spacing) + grid_size // 2
            center_y = start_y + row * (grid_size + spacing) + grid_size // 2
            
            shape = shapes[i % len(shapes)]
            
            if shape == 'circle':
                radius = grid_size // 3
                draw.ellipse([center_x - radius, center_y - radius,
                             center_x + radius, center_y + radius],
                            fill=palette['primary'], outline=palette['accent'], width=3)
            
            elif shape == 'square':
                size = grid_size // 2
                draw.rectangle([center_x - size//2, center_y - size//2,
                               center_x + size//2, center_y + size//2],
                              fill=palette['primary'], outline=palette['accent'], width=3)
            
            elif shape == 'diamond':
                size = grid_size // 3
                points = [
                    (center_x, center_y - size),
                    (center_x + size, center_y),
                    (center_x, center_y + size),
                    (center_x - size, center_y)
                ]
                draw.polygon(points, fill=palette['primary'], outline=palette['accent'])
            
            elif shape == 'triangle':
                size = grid_size // 3
                points = [
                    (center_x, center_y - size),
                    (center_x - size, center_y + size//2),
                    (center_x + size, center_y + size//2)
                ]
                draw.polygon(points, fill=palette['primary'], outline=palette['accent'])
            
            # Texto centrado
            text_bbox = draw.textbbox((0, 0), concept, font=concept_font)
            text_width = text_bbox[2] - text_bbox[0]
            text_height = text_bbox[3] - text_bbox[1]
            
            text_x = center_x - text_width // 2
            text_y = center_y - text_height // 2
            
            draw.text((text_x, text_y), concept, fill=palette['text'], font=concept_font)
    
    def _render_hierarchy_tree(self, draw, title: str, concepts: List[str], palette: dict):
        """Estilo 7: Hierarchy Tree - Concepto principal arriba, secundarios abajo."""
        # Título como concepto principal en la parte superior
        title_font = self._get_font(40)
        title_box_width = 300
        title_box_height = 80
        title_x = (self.width - title_box_width) // 2
        title_y = 100
        
        # Caja del título principal
        draw.rectangle([title_x, title_y, title_x + title_box_width, title_y + title_box_height],
                      fill=palette['primary'], outline=palette['accent'], width=4)
        
        # Texto del título centrado
        title_bbox = draw.textbbox((0, 0), title, font=title_font)
        title_text_width = title_bbox[2] - title_bbox[0]
        title_text_height = title_bbox[3] - title_bbox[1]
        
        title_text_x = title_x + (title_box_width - title_text_width) // 2
        title_text_y = title_y + (title_box_height - title_text_height) // 2
        
        draw.text((title_text_x, title_text_y), title, fill=palette['text'], font=title_font)
        
        # Conceptos secundarios distribuidos abajo
        concept_font = self._get_font(28)
        box_width = 180
        box_height = 60
        spacing = 40
        
        num_concepts = min(len(concepts), 3)
        if num_concepts > 0:
            total_width = num_concepts * box_width + (num_concepts - 1) * spacing
            start_x = (self.width - total_width) // 2
            start_y = title_y + title_box_height + 120
            
            # Líneas de conexión desde el título a cada concepto
            title_center_x = title_x + title_box_width // 2
            title_bottom_y = title_y + title_box_height
            
            for i, concept in enumerate(concepts[:3]):
                concept_x = start_x + i * (box_width + spacing)
                concept_center_x = concept_x + box_width // 2
                concept_top_y = start_y
                
                # Línea de conexión
                draw.line([(title_center_x, title_bottom_y), (title_center_x, title_bottom_y + 60)],
                         fill=palette['secondary'], width=3)
                draw.line([(title_center_x, title_bottom_y + 60), (concept_center_x, title_bottom_y + 60)],
                         fill=palette['secondary'], width=3)
                draw.line([(concept_center_x, title_bottom_y + 60), (concept_center_x, concept_top_y)],
                         fill=palette['secondary'], width=3)
                
                # Caja del concepto
                draw.rectangle([concept_x, start_y, concept_x + box_width, start_y + box_height],
                              fill=palette['secondary'], outline=palette['accent'], width=2)
                
                # Texto del concepto
                text_bbox = draw.textbbox((0, 0), concept, font=concept_font)
                text_width = text_bbox[2] - text_bbox[0]
                text_height = text_bbox[3] - text_bbox[1]
                
                text_x = concept_x + (box_width - text_width) // 2
                text_y = start_y + (box_height - text_height) // 2
                
                draw.text((text_x, text_y), concept, fill=palette['text'], font=concept_font)
    
    def _render_floating_elements(self, draw, title: str, concepts: List[str], palette: Dict[str, str]) -> None:
        """Estilo 8: Elementos flotantes distribuidos de forma orgánica."""
        # Título centrado en la parte superior
        title_font = self._get_font(44)
        title_bbox = draw.textbbox((0, 0), title, font=title_font)
        title_x = (self.width - title_bbox[2]) // 2
        title_y = 80
        draw.text((title_x, title_y), title, fill=palette['text'], font=title_font)
        
        # Crear "burbujas" flotantes con conceptos
        import random
        random.seed(42)  # Para resultados consistentes
        
        concept_font = self._get_font(28)
        available_area = {
            'x_min': 100, 'x_max': self.width - 100,
            'y_min': title_y + 120, 'y_max': self.height - 100
        }
        
        # Distribuir conceptos en posiciones "flotantes"
        for i, concept in enumerate(concepts[:6]):  # Máximo 6 elementos
            # Posición pseudo-aleatoria pero balanceada
            x = available_area['x_min'] + (i % 3) * (available_area['x_max'] - available_area['x_min']) // 3
            y = available_area['y_min'] + (i // 3) * (available_area['y_max'] - available_area['y_min']) // 2
            
            # Agregar variación aleatoria
            x += random.randint(-80, 80)
            y += random.randint(-60, 60)
            
            # Asegurar que esté dentro de límites
            x = max(120, min(x, self.width - 250))
            y = max(available_area['y_min'], min(y, available_area['y_max'] - 80))
            
            # Dibujar círculo con gradiente visual (círculo doble)
            radius = 60
            # Círculo exterior (sombra)
            draw.ellipse([x-radius-2, y-radius-2, x+radius+2, y+radius+2], 
                        fill=palette['secondary'])
            # Círculo principal
            draw.ellipse([x-radius, y-radius, x+radius, y+radius], 
                        fill=palette['primary'])
            
            # Texto centrado en el círculo
            text_bbox = draw.textbbox((0, 0), concept, font=concept_font)
            text_x = x - text_bbox[2] // 2
            text_y = y - text_bbox[3] // 2
            draw.text((text_x, text_y), concept, fill=palette['text'], font=concept_font)
            
            # Líneas sutiles conectando elementos cercanos
            if i > 0:
                prev_x = available_area['x_min'] + ((i-1) % 3) * (available_area['x_max'] - available_area['x_min']) // 3
                prev_y = available_area['y_min'] + ((i-1) // 3) * (available_area['y_max'] - available_area['y_min']) // 2
                prev_x += random.randint(-80, 80) if i > 1 else 0
                prev_y += random.randint(-60, 60) if i > 1 else 0
                
                # Línea sutil conectora
                draw.line([prev_x, prev_y, x, y], fill=palette['accent'], width=2)

    def _render_banner_style(self, draw, title: str, concepts: List[str], palette: Dict[str, str]) -> None:
        """Estilo 9: Diseño tipo banner con franjas horizontales."""
        # Título en banner superior
        banner_height = 120
        draw.rectangle([0, 0, self.width, banner_height], fill=palette['primary'])
        
        title_font = self._get_font(44)
        title_bbox = draw.textbbox((0, 0), title, font=title_font)
        title_x = 50
        title_y = (banner_height - title_bbox[3]) // 2
        draw.text((title_x, title_y), title, fill=palette['text'], font=title_font)
        
        # Conceptos en franjas intercaladas
        concept_font = self._get_font(32)
        content_start_y = banner_height + 40
        available_height = self.height - content_start_y - 40
        
        stripe_height = min(available_height // len(concepts), 140) if concepts else 140
        
        for i, concept in enumerate(concepts):
            y_start = content_start_y + i * (stripe_height + 20)
            y_end = y_start + stripe_height
            
            # Alternar lados y colores
            if i % 2 == 0:
                # Franja desde la izquierda
                stripe_width = self.width * 0.7
                draw.rectangle([0, y_start, stripe_width, y_end], fill=palette['secondary'])
                
                # Triángulo decorativo en el extremo
                triangle_points = [
                    (stripe_width, y_start),
                    (stripe_width + 50, (y_start + y_end) // 2),
                    (stripe_width, y_end)
                ]
                draw.polygon(triangle_points, fill=palette['secondary'])
                
                # Texto alineado a la izquierda
                text_x = 40
            else:
                # Franja desde la derecha
                stripe_width = self.width * 0.7
                x_start = self.width - stripe_width
                draw.rectangle([x_start, y_start, self.width, y_end], fill=palette['accent'])
                
                # Triángulo decorativo en el extremo
                triangle_points = [
                    (x_start, y_start),
                    (x_start - 50, (y_start + y_end) // 2),
                    (x_start, y_end)
                ]
                draw.polygon(triangle_points, fill=palette['accent'])
                
                # Texto alineado a la derecha
                text_bbox = draw.textbbox((0, 0), concept, font=concept_font)
                text_x = self.width - text_bbox[2] - 40
            
            # Dibujar texto centrado verticalmente en la franja
            text_y = (y_start + y_end - draw.textbbox((0, 0), concept, font=concept_font)[3]) // 2
            draw.text((text_x, text_y), concept, fill=palette['text'], font=concept_font)

    def _render_banner_style_green(self, draw, title: str, concepts: List[str], palette: Dict[str, str]) -> None:
        """Variación Verde de Banner Style - Modo oscuro con tonos verdes."""
        green_palette = {
            'bg': (15, 25, 15),
            'primary': (46, 125, 50),
            'secondary': (76, 175, 80),
            'text': (255, 255, 255),
            'accent': (129, 199, 132)
        }
        
        # Reutilizar la lógica del banner_style original con nueva paleta
        self._render_banner_style_base(draw, title, concepts, green_palette)
    
    def _render_banner_style_orange(self, draw, title: str, concepts: List[str], palette: Dict[str, str]) -> None:
        """Variación Naranja de Banner Style - Modo oscuro con tonos naranjas."""
        orange_palette = {
            'bg': (25, 15, 10),
            'primary': (255, 152, 0),
            'secondary': (255, 183, 77),
            'text': (255, 255, 255),
            'accent': (255, 204, 128)
        }
        
        # Reutilizar la lógica del banner_style original con nueva paleta
        self._render_banner_style_base(draw, title, concepts, orange_palette)
    
    def _render_banner_style_purple(self, draw, title: str, concepts: List[str], palette: Dict[str, str]) -> None:
        """Variación Púrpura de Banner Style - Modo oscuro con tonos púrpuras."""
        purple_palette = {
            'bg': (20, 15, 25),
            'primary': (156, 39, 176),
            'secondary': (186, 104, 200),
            'text': (255, 255, 255),
            'accent': (206, 147, 216)
        }
        
        # Reutilizar la lógica del banner_style original con nueva paleta
        self._render_banner_style_base(draw, title, concepts, purple_palette)
    
    def _render_banner_style_base(self, draw, title: str, concepts: List[str], palette: Dict[str, str]) -> None:
        """Método base para todas las variaciones de banner_style."""
        # Título en banner superior
        banner_height = 120
        draw.rectangle([0, 0, self.width, banner_height], fill=palette['primary'])
        
        title_font = self._get_font(44)
        title_bbox = draw.textbbox((0, 0), title, font=title_font)
        title_x = 50
        title_y = (banner_height - title_bbox[3]) // 2
        draw.text((title_x, title_y), title, fill=palette['text'], font=title_font)
        
        # Conceptos en franjas intercaladas
        concept_font = self._get_font(32)
        content_start_y = banner_height + 40
        available_height = self.height - content_start_y - 40
        
        stripe_height = min(available_height // len(concepts), 140) if concepts else 140
        
        for i, concept in enumerate(concepts):
            y_start = content_start_y + i * (stripe_height + 20)
            y_end = y_start + stripe_height
            
            # Alternar lados y colores
            if i % 2 == 0:
                # Franja desde la izquierda
                stripe_width = self.width * 0.7
                draw.rectangle([0, y_start, stripe_width, y_end], fill=palette['secondary'])
                
                # Triángulo decorativo en el extremo
                triangle_points = [
                    (stripe_width, y_start),
                    (stripe_width + 50, (y_start + y_end) // 2),
                    (stripe_width, y_end)
                ]
                draw.polygon(triangle_points, fill=palette['secondary'])
                
                # Texto alineado a la izquierda
                text_x = 40
            else:
                # Franja desde la derecha
                stripe_width = self.width * 0.7
                x_start = self.width - stripe_width
                draw.rectangle([x_start, y_start, self.width, y_end], fill=palette['accent'])
                
                # Triángulo decorativo en el extremo
                triangle_points = [
                    (x_start, y_start),
                    (x_start - 50, (y_start + y_end) // 2),
                    (x_start, y_end)
                ]
                draw.polygon(triangle_points, fill=palette['accent'])
                
                # Texto alineado a la derecha
                text_bbox = draw.textbbox((0, 0), concept, font=concept_font)
                text_x = self.width - text_bbox[2] - 40
            
            # Dibujar texto centrado verticalmente en la franja
            text_y = (y_start + y_end - draw.textbbox((0, 0), concept, font=concept_font)[3]) // 2
            draw.text((text_x, text_y), concept, fill=palette['text'], font=concept_font)

    def _render_focus_spotlight(self, draw, title: str, concepts: List[str], palette: Dict[str, str]) -> None:
        """Estilo 10: Un concepto principal en spotlight con secundarios alrededor."""
        # Título en la parte superior
        title_font = self._get_font(44)
        title_bbox = draw.textbbox((0, 0), title, font=title_font)
        title_x = (self.width - title_bbox[2]) // 2
        title_y = 60
        draw.text((title_x, title_y), title, fill=palette['text'], font=title_font)
        
        if not concepts:
            return
            
        # Concepto principal en el centro (spotlight)
        main_concept = concepts[0]
        secondary_concepts = concepts[1:6]  # Máximo 5 secundarios
        
        # Círculo principal grande en el centro
        center_x, center_y = self.width // 2, (self.height + title_y + 100) // 2
        main_radius = 120
        
        # Efecto de spotlight (círculos concéntricos)
        for radius_offset in [30, 20, 10, 0]:
            alpha = 100 - radius_offset * 2  # Efecto de transparencia simulado
            color = palette['primary'] if radius_offset == 0 else palette['secondary']
            draw.ellipse([
                center_x - main_radius - radius_offset,
                center_y - main_radius - radius_offset,
                center_x + main_radius + radius_offset,
                center_y + main_radius + radius_offset
            ], fill=color)
        
        # Texto del concepto principal
        main_font = self._get_font(36)
        main_bbox = draw.textbbox((0, 0), main_concept, font=main_font)
        main_x = center_x - main_bbox[2] // 2
        main_y = center_y - main_bbox[3] // 2
        draw.text((main_x, main_y), main_concept, fill=palette['text'], font=main_font)
        
        # Conceptos secundarios alrededor del principal
        secondary_font = self._get_font(24)
        orbit_radius = 250
        
        import math
        for i, concept in enumerate(secondary_concepts):
            # Distribución circular alrededor del concepto principal
            angle = (2 * math.pi * i) / len(secondary_concepts)
            sec_x = center_x + orbit_radius * math.cos(angle)
            sec_y = center_y + orbit_radius * math.sin(angle)
            
            # Círculo secundario
            sec_radius = 50
            draw.ellipse([
                sec_x - sec_radius, sec_y - sec_radius,
                sec_x + sec_radius, sec_y + sec_radius
            ], fill=palette['accent'])
            
            # Texto del concepto secundario
            sec_bbox = draw.textbbox((0, 0), concept, font=secondary_font)
            text_x = sec_x - sec_bbox[2] // 2
            text_y = sec_y - sec_bbox[3] // 2
            draw.text((text_x, text_y), concept, fill=palette['text'], font=secondary_font)
            
            # Línea conectora al concepto principal
            draw.line([center_x, center_y, sec_x, sec_y], fill=palette['secondary'], width=3)
    
    def render_slide(self, slide: Dict[str, Any], slide_num: int, output_path: str) -> None:
        """
        Renderiza una slide como imagen PNG usando estilos dinámicos.
        
        Args:
            slide: Diccionario con datos de la slide
            slide_num: Número de slide para logging
            output_path: Ruta donde guardar la imagen
        """
        # Extraer título y conceptos
        title = slide.get('titulo', f'Slide {slide_num}')
        concepts = slide.get('puntos', [])
        
        # Seleccionar estilo aleatorio 
        style = self.style_manager.get_next_style()
        palette = self.style_manager.get_random_palette()
        
        # Crear imagen con color de fondo de la paleta
        img = Image.new('RGB', (self.width, self.height), palette['bg'])
        draw = ImageDraw.Draw(img)
        
        # Renderizar según el estilo seleccionado (solo estilos universales)
        if style == 'minimal_clean':
            self._render_minimal_clean(draw, title, concepts, palette)
        elif style == 'minimal_clean_green':
            self._render_minimal_clean_green(draw, title, concepts, palette)
        elif style == 'minimal_clean_orange':
            self._render_minimal_clean_orange(draw, title, concepts, palette)
        elif style == 'minimal_clean_purple':
            self._render_minimal_clean_purple(draw, title, concepts, palette)
        elif style == 'geometric_boxes':
            self._render_geometric_boxes(draw, title, concepts, palette)
        elif style == 'banner_style':
            self._render_banner_style(draw, title, concepts, palette)
        elif style == 'banner_style_green':
            self._render_banner_style_green(draw, title, concepts, palette)
        elif style == 'banner_style_orange':
            self._render_banner_style_orange(draw, title, concepts, palette)
        elif style == 'banner_style_purple':
            self._render_banner_style_purple(draw, title, concepts, palette)
        else:
            # Fallback al estilo minimal si no está implementado
            self._render_minimal_clean(draw, title, concepts, palette)
        
        # Modificar el nombre del archivo para incluir el estilo
        path_parts = os.path.splitext(output_path)
        new_output_path = f"{path_parts[0]}_{style}{path_parts[1]}"
        
        # Guardar imagen
        img.save(new_output_path, 'PNG')
        print(f"  Slide {slide_num:04d} renderizada ({style}): {os.path.basename(new_output_path)}")
        
        # Retornar la nueva ruta para actualizar la referencia
        return new_output_path
    
    def _fit_text_to_width(self, text: str, max_width: int, max_font_size: int = 48, min_font_size: int = 16) -> Tuple[ImageFont.ImageFont, List[str]]:
        """
        Ajusta el tamaño de fuente y divide el texto para que quepa en el ancho especificado.
        
        Args:
            text: Texto a ajustar
            max_width: Ancho máximo disponible
            max_font_size: Tamaño máximo de fuente
            min_font_size: Tamaño mínimo de fuente
            
        Returns:
            Tuple con (fuente ajustada, lista de líneas de texto)
        """
        # Comenzar con el tamaño máximo e ir reduciendo
        for font_size in range(max_font_size, min_font_size - 1, -2):
            font = self._get_font(font_size)
            
            # Intentar primero como una sola línea
            bbox = font.getbbox(text)
            text_width = bbox[2] - bbox[0]
            
            if text_width <= max_width:
                return font, [text]
            
            # Si no cabe en una línea, intentar dividir en múltiples líneas
            words = text.split()
            lines = []
            current_line = []
            
            for word in words:
                test_line = ' '.join(current_line + [word])
                test_bbox = font.getbbox(test_line)
                test_width = test_bbox[2] - test_bbox[0]
                
                if test_width <= max_width:
                    current_line.append(word)
                else:
                    if current_line:
                        lines.append(' '.join(current_line))
                        current_line = [word]
                    else:
                        # Palabra muy larga, forzar división
                        lines.append(word)
            
            if current_line:
                lines.append(' '.join(current_line))
            
            # Verificar que todas las líneas quepan (máximo 2 líneas para títulos largos)
            max_title_lines = 2 if len(text) > 50 else 3
            if len(lines) <= max_title_lines:
                all_fit = True
                for line in lines:
                    line_bbox = font.getbbox(line)
                    line_width = line_bbox[2] - line_bbox[0]
                    if line_width > max_width:
                        all_fit = False
                        break
                
                if all_fit:
                    return font, lines
        
        # Si llegamos aquí, usar el tamaño mínimo y forzar división
        font = self._get_font(min_font_size)
        lines = self._wrap_text(text, font, max_width)
        max_lines = 2 if len(text) > 50 else 3
        return font, lines[:max_lines]  # Limitar líneas según longitud del texto

    def _wrap_text(self, text: str, font: ImageFont.ImageFont, max_width: int) -> List[str]:
        """Envuelve texto para que no exceda el ancho máximo."""
        words = text.split()
        lines = []
        current_line = []
        
        for word in words:
            test_line = ' '.join(current_line + [word])
            bbox = font.getbbox(test_line)
            width = bbox[2] - bbox[0]
            
            if width <= max_width:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                    current_line = [word]
                else:
                    lines.append(word)  # Palabra muy larga
        
        if current_line:
            lines.append(' '.join(current_line))
        
        return lines


class JSONExtractor:
    """Clase para extraer y limpiar JSON desde texto ruidoso."""
    
    @staticmethod
    def extract_json_from_text(raw_text: str) -> List[Dict[str, Any]]:
        """
        Extrae JSON desde texto que puede contener ruido de LLM.
        Maneja múltiples arrays JSON fragmentados y los combina automáticamente.
        
        Args:
            raw_text: Texto crudo que puede contener JSON
            
        Returns:
            Lista de slides parseadas
            
        Raises:
            VideoGeneratorError: Si no se puede extraer JSON válido
        """
        print("Extrayendo JSON desde texto...")
        
        # Paso 1: Buscar y extraer TODOS los arrays JSON del texto
        all_slides = []
        
        # Buscar múltiples arrays JSON usando regex
        array_pattern = r'\[\s*\{.*?\}\s*\]'
        array_matches = re.findall(array_pattern, raw_text, re.DOTALL)
        
        print(f"Encontrados {len(array_matches)} arrays JSON potenciales")
        
        for i, match in enumerate(array_matches):
            try:
                # Limpiar cada array encontrado
                cleaned_json = JSONExtractor._clean_json_text(match)
                parsed = json.loads(cleaned_json)
                
                if isinstance(parsed, list):
                    print(f"  Array {i+1}: {len(parsed)} slides extraídas")
                    all_slides.extend(parsed)
                elif isinstance(parsed, dict):
                    print(f"  Array {i+1}: 1 slide extraída (objeto único)")
                    all_slides.append(parsed)
                    
            except json.JSONDecodeError as e:
                print(f"  Array {i+1}: Error parseando - {e}")
                continue
        
        # Si encontramos slides, retornarlas
        if all_slides:
            print(f"Total de slides combinadas: {len(all_slides)}")
            return all_slides
        
        # Fallback: Método original (para compatibilidad con formato único)
        print("Fallback: Intentando método de extracción original...")
        return JSONExtractor._extract_single_json(raw_text)
    
    @staticmethod
    def _extract_single_json(raw_text: str) -> List[Dict[str, Any]]:
        """Método original de extracción para un solo JSON."""
        # Paso 1: Buscar primer '[' o '{'
        start_idx = -1
        for i, char in enumerate(raw_text):
            if char in '[{':
                start_idx = i
                break
        
        if start_idx == -1:
            # No hay JSON, intentar parsear bloques de texto
            return JSONExtractor._parse_markdown_blocks(raw_text)
        
        # Paso 2: Balanceo de paréntesis/corchetes/llaves
        substring = raw_text[start_idx:]
        stack = []
        end_idx = -1
        
        for i, char in enumerate(substring):
            if char in '[{(':
                stack.append(char)
            elif char in ']})':
                if not stack:
                    continue
                last = stack.pop()
                # Verificar matching
                if ((char == ']' and last == '[') or 
                    (char == '}' and last == '{') or 
                    (char == ')' and last == '(')):
                    if not stack:  # Stack vacío = cierre completo
                        end_idx = i + 1
                        break
        
        if end_idx == -1:
            raise VideoGeneratorError("No se encontró JSON balanceado en el texto")
        
        json_text = substring[:end_idx]
        cleaned_json = JSONExtractor._clean_json_text(json_text)
        
        # Intentar parsear
        try:
            parsed = json.loads(cleaned_json)
            if isinstance(parsed, list):
                return parsed
            elif isinstance(parsed, dict):
                return [parsed]  # Convertir objeto único a lista
            else:
                raise VideoGeneratorError(f"JSON parseado no es lista ni objeto: {type(parsed)}")
        except json.JSONDecodeError as e:
            print(f"Error parseando JSON limpio: {e}")
            # Intentar extraer múltiples objetos con regex
            return JSONExtractor._extract_multiple_objects(cleaned_json, raw_text)
    
    @staticmethod
    def _clean_json_text(json_text: str) -> str:
        """Limpia texto JSON de caracteres problemáticos."""
        # Limpiar comillas tipográficas
        json_text = json_text.replace('"', '"').replace('"', '"')
        json_text = json_text.replace(''', "'").replace(''', "'")
        
        # Eliminar comas finales
        json_text = re.sub(r',(\s*[}\]])', r'\1', json_text)
        
        return json_text
    
    @staticmethod
    def _extract_multiple_objects(json_text: str, raw_text: str) -> List[Dict[str, Any]]:
        """Intenta extraer múltiples objetos JSON con regex."""
        print("Intentando extraer múltiples objetos JSON...")
        
        objects = []
        
        # Buscar objetos {...}
        object_pattern = r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}'
        matches = re.findall(object_pattern, json_text, re.DOTALL)
        
        for match in matches:
            try:
                clean_match = JSONExtractor._clean_json_text(match)
                obj = json.loads(clean_match)
                if isinstance(obj, dict):
                    objects.append(obj)
            except json.JSONDecodeError:
                continue
        
        if objects:
            return objects
        
        # Si aún falla, intentar parsear bloques de texto
        return JSONExtractor._parse_markdown_blocks(raw_text)
    
    @staticmethod
    def _parse_markdown_blocks(text: str) -> List[Dict[str, Any]]:
        """
        Parsea bloques de texto formato [HH:MM - HH:MM] como fallback.
        
        Args:
            text: Texto con bloques formato markdown
            
        Returns:
            Lista de slides parseadas
        """
        print("Parseando bloques de texto como fallback...")
        
        slides = []
        
        # Pattern para bloques [HH:MM - HH:MM] o [HH:MM:SS - HH:MM:SS]
        time_pattern = r'\[(\d{1,2}:\d{2}(?::\d{2})?)\s*-\s*(\d{1,2}:\d{2}(?::\d{2})?)\]'
        
        blocks = re.split(time_pattern, text)
        
        # blocks será: [texto_antes, inicio1, fin1, contenido1, inicio2, fin2, contenido2, ...]
        for i in range(1, len(blocks), 3):
            if i + 2 < len(blocks):
                inicio = blocks[i]
                fin = blocks[i + 1]
                contenido = blocks[i + 2].strip()
                
                # Parsear contenido del bloque
                lines = [line.strip() for line in contenido.split('\n') if line.strip()]
                
                titulo = "Sin título"
                puntos = []
                
                for line in lines:
                    if line.startswith('Título:') or line.startswith('**'):
                        titulo = line.replace('Título:', '').replace('**', '').strip()
                    elif line.startswith('-') or line.startswith('•'):
                        puntos.append(line[1:].strip())
                
                if not puntos and lines:
                    # Si no hay bullets, usar todas las líneas como puntos
                    puntos = lines[1:] if titulo != "Sin título" else lines
                
                slides.append({
                    "inicio": inicio,
                    "fin": fin,
                    "titulo": titulo,
                    "puntos": puntos
                })
        
        if not slides:
            raise VideoGeneratorError("No se pudieron extraer slides del texto")
        
        return slides


class TimeUtils:
    """Utilidades para manejo de tiempo."""
    
    @staticmethod
    def time_to_seconds(time_str: str) -> float:
        """Convierte tiempo HH:MM o HH:MM:SS a segundos."""
        parts = time_str.split(':')
        if len(parts) == 2:  # MM:SS
            return int(parts[0]) * 60 + int(parts[1])
        elif len(parts) == 3:  # HH:MM:SS
            return int(parts[0]) * 3600 + int(parts[1]) * 60 + int(parts[2])
        else:
            raise ValueError(f"Formato de tiempo inválido: {time_str}")
    
    @staticmethod
    def validate_slide_times(slides: List[Dict[str, Any]]) -> None:
        """Valida que los tiempos de las slides sean consistentes."""
        for i, slide in enumerate(slides):
            inicio_sec = TimeUtils.time_to_seconds(slide['inicio'])
            fin_sec = TimeUtils.time_to_seconds(slide['fin'])
            
            if fin_sec <= inicio_sec:
                raise VideoGeneratorError(
                    f"Slide {i+1}: tiempo de fin ({slide['fin']}) debe ser mayor que inicio ({slide['inicio']})")
            
            # Verificar solapamiento con slide anterior
            if i > 0:
                prev_fin = TimeUtils.time_to_seconds(slides[i-1]['fin'])
                if inicio_sec < prev_fin:
                    print(f"WARNING: Slide {i+1} se solapa con slide anterior")


class VideoGenerator:
    """Clase principal para generar videos desde slides."""
    
    def __init__(self, input_txt_path: str, audio_path: str, output_video_path: str):
        self.input_txt_path = os.path.abspath(input_txt_path)
        self.audio_path = os.path.abspath(audio_path)
        self.output_video_path = os.path.abspath(output_video_path)
        
        # Crear directorio de trabajo temporal en el mismo directorio que el video de salida
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_dir = os.path.dirname(self.output_video_path)
        self.job_dir = os.path.join(output_dir, f"job_{timestamp}")
        os.makedirs(self.job_dir, exist_ok=True)
        
        self.renderer = SlideRenderer()
        
        print(f"Directorio de trabajo: {self.job_dir}")
    
    def validate_inputs(self) -> None:
        """Valida que los archivos de entrada existan."""
        if not os.path.exists(self.input_txt_path):
            raise VideoGeneratorError(f"Archivo de texto no encontrado: {self.input_txt_path}")
        
        if not os.path.exists(self.audio_path):
            raise VideoGeneratorError(f"Archivo de audio no encontrado: {self.audio_path}")
        
        # Verificar que ffmpeg esté disponible
        try:
            subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            raise VideoGeneratorError("ffmpeg no está instalado o no está en PATH")
    
    def load_and_validate_slides(self) -> List[Dict[str, Any]]:
        """Carga y valida las slides desde el archivo de entrada."""
        print(f"Leyendo archivo: {self.input_txt_path}")
        
        with open(self.input_txt_path, 'r', encoding='utf-8') as f:
            raw_text = f.read()
        
        # Guardar texto crudo para debugging
        raw_output_path = os.path.join(self.job_dir, 'raw_llm_output.txt')
        with open(raw_output_path, 'w', encoding='utf-8') as f:
            f.write(raw_text)
        
        try:
            slides = JSONExtractor.extract_json_from_text(raw_text)
            print(f"Extraídas {len(slides)} slides")
        except Exception as e:
            raise VideoGeneratorError(f"Error extrayendo slides: {e}")
        
        # Validar con schema
        self._validate_slides_schema(slides)
        
        # Validar tiempos
        TimeUtils.validate_slide_times(slides)
        
        return slides
    
    def _validate_slides_schema(self, slides: List[Dict[str, Any]]) -> None:
        """Valida slides contra el schema JSON."""
        schema_path = os.path.join(os.path.dirname(__file__), 'slides.schema.json')
        
        if not os.path.exists(schema_path):
            print("WARNING: slides.schema.json no encontrado, saltando validación de schema")
            return
        
        with open(schema_path, 'r', encoding='utf-8') as f:
            schema = json.load(f)
        
        try:
            jsonschema.validate(slides, schema)
            print("✓ Validación de schema exitosa")
        except jsonschema.ValidationError as e:
            raise VideoGeneratorError(f"Error de validación de schema: {e.message}")
    
    def render_slides(self, slides: List[Dict[str, Any]]) -> List[str]:
        """Renderiza todas las slides como imágenes PNG."""
        print("Renderizando slides...")
        
        slide_paths = []
        
        for i, slide in enumerate(slides, 1):
            filename = f"slide_{i:04d}.png"
            output_path = os.path.join(self.job_dir, filename)
            
            # render_slide ahora retorna la ruta real con el estilo incluido
            actual_path = self.renderer.render_slide(slide, i, output_path)
            slide_paths.append(actual_path)
        
        # Mostrar estadísticas de distribución de estilos
        stats = self.renderer.style_manager.get_style_statistics()
        print(f"\n📊 Estadísticas de estilos utilizados:")
        print(f"   Total de slides: {stats['total_selections']}")
        print(f"   Promedio esperado por estilo: {stats['expected_per_style']:.1f}")
        for style, count in stats['usage_count'].items():
            variance = stats['variance'][style]
            print(f"   • {style}: {count} veces (desviación: {variance:+.1f})")
        
        return slide_paths
    
    def generate_concat_file(self, slides: List[Dict[str, Any]], slide_paths: List[str]) -> str:
        """Genera archivo list.txt para ffmpeg concat."""
        list_path = os.path.join(self.job_dir, 'list.txt')
        
        print("Generando archivo de concatenación...")
        
        with open(list_path, 'w', encoding='utf-8') as f:
            for i, slide in enumerate(slides):
                inicio_sec = TimeUtils.time_to_seconds(slide['inicio'])
                fin_sec = TimeUtils.time_to_seconds(slide['fin'])
                duration = fin_sec - inicio_sec
                
                # Usar ruta relativa para ffmpeg
                slide_filename = os.path.basename(slide_paths[i])
                f.write(f"file '{slide_filename}'\n")
                f.write(f"duration {duration:.1f}\n")
            
            # Para que ffmpeg reproduzca correctamente, agregar la última imagen sin duración
            if slides:
                last_slide_filename = os.path.basename(slide_paths[-1])
                f.write(f"file '{last_slide_filename}'\n")
        
        print(f"Archivo de concatenación generado: {list_path}")
        return list_path
    
    def create_video(self, list_path: str) -> str:
        """Crea video de slides usando ffmpeg."""
        slides_video_path = os.path.join(self.job_dir, 'slides.mp4')
        
        print("Generando video de slides...")
        
        # Comando ffmpeg para crear video de slides con configuración compatible
        cmd = [
            'ffmpeg', '-y',
            '-f', 'concat',
            '-safe', '0',
            '-i', list_path,
            '-fps_mode', 'cfr',  # Usar fps_mode en lugar de vsync
            '-r', '25',  # Frame rate
            '-pix_fmt', 'yuv420p',
            slides_video_path
        ]
        
        try:
            # Ejecutar desde el directorio de trabajo para rutas relativas
            result = subprocess.run(cmd, cwd=self.job_dir, capture_output=True, text=True)
            if result.returncode != 0:
                print(f"Error ffmpeg stdout: {result.stdout}")
                print(f"Error ffmpeg stderr: {result.stderr}")
                raise VideoGeneratorError(f"Error en ffmpeg (slides): {result.stderr}")
            
            print(f"Video de slides generado: {slides_video_path}")
        except Exception as e:
            raise VideoGeneratorError(f"Error ejecutando ffmpeg: {e}")
        
        return slides_video_path
    
    def merge_audio(self, slides_video_path: str) -> None:
        """Combina video de slides con audio."""
        print("Combinando video con audio...")
        
        # Primero obtener la duración del audio
        audio_duration_cmd = [
            'ffprobe', '-v', 'quiet', 
            '-show_entries', 'format=duration',
            '-of', 'default=noprint_wrappers=1:nokey=1',
            self.audio_path
        ]
        
        try:
            audio_result = subprocess.run(audio_duration_cmd, capture_output=True, text=True)
            audio_duration = float(audio_result.stdout.strip())
            print(f"Duración del audio: {audio_duration:.2f} segundos")
        except Exception as e:
            print(f"Warning: No se pudo obtener duración del audio: {e}")
            audio_duration = None
        
        # Comando simplificado para combinar video y audio
        cmd = [
            'ffmpeg', '-y',
            '-i', slides_video_path,
            '-i', self.audio_path,
            '-c:v', 'copy',  # Copiar video sin recodificar
            '-c:a', 'aac',
            '-map', '0:v:0',
            '-map', '1:a:0',
        ]
        
        # Si tenemos la duración del audio, usarla como referencia
        if audio_duration:
            cmd.extend(['-t', str(audio_duration)])
        
        cmd.append(self.output_video_path)
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode != 0:
                print(f"Error ffmpeg stdout: {result.stdout}")
                print(f"Error ffmpeg stderr: {result.stderr}")
                raise VideoGeneratorError(f"Error en ffmpeg (audio merge): {result.stderr}")
            
            print(f"Video final generado: {self.output_video_path}")
        except Exception as e:
            raise VideoGeneratorError(f"Error combinando audio: {e}")
    
    def generate_manifest(self, slides: List[Dict[str, Any]]) -> None:
        """Genera archivo manifest.json con metadatos."""
        print("Generando manifest...")
        
        # Calcular checksums
        def file_checksum(path: str) -> str:
            if not os.path.exists(path):
                return ""
            with open(path, 'rb') as f:
                return hashlib.md5(f.read()).hexdigest()
        
        # Calcular duración total
        total_duration = 0
        if slides:
            last_slide = slides[-1]
            total_duration = TimeUtils.time_to_seconds(last_slide['fin'])
        
        manifest = {
            "timestamp": datetime.now().isoformat(),
            "input_files": {
                "text": self.input_txt_path,
                "audio": self.audio_path
            },
            "output_file": self.output_video_path,
            "slides_count": len(slides),
            "total_duration_seconds": total_duration,
            "job_directory": self.job_dir,
            "checksums": {
                "input_text": file_checksum(self.input_txt_path),
                "input_audio": file_checksum(self.audio_path),
                "output_video": file_checksum(self.output_video_path)
            },
            "slides_summary": [
                {
                    "index": i + 1,
                    "titulo": slide.get('titulo', ''),
                    "inicio": slide.get('inicio', ''),
                    "fin": slide.get('fin', ''),
                    "duration": TimeUtils.time_to_seconds(slide['fin']) - TimeUtils.time_to_seconds(slide['inicio'])
                }
                for i, slide in enumerate(slides)
            ]
        }
        
        manifest_path = os.path.join(self.job_dir, 'manifest.json')
        with open(manifest_path, 'w', encoding='utf-8') as f:
            json.dump(manifest, f, indent=2, ensure_ascii=False)
        
        print(f"Manifest guardado: {manifest_path}")
    
    def generate(self) -> None:
        """Método principal para generar el video."""
        print("=== Iniciando generación de video ===")
        
        try:
            # Validar entradas
            self.validate_inputs()
            
            # Cargar y validar slides
            slides = self.load_and_validate_slides()
            
            # Renderizar slides
            slide_paths = self.render_slides(slides)
            
            # Generar archivo de concatenación
            list_path = self.generate_concat_file(slides, slide_paths)
            
            # Crear video de slides
            slides_video_path = self.create_video(list_path)
            
            # Combinar con audio
            self.merge_audio(slides_video_path)
            
            # Generar manifest
            self.generate_manifest(slides)
            
            print(f"✓ Video generado exitosamente: {self.output_video_path}")
            print(f"✓ Artefactos guardados en: {self.job_dir}")
            
        except VideoGeneratorError as e:
            print(f"ERROR: {e}")
            sys.exit(1)
        except Exception as e:
            print(f"ERROR INESPERADO: {e}")
            sys.exit(1)


def main():
    """Función principal del script."""
    parser = argparse.ArgumentParser(
        description="Genera video MP4 sincronizado con diapositivas desde texto y audio",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos:
  python generate_video.py input.txt audio.mp3 output.mp4
  python generate_video.py /ruta/completa/texto.md /ruta/audio.wav /ruta/video.mp4
        """
    )
    
    parser.add_argument('input_txt_path', 
                       help='Ruta completa al archivo TXT/MD con JSON o bloques de texto')
    parser.add_argument('audio_path', 
                       help='Ruta completa al archivo de audio (mp3/wav)')
    parser.add_argument('output_video_path', 
                       help='Ruta completa donde guardar el video MP4')
    
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Mostrar información detallada')
    
    args = parser.parse_args()
    
    if args.verbose:
        print(f"Input TXT: {args.input_txt_path}")
        print(f"Audio: {args.audio_path}")
        print(f"Output Video: {args.output_video_path}")
        print()
    
    # Crear y ejecutar generador
    generator = VideoGenerator(args.input_txt_path, args.audio_path, args.output_video_path)
    generator.generate()


if __name__ == "__main__":
    main()
