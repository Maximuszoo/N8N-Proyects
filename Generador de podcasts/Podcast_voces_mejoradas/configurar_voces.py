#!/usr/bin/env python3
"""
Configurador de voces para el generador de podcast
Permite cambiar fácilmente entre diferentes locutores
"""

VOCES_DISPONIBLES = {
    # México
    "mx_dalia": "es-MX-DaliaNeural",      # Mujer México
    "mx_jorge": "es-MX-JorgeNeural",      # Hombre México
    
    # Colombia  
    "co_salome": "es-CO-SalomeNeural",    # Mujer Colombia
    "co_gonzalo": "es-CO-GonzaloNeural",  # Hombre Colombia
    
    # Argentina
    "ar_elena": "es-AR-ElenaNeural",      # Mujer Argentina
    "ar_tomas": "es-AR-TomasNeural",      # Hombre Argentina
    
    # España (opcional)
    "es_elvira": "es-ES-ElviraNeural",    # Mujer España
    "es_alvaro": "es-ES-AlvaroNeural",    # Hombre España
    
    # Perú
    "pe_camila": "es-PE-CamilaNeural",    # Mujer Perú
    "pe_alex": "es-PE-AlexNeural",        # Hombre Perú
    
    # Chile
    "cl_catalina": "es-CL-CatalinaNeural", # Mujer Chile
    "cl_lorenzo": "es-CL-LorenzoNeural",   # Hombre Chile
}

CONFIGURACIONES_PODCAST = {
    "mexicano": {
        "voz1": "mx_dalia",
        "voz2": "mx_jorge",
        "descripcion": "Podcast estilo mexicano con Dalia y Jorge"
    },
    "colombiano": {
        "voz1": "co_salome", 
        "voz2": "co_gonzalo",
        "descripcion": "Podcast estilo colombiano con Salome y Gonzalo"
    },
    "argentino": {
        "voz1": "ar_elena",
        "voz2": "ar_tomas", 
        "descripcion": "Podcast estilo argentino con Elena y Tomás"
    },
    "mixto_latino": {
        "voz1": "mx_dalia",
        "voz2": "co_gonzalo",
        "descripcion": "Podcast multinacional con Dalia (México) y Gonzalo (Colombia)"
    },
    "espanol": {
        "voz1": "es_elvira",
        "voz2": "es_alvaro",
        "descripcion": "Podcast estilo español con Elvira y Álvaro"
    }
}

def generar_configuracion(estilo="mexicano"):
    """Genera el código para Podcast.py con el estilo seleccionado"""
    
    if estilo not in CONFIGURACIONES_PODCAST:
        print(f"❌ Estilo '{estilo}' no disponible.")
        print(f"Estilos disponibles: {list(CONFIGURACIONES_PODCAST.keys())}")
        return
    
    config = CONFIGURACIONES_PODCAST[estilo]
    voz1 = VOCES_DISPONIBLES[config["voz1"]]
    voz2 = VOCES_DISPONIBLES[config["voz2"]]
    
    codigo = f'''
            # Mapear VOZ1/VOZ2 a las voces - {config["descripcion"]}
            voice_num = voice_match.group(1)
            if voice_num == "1":
                current_voice = "{voz1}"  # {config["voz1"]}
            elif voice_num == "2":
                current_voice = "{voz2}"  # {config["voz2"]}
    '''
    
    print(f"\n🎙️ Configuración para estilo '{estilo}':")
    print(f"📝 {config['descripcion']}")
    print(f"🎭 VOZ1: {config['voz1']} ({voz1})")
    print(f"🎭 VOZ2: {config['voz2']} ({voz2})")
    print(f"\n📋 Código para copiar en Podcast.py (líneas 35-40):")
    print("="*60)
    print(codigo)
    print("="*60)

def mostrar_todas_las_voces():
    """Muestra todas las voces disponibles organizadas por país"""
    print("\n🌎 TODAS LAS VOCES DISPONIBLES:")
    print("="*50)
    
    paises = {
        "México": ["mx_dalia", "mx_jorge"],
        "Colombia": ["co_salome", "co_gonzalo"], 
        "Argentina": ["ar_elena", "ar_tomas"],
        "España": ["es_elvira", "es_alvaro"],
        "Perú": ["pe_camila", "pe_alex"],
        "Chile": ["cl_catalina", "cl_lorenzo"]
    }
    
    for pais, voces in paises.items():
        print(f"\n🇪🇸 {pais}:")
        for voz in voces:
            genero = "👩 Mujer" if any(x in voz for x in ["dalia", "salome", "elena", "elvira", "camila", "catalina"]) else "👨 Hombre"
            print(f"  {genero} {voz}: {VOCES_DISPONIBLES[voz]}")

def menu_principal():
    """Menú interactivo para configurar voces"""
    print("\n🎙️ CONFIGURADOR DE VOCES PARA PODCAST")
    print("="*50)
    print("1. Ver todas las voces disponibles")
    print("2. Generar configuración mexicana")
    print("3. Generar configuración colombiana") 
    print("4. Generar configuración argentina")
    print("5. Generar configuración mixta latinoamericana")
    print("6. Generar configuración española")
    print("0. Salir")
    
    opcion = input("\n🔢 Selecciona una opción: ").strip()
    
    if opcion == "1":
        mostrar_todas_las_voces()
    elif opcion == "2":
        generar_configuracion("mexicano")
    elif opcion == "3":
        generar_configuracion("colombiano")
    elif opcion == "4":
        generar_configuracion("argentino")
    elif opcion == "5":
        generar_configuracion("mixto_latino")
    elif opcion == "6":
        generar_configuracion("espanol")
    elif opcion == "0":
        print("👋 ¡Hasta luego!")
        return False
    else:
        print("❌ Opción no válida")
    
    return True

if __name__ == "__main__":
    print("🎭 CONFIGURADOR DE VOCES PARA PODCAST EN ESPAÑOL")
    print("🔧 Herramienta para cambiar fácilmente entre diferentes locutores")
    
    while menu_principal():
        input("\n⏎ Presiona Enter para continuar...")
        print("\n" + "="*60 + "\n")
