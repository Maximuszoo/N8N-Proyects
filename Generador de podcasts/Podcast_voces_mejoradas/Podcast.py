import sys
from model import PodcastModel, TextBlock

import sys
import json
import re
from model import PodcastModel, TextBlock

def extract_json_from_dirty_text(content):
    """Extrae JSON de texto sucio de IA, manejando múltiples fragmentos y texto basura"""
    print("🔍 Extrayendo JSON de texto sucio...")
    
    # Separar el contenido por bloques usando líneas vacías
    blocks = re.split(r'\n\s*\n+', content.strip())
    
    json_objects = []
    
    for i, block in enumerate(blocks):
        if not block.strip():
            continue
            
        print(f"📝 Procesando bloque {i+1}: {block[:100]}...")
        
        # Buscar patrones que parezcan arrays JSON
        json_patterns = [
            r'\[[\s\S]*?\]',  # Cualquier array
        ]
        
        for pattern in json_patterns:
            matches = re.findall(pattern, block, re.MULTILINE | re.DOTALL)
            for match in matches:
                # Verificar que el match contenga palabras clave de podcast
                if any(keyword in match.lower() for keyword in ['hablante', 'voz', 'texto', 'locutor']):
                    try:
                        # Limpiar el JSON encontrado
                        clean_json = clean_json_string(match)
                        print(f"🧹 JSON limpiado: {clean_json[:150]}...")
                        
                        parsed = json.loads(clean_json)
                        
                        # Verificar que tenga la estructura correcta
                        if is_valid_podcast_json(parsed):
                            json_objects.append(parsed)
                            print(f"✅ JSON válido encontrado con {len(parsed)} elementos")
                    except json.JSONDecodeError as e:
                        print(f"⚠️ Error parsing JSON en bloque {i+1}: {e}")
                        print(f"   JSON problemático: {clean_json[:200]}...")
                        continue
    
    # Si no encontramos JSONs válidos, buscar líneas que parezcan diálogo
    if not json_objects:
        print("⚠️ No se encontró JSON válido, buscando formato [VOZ] alternativo...")
        return extract_voice_format_fallback(content)
    
    # Combinar todos los JSONs encontrados y eliminar duplicados
    combined_segments = []
    seen_texts = set()  # Para evitar duplicados
    
    for json_obj in json_objects:
        if isinstance(json_obj, list):
            for segment in json_obj:
                text = extract_text(segment)
                if text and text.strip() not in seen_texts:
                    combined_segments.append(segment)
                    seen_texts.add(text.strip())
        elif isinstance(json_obj, dict) and 'podcast' in json_obj:
            for segment in json_obj['podcast']:
                text = extract_text(segment)
                if text and text.strip() not in seen_texts:
                    combined_segments.append(segment)
                    seen_texts.add(text.strip())
    
    print(f"🎯 Total de segmentos únicos extraídos: {len(combined_segments)}")
    return combined_segments

def clean_json_string(json_str):
    """Limpia una cadena JSON de caracteres problemáticos"""
    # Remover texto antes del primer [ o {
    json_str = re.sub(r'^[^[\{]*', '', json_str)
    
    # Remover texto después del último ] o }
    json_str = re.sub(r'[^\]\}]*$', '', json_str)
    
    # 1. Arreglar claves sin comillas
    json_str = re.sub(r'\b(hablante|texto|locutor|voz|speaker|text|contenido|content)\s*:', r'"\1":', json_str, flags=re.IGNORECASE)
    
    # 2. Arreglar valores VOZ sin comillas
    json_str = re.sub(r':\s*(VOZ\d+)\s*([,}])', r': "\1"\2', json_str)
    
    # 3. Método más específico para arreglar texto sin comillas
    # Procesar línea por línea para manejar mejor el contenido de texto
    lines = json_str.split('\n')
    processed_lines = []
    
    for line in lines:
        # Si la línea contiene "texto": sin comillas en el valor
        if '"texto":' in line and not re.search(r'"texto":\s*"', line):
            # Encontrar dónde termina realmente el valor (buscar el } que cierra el objeto)
            line = re.sub(r'("texto":\s*)([^"][^}]*?)(\s*})', r'\1"\2"\3', line)
            
        processed_lines.append(line)
    
    json_str = '\n'.join(processed_lines)
    
    # 4. Limpiar comas dobles y otros problemas
    json_str = re.sub(r',,+', ',', json_str)  # Múltiples comas
    json_str = re.sub(r',\s*([}\]])', r'\1', json_str)  # Comas antes de } o ]
    
    # 5. Remover comentarios
    json_str = re.sub(r'//.*$', '', json_str, flags=re.MULTILINE)
    
    return json_str.strip()

def is_valid_podcast_json(data):
    """Verifica si el JSON tiene estructura válida para podcast"""
    if isinstance(data, list):
        # Verificar que sea un array de objetos con los campos necesarios
        for item in data:
            if not isinstance(item, dict):
                return False
            # Verificar que tenga al menos hablante y texto
            has_speaker = any(key.lower() in ['hablante', 'locutor', 'voz', 'speaker'] for key in item.keys())
            has_text = any(key.lower() in ['texto', 'text', 'contenido', 'content'] for key in item.keys())
            if not (has_speaker and has_text):
                return False
        return len(data) > 0
    
    elif isinstance(data, dict):
        # Verificar que sea un objeto con campo podcast
        return 'podcast' in data and isinstance(data['podcast'], list)
    
    return False

def extract_voice_format_fallback(content):
    """Fallback para extraer formato [VOZ1]/[VOZ2] del texto"""
    print("🔄 Usando fallback para formato [VOZ] tradicional...")
    
    segments = []
    lines = content.split('\n')
    current_speaker = None
    current_text = []
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # Buscar indicadores de hablante
        voice_match = re.match(r'^\[?(VOZ[12]|Voz[12]|locutor[12])\]?', line, re.IGNORECASE)
        if voice_match:
            # Guardar el segmento anterior si existe
            if current_speaker and current_text:
                segments.append({
                    'hablante': current_speaker,
                    'texto': ' '.join(current_text).strip(),
                    'metadatos': {'emocion': 'neutral'}
                })
                current_text = []
            
            current_speaker = voice_match.group(1).upper()
            # El resto de la línea puede ser texto
            remaining_text = line[voice_match.end():].strip()
            if remaining_text:
                current_text.append(remaining_text)
        
        elif current_speaker and line:
            # Es texto del hablante actual
            current_text.append(line)
    
    # Guardar el último segmento
    if current_speaker and current_text:
        segments.append({
            'hablante': current_speaker,
            'texto': ' '.join(current_text).strip(),
            'metadatos': {'emocion': 'neutral'}
        })
    
    return segments

def parse_script_file(file_path):
    """Parsea archivo que puede contener JSON sucio o formato tradicional [VOZ]"""
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    print(f"📖 Parseando archivo: {file_path}")
    
    # Intentar extraer JSON del texto sucio
    segments = extract_json_from_dirty_text(content)
    
    if not segments:
        print("❌ No se pudo extraer contenido válido del archivo")
        return []
    
    # Convertir segmentos JSON a TextBlocks
    blocks = []
    for segment in segments:
        # Extraer información del segmento
        speaker = extract_speaker(segment)
        text = extract_text(segment)
        
        if not text.strip():
            continue
            
        # Mapear hablante a voz
        voice = map_speaker_to_voice(speaker)
        
        blocks.append(TextBlock(
            text=text.strip(),
            voice=voice,
            speed='Rápida'  # Mantener velocidad rápida por defecto
        ))
        
        print(f"🎙️ Bloque creado: {speaker} -> {voice}")
        print(f"   Texto: '{text[:60]}...'")
    
    print(f"✅ Parser completado: {len(blocks)} bloques de audio detectados")
    return blocks

def extract_speaker(segment):
    """Extrae el hablante del segmento JSON"""
    speaker_keys = ['hablante', 'locutor', 'voz', 'speaker']
    for key in speaker_keys:
        if key in segment:
            return str(segment[key]).upper()
    return 'VOZ1'  # Default

def extract_text(segment):
    """Extrae el texto del segmento JSON"""
    text_keys = ['texto', 'text', 'contenido', 'content']
    for key in text_keys:
        if key in segment:
            return str(segment[key])
    return ''

def map_speaker_to_voice(speaker, voice_style='argentina'):
    """Mapea hablante a voz específica según el estilo seleccionado"""
    speaker = speaker.upper()
    
    # Diferentes estilos de voces disponibles
    voice_styles = {
        'argentina': {
            'VOZ1': "es-AR-ElenaNeural",  # Mujer Argentina
            'VOZ2': "es-AR-TomasNeural"   # Hombre Argentina
        },
        'mexico': {
            'VOZ1': "es-MX-DaliaNeural",  # Mujer México
            'VOZ2': "es-MX-JorgeNeural"   # Hombre México
        },
        'colombia': {
            'VOZ1': "es-CO-SalomeNeural", # Mujer Colombia
            'VOZ2': "es-CO-GonzaloNeural" # Hombre Colombia
        },
        'espana': {
            'VOZ1': "es-ES-ElviraNeural", # Mujer España
            'VOZ2': "es-ES-AlvaroNeural"  # Hombre España
        }
    }
    
    # Usar estilo por defecto si no se especifica
    style = voice_styles.get(voice_style, voice_styles['argentina'])
    
    # Mapear hablante
    if speaker in ['VOZ1', 'LOCUTOR1', 'HABLANTE1', 'SPEAKER1']:
        return style['VOZ1']
    elif speaker in ['VOZ2', 'LOCUTOR2', 'HABLANTE2', 'SPEAKER2']:
        return style['VOZ2']
    else:
        # Default a VOZ1 si no se reconoce
        return style['VOZ1']

def main(script_path, output_file="output_podcast.mp3"):
    model = PodcastModel()
    model.text_blocks = parse_script_file(script_path)
    model.generate_audio(output_file)
    print(f"✅ Podcast generado: {output_file}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python main.py ruta/al/guion.txt [salida.mp3]")
    else:
        script_path = sys.argv[1]
        output_file = sys.argv[2] if len(sys.argv) > 2 else "output_podcast.mp3"
        main(script_path, output_file)

