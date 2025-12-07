#!/usr/bin/env python3
"""
Script para limpiar y arreglar el guión de slides.
Elimina duplicados y llena gaps de tiempo.
"""

import json
import sys
from typing import List, Dict, Any

def time_to_seconds(time_str: str) -> float:
    """Convierte tiempo MM:SS a segundos."""
    try:
        if ':' in time_str:
            parts = time_str.split(':')
            if len(parts) == 2:
                minutes, seconds = parts
                return int(minutes) * 60 + int(seconds)
            elif len(parts) == 3:
                hours, minutes, seconds = parts
                return int(hours) * 3600 + int(minutes) * 60 + int(seconds)
        return float(time_str)
    except:
        return 0.0

def seconds_to_time(seconds: float) -> str:
    """Convierte segundos a formato MM:SS."""
    minutes = int(seconds // 60)
    secs = int(seconds % 60)
    return f"{minutes:02d}:{secs:02d}"

def clean_script(script_text: str) -> List[Dict[str, Any]]:
    """Limpia el script eliminando duplicados y organizando por tiempo."""
    
    # Parsear todas las secciones del script
    all_slides = []
    
    # Dividir por secciones (arrays JSON separados)
    sections = script_text.strip().split('\n]\n\n[')
    
    for i, section in enumerate(sections):
        # Limpiar y formar JSON válido
        if not section.startswith('['):
            section = '[' + section
        if not section.endswith(']'):
            section = section + ']'
        
        try:
            slides = json.loads(section)
            all_slides.extend(slides)
        except json.JSONDecodeError as e:
            print(f"Error parseando sección {i+1}: {e}")
            continue
    
    # Eliminar duplicados basado en tiempo de inicio
    seen_times = set()
    unique_slides = []
    
    for slide in all_slides:
        inicio_sec = time_to_seconds(slide['inicio'])
        if inicio_sec not in seen_times:
            seen_times.add(inicio_sec)
            unique_slides.append(slide)
        else:
            print(f"Eliminando duplicado en {slide['inicio']}: {slide['titulo']}")
    
    # Ordenar por tiempo de inicio
    unique_slides.sort(key=lambda x: time_to_seconds(x['inicio']))
    
    # Verificar y llenar gaps
    print("\n🔍 Analizando timeline:")
    for i, slide in enumerate(unique_slides):
        inicio_sec = time_to_seconds(slide['inicio'])
        fin_sec = time_to_seconds(slide['fin'])
        print(f"  {slide['inicio']}-{slide['fin']}: {slide['titulo']}")
        
        # Verificar gap con la siguiente slide
        if i < len(unique_slides) - 1:
            next_inicio_sec = time_to_seconds(unique_slides[i+1]['inicio'])
            if fin_sec < next_inicio_sec:
                gap_duration = next_inicio_sec - fin_sec
                print(f"  ⚠️  GAP: {seconds_to_time(fin_sec)}-{seconds_to_time(next_inicio_sec)} ({gap_duration:.0f}s)")
                
                # Crear slide de relleno para gaps grandes (>2 segundos)
                if gap_duration > 2:
                    fill_slide = {
                        "inicio": seconds_to_time(fin_sec),
                        "fin": seconds_to_time(next_inicio_sec),
                        "titulo": "Transición",
                        "puntos": ["Continuamos...", "Próximo tema"]
                    }
                    unique_slides.append(fill_slide)
                    print(f"  ✅ Agregada slide de relleno: {fill_slide['inicio']}-{fill_slide['fin']}")
    
    # Re-ordenar después de agregar rellenos
    unique_slides.sort(key=lambda x: time_to_seconds(x['inicio']))
    
    return unique_slides

def main():
    if len(sys.argv) != 2:
        print("Uso: python fix_script.py <archivo_guion.txt>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            script_content = f.read()
        
        print("🔧 Limpiando y arreglando guión...")
        cleaned_slides = clean_script(script_content)
        
        # Guardar resultado
        output_file = input_file.replace('.txt', '_limpio.json')
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(cleaned_slides, f, ensure_ascii=False, indent=2)
        
        print(f"\n✅ Guión limpio guardado en: {output_file}")
        print(f"📊 Slides totales: {len(cleaned_slides)}")
        
        # Mostrar timeline final
        print(f"\n📋 Timeline final:")
        for slide in cleaned_slides:
            print(f"  {slide['inicio']}-{slide['fin']}: {slide['titulo']}")
            
        # Verificar duración total
        if cleaned_slides:
            ultimo_fin = time_to_seconds(cleaned_slides[-1]['fin'])
            print(f"\n⏱️  Duración total del video: {seconds_to_time(ultimo_fin)} ({ultimo_fin:.1f}s)")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
