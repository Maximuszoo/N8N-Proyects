#!/usr/bin/env python3
import json
import re

def clean_json_string(json_str):
    """Limpia una cadena JSON de caracteres problemáticos"""
    print(f"🔧 JSON original:\n{json_str}")
    
    # Remover texto antes del primer [ o {
    json_str = re.sub(r'^[^[\{]*', '', json_str)
    
    # Remover texto después del último ] o }
    json_str = re.sub(r'[^\]\}]*$', '', json_str)
    
    # 1. Arreglar claves sin comillas
    json_str = re.sub(r'\b(hablante|texto|locutor|voz|speaker|text|contenido|content)\s*:', r'"\1":', json_str, flags=re.IGNORECASE)
    
    # 2. Arreglar valores VOZ sin comillas
    json_str = re.sub(r':\s*(VOZ\d+)\s*([,}])', r': "\1"\2', json_str)
    
    # 3. Método más específico para arreglar texto sin comillas
    # Usar un enfoque de parsing más cuidadoso
    
    # Procesar línea por línea
    lines = json_str.split('\n')
    processed_lines = []
    
    for line in lines:
        # Si la línea contiene "texto": sin comillas en el valor
        if '"texto":' in line and not re.search(r'"texto":\s*"', line):
            # Encontrar dónde termina realmente el valor (buscar el } o }, que cierra el objeto)
            # Patrón: "texto": valor_sin_comillas}, 
            line = re.sub(r'("texto":\s*)([^"][^}]*?)(\s*})', r'\1"\2"\3', line)
            
        processed_lines.append(line)
    
    json_str = '\n'.join(processed_lines)
    
    # 4. Limpiar comas dobles y otros problemas
    json_str = re.sub(r',,+', ',', json_str)  # Múltiples comas
    json_str = re.sub(r',\s*([}\]])', r'\1', json_str)  # Comas antes de } o ]
    
    # 5. Remover comentarios
    json_str = re.sub(r'//.*$', '', json_str, flags=re.MULTILINE)
    
    print(f"🔧 JSON limpiado:\n{json_str}")
    return json_str.strip()

# Probar con el archivo real
with open('test_nuevo_formato.txt', 'r', encoding='utf-8') as f:
    content = f.read()

print("=== CONTENIDO ORIGINAL ===")
print(content)
print("\n=== PROBANDO LIMPIEZA ===")

# Dividir por bloques como hace el parser
blocks = re.split(r'\n\s*\n', content.strip())
print(f"📊 Se encontraron {len(blocks)} bloques")

for i, block in enumerate(blocks, 1):
    print(f"\n--- BLOQUE {i} ---")
    if block.strip():
        cleaned = clean_json_string(block)
        try:
            data = json.loads(cleaned)
            print(f"✅ JSON válido: {len(data)} elementos")
            for item in data:
                print(f"   - {item.get('hablante', 'N/A')}: {item.get('texto', '')[:50]}...")
        except json.JSONDecodeError as e:
            print(f"❌ Error de JSON: {e}")
            print(f"📝 Contenido problemático: {cleaned[:200]}...")
