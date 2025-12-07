import os
import asyncio
import subprocess
import edge_tts
from datetime import timedelta

class TextBlock:
    def __init__(self, text='', voice='es-MX-DaliaNeural', speed='Normal'):
        self.text = text
        self.voice = voice
        self.speed = speed  # Agregar atributo de velocidad
        self.duration = 0  # Duración en segundos del audio generado
        self.start_time = 0  # Tiempo de inicio en el podcast completo

class PodcastModel:
    def __init__(self):
        self.text_blocks = [TextBlock()]  # Inicia con un bloque de texto
        self.available_voices = self.get_available_voices()
        self.max_tts_chars = 3000  # Edge TTS permite textos más largos
        self.speed_map = {
            'Muy lenta': '-50%',
            'Lenta': '-25%',
            'Normal': '+0%',
            'Rápida': '+25%',
            'Muy rápida': '+50%'
        }

    def get_available_voices(self):
        """Obtiene las voces neurales de Edge TTS en español latino"""
        voices = {
            'Locutor 1 (Mujer México)': 'es-MX-DaliaNeural',
            'Locutor 2 (Hombre México)': 'es-MX-JorgeNeural', 
            'Locutor 3 (Mujer Colombia)': 'es-CO-SalomeNeural',
            'Locutor 4 (Hombre Colombia)': 'es-CO-GonzaloNeural',
            'Locutor 5 (Mujer Argentina)': 'es-AR-ElenaNeural',
            'Locutor 6 (Hombre Argentina)': 'es-AR-TomasNeural'
        }
        return voices

    def add_text_block(self):
        """Añade un nuevo bloque de texto"""
        self.text_blocks.append(TextBlock())

    def generate_audio(self, file_name='podcast.mp3'):
        """Genera el archivo de audio usando Edge TTS y calcula timestamps"""
        temp_files = []
        current_time = 0.0  # Tiempo acumulado en segundos

        # Procesar cada bloque de texto y generar un archivo temporal
        for idx, block in enumerate(self.text_blocks):
            if not block.text.strip():
                print(f"Bloque de texto {idx + 1} está vacío. Se omitirá.")
                continue

            temp_file = f'temp_{idx}.wav'
            
            # Establecer tiempo de inicio para este bloque
            block.start_time = current_time
            
            # Ejecutar Edge TTS de forma asíncrona
            asyncio.run(self.generate_edge_audio_async(
                block.text, temp_file, block.voice, block.speed
            ))

            if os.path.exists(temp_file) and os.path.getsize(temp_file) > 1000:
                # Calcular duración del archivo de audio generado
                duration = self.get_audio_duration(temp_file)
                block.duration = duration
                current_time += duration
                
                temp_files.append(temp_file)
                print(f"✅ Archivo temporal creado: {temp_file} (duración: {duration:.2f}s)")
            else:
                print(f"❌ Error generando el archivo de audio {temp_file}, se omitirá.")

        # Combinar todos los archivos temporales usando ffmpeg
        if temp_files:
            self.combine_audio_files(temp_files, file_name)
            print(f"✅ Podcast generado exitosamente: {file_name}")
            
            # Generar guión con timestamps
            self.generate_transcript_with_timestamps(file_name)

        # Eliminar archivos temporales
        for temp_file in temp_files:
            if os.path.exists(temp_file):
                os.remove(temp_file)

    def get_audio_duration(self, audio_file):
        """Obtiene la duración en segundos de un archivo de audio usando ffprobe"""
        try:
            result = subprocess.run([
                'ffprobe', '-v', 'quiet', '-show_entries', 'format=duration',
                '-of', 'default=noprint_wrappers=1:nokey=1', audio_file
            ], capture_output=True, text=True, check=True)
            
            duration = float(result.stdout.strip())
            return duration
        except (subprocess.CalledProcessError, ValueError) as e:
            print(f"❌ Error calculando duración de {audio_file}: {e}")
            # Estimación basada en caracteres (aprox 10-15 caracteres por segundo)
            estimated_duration = len(self.text_blocks[0].text) / 12.0
            return estimated_duration

    def format_timestamp(self, seconds):
        """Convierte segundos a formato MM:SS o HH:MM:SS"""
        td = timedelta(seconds=seconds)
        total_seconds = int(td.total_seconds())
        hours, remainder = divmod(total_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        
        if hours > 0:
            return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        else:
            return f"{minutes:02d}:{seconds:02d}"

    def generate_transcript_with_timestamps(self, audio_file):
        """Genera un guión con timestamps en el formato solicitado"""
        base_name = os.path.splitext(audio_file)[0]
        transcript_file = f"{base_name}_guion.txt"
        
        # Mapeo de voces a descripción
        voice_descriptions = {
            'es-AR-ElenaNeural': '[VOZ1] (Mujer Argentina)',
            'es-AR-TomasNeural': '[VOZ2] (Hombre Argentina)',
            'es-MX-DaliaNeural': '[VOZ1] (Mujer México)',
            'es-MX-JorgeNeural': '[VOZ2] (Hombre México)',
            'es-CO-SalomeNeural': '[VOZ1] (Mujer Colombia)',
            'es-CO-GonzaloNeural': '[VOZ2] (Hombre Colombia)'
        }
        
        try:
            with open(transcript_file, 'w', encoding='utf-8') as f:
                f.write("# Guión del Podcast con Timestamps\n\n")
                
                for block in self.text_blocks:
                    if not block.text.strip():
                        continue
                        
                    # Calcular tiempo de inicio y fin
                    start_time = self.format_timestamp(block.start_time)
                    end_time = self.format_timestamp(block.start_time + block.duration)
                    
                    # Obtener descripción de la voz
                    voice_desc = voice_descriptions.get(block.voice, '[VOZ] (Voz)')
                    
                    # Escribir en el formato solicitado
                    f.write(f"[{start_time} - {end_time}] {voice_desc}\n")
                    f.write(f"{block.text}\n\n")
            
            print(f"✅ Guión con timestamps generado: {transcript_file}")
            
        except Exception as e:
            print(f"❌ Error generando guión: {e}")

    def combine_audio_files(self, input_files, output_file):
        """Combina múltiples archivos de audio usando ffmpeg"""
        if len(input_files) == 1:
            # Si solo hay un archivo, simplemente convertirlo a MP3
            subprocess.run([
                'ffmpeg', '-i', input_files[0], '-acodec', 'mp3', '-y', output_file
            ], check=True, capture_output=True)
        else:
            # Crear lista de archivos para ffmpeg
            concat_list = 'concat_list.txt'
            with open(concat_list, 'w') as f:
                for file in input_files:
                    f.write(f"file '{file}'\n")
            
            # Combinar archivos usando ffmpeg
            subprocess.run([
                'ffmpeg', '-f', 'concat', '-safe', '0', '-i', concat_list, 
                '-acodec', 'mp3', '-y', output_file
            ], check=True, capture_output=True)
            
            # Eliminar archivo temporal de lista
            if os.path.exists(concat_list):
                os.remove(concat_list)

    def clean_text_for_tts(self, text):
        """Limpia el texto para evitar problemas con TTS"""
        import re
        
        # Remover caracteres especiales problemáticos
        clean_text = text.strip()
        
        # Reemplazar caracteres que Edge TTS puede malinterpretar
        replacements = {
            '&': ' y ',
            '<': ' menor que ',
            '>': ' mayor que ',
            '"': '',
            "'": '',
            '`': '',
            '*': '',
            '_': '',
            '#': '',
            '@': ' arroba ',
            '%': ' por ciento',
            '$': ' dólares',
            '€': ' euros',
            '£': ' libras',
            '|': '',
            '\\': '',
            '/': ' ',
            '~': '',
            '^': '',
            '[': '',
            ']': '',
            '{': '',
            '}': '',
            '=': ' es igual a '
        }
        
        for old, new in replacements.items():
            clean_text = clean_text.replace(old, new)
        
        # Limpiar espacios múltiples
        clean_text = re.sub(r'\s+', ' ', clean_text).strip()
        
        return clean_text

    async def generate_edge_audio_async(self, text, temp_file, voice_code, speed):
        """Genera audio usando Edge TTS (Microsoft) - GRATIS"""
        try:
            # Limpiar el texto de caracteres problemáticos
            clean_text = self.clean_text_for_tts(text)
            
            # Usar Edge TTS simple sin SSML complejo
            communicate = edge_tts.Communicate(
                text=clean_text, 
                voice=voice_code,
                rate=self.speed_map[speed]  # Aplicar velocidad directamente
            )
            await communicate.save(temp_file)
            print(f"✅ Audio generado con Edge TTS ({voice_code}): '{clean_text[:50]}...'")
            
        except Exception as e:
            print(f"❌ Error con configuración de velocidad, usando modo básico: {e}")
            # Fallback completamente básico
            try:
                clean_text = self.clean_text_for_tts(text)
                communicate = edge_tts.Communicate(text=clean_text, voice=voice_code)
                await communicate.save(temp_file)
                print(f"✅ Audio generado (modo básico): '{clean_text[:50]}...'")
            except Exception as e2:
                print(f"❌ Error crítico con Edge TTS: {e2}")

    def split_text_into_segments(self, text, max_chars):
        """Divide el texto en segmentos más pequeños basados en el límite de caracteres"""
        words = text.split()
        segments = []
        current_segment = ""

        for word in words:
            if len(current_segment) + len(word) + 1 <= max_chars:  # +1 para el espacio
                current_segment += (word + " ")
            else:
                if current_segment:
                    segments.append(current_segment.strip())
                current_segment = word + " "

        if current_segment:  # Añadir el último segmento si queda algo
            segments.append(current_segment.strip())

        return segments
