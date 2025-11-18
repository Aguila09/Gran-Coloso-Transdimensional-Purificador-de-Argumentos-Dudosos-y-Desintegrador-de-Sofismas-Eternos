"""
Interfaz Gráfica para El Gran Coloso Transdimensional
Purificador de Argumentos Dudosos y Desintegrador de Sofismas Eternos

Interfaz web usando Gradio que permite:
- Ingresar argumentos
- Ver clasificación de sesgos y falacias
- Ver explicaciones
- Ver señalamiento de partes problemáticas del texto
"""

import gradio as gr
from detector import DetectorFalaciasSesgos
from ontology import ResultadoAnalisis


def formatear_resultado_html(resultado: ResultadoAnalisis) -> str:
    """
    Formatea el resultado del análisis como HTML con resaltado
    """
    texto = resultado.texto_original
    
    # Crear lista de todas las detecciones con sus posiciones
    detecciones = []
    
    for falacia in resultado.falacias_detectadas:
        detecciones.append({
            'inicio': falacia.posicion_inicio,
            'fin': falacia.posicion_fin,
            'tipo': 'falacia',
            'nombre': falacia.get_tipo(),
            'confianza': falacia.confianza,
            'explicacion': falacia.explicacion
        })
    
    for sesgo in resultado.sesgos_detectados:
        detecciones.append({
            'inicio': sesgo.posicion_inicio,
            'fin': sesgo.posicion_fin,
            'tipo': 'sesgo',
            'nombre': sesgo.get_tipo(),
            'confianza': sesgo.confianza,
            'explicacion': sesgo.explicacion
        })
    
    # Ordenar por posición
    detecciones.sort(key=lambda x: x['inicio'])
    
    # Construir HTML con resaltado
    html = """
    <div style="font-family: Arial, sans-serif;">
        <h2>📊 Resultado del Análisis</h2>
    """
    
    # Estadísticas generales
    html += f"""
    <div style="background-color: #f0f0f0; padding: 15px; border-radius: 8px; margin-bottom: 20px;">
        <h3>Resumen</h3>
        <ul>
            <li><strong>Falacias detectadas:</strong> {len(resultado.falacias_detectadas)}</li>
            <li><strong>Sesgos cognitivos detectados:</strong> {len(resultado.sesgos_detectados)}</li>
            <li><strong>Confianza general:</strong> {resultado.confianza_general:.2%}</li>
        </ul>
    </div>
    """
    
    # Texto con resaltado
    html += "<h3>Texto Analizado (con señalamientos)</h3>"
    html += '<div style="background-color: white; padding: 15px; border: 1px solid #ddd; border-radius: 8px; line-height: 1.8;">'
    
    if detecciones:
        ultimo_idx = 0
        for det in detecciones:
            # Texto antes de la detección
            html += texto[ultimo_idx:det['inicio']]
            
            # Texto detectado con resaltado
            color = '#ffcccc' if det['tipo'] == 'falacia' else '#ffffcc'
            tooltip = f"{det['nombre']} (Confianza: {det['confianza']:.0%})"
            html += f'<span style="background-color: {color}; padding: 2px 4px; border-radius: 3px; cursor: help;" title="{tooltip}">'
            html += texto[det['inicio']:det['fin']]
            html += '</span>'
            
            ultimo_idx = det['fin']
        
        # Texto restante
        html += texto[ultimo_idx:]
    else:
        html += texto
    
    html += '</div>'
    
    # Lista detallada de falacias
    if resultado.falacias_detectadas:
        html += "<h3>🚫 Falacias Detectadas</h3>"
        for i, falacia in enumerate(resultado.falacias_detectadas, 1):
            fragmento = texto[falacia.posicion_inicio:falacia.posicion_fin]
            html += f"""
            <div style="background-color: #ffe6e6; padding: 12px; margin-bottom: 10px; border-left: 4px solid #ff4444; border-radius: 4px;">
                <h4 style="margin-top: 0;">#{i}: {falacia.get_tipo()}</h4>
                <p><strong>Fragmento:</strong> <em>"{fragmento}"</em></p>
                <p><strong>Explicación:</strong> {falacia.explicacion}</p>
                <p><strong>Confianza:</strong> {falacia.confianza:.0%}</p>
            </div>
            """
    
    # Lista detallada de sesgos
    if resultado.sesgos_detectados:
        html += "<h3>🧠 Sesgos Cognitivos Detectados</h3>"
        for i, sesgo in enumerate(resultado.sesgos_detectados, 1):
            fragmento = texto[sesgo.posicion_inicio:sesgo.posicion_fin]
            html += f"""
            <div style="background-color: #ffffcc; padding: 12px; margin-bottom: 10px; border-left: 4px solid #ffaa00; border-radius: 4px;">
                <h4 style="margin-top: 0;">#{i}: {sesgo.get_tipo()}</h4>
                <p><strong>Fragmento:</strong> <em>"{fragmento}"</em></p>
                <p><strong>Explicación:</strong> {sesgo.explicacion}</p>
                <p><strong>Confianza:</strong> {sesgo.confianza:.0%}</p>
            </div>
            """
    
    # Si no hay detecciones
    if not resultado.falacias_detectadas and not resultado.sesgos_detectados:
        html += """
        <div style="background-color: #e6ffe6; padding: 15px; border-radius: 8px; text-align: center;">
            <h3>✅ No se detectaron falacias ni sesgos significativos</h3>
            <p>El argumento parece estar libre de falacias lógicas evidentes y sesgos cognitivos detectables.</p>
        </div>
        """
    
    html += "</div>"
    return html


def analizar_texto_interface(texto: str) -> str:
    """
    Función principal de la interfaz que analiza el texto
    """
    if not texto or not texto.strip():
        return "<p style='color: red;'>Por favor, ingrese un texto para analizar.</p>"
    
    # Inicializar detector (se cachea en memoria)
    if not hasattr(analizar_texto_interface, 'detector'):
        analizar_texto_interface.detector = DetectorFalaciasSesgos()
    
    # Analizar
    resultado = analizar_texto_interface.detector.analizar(texto)
    
    # Formatear resultado
    return formatear_resultado_html(resultado)


def crear_interfaz():
    """
    Crea la interfaz Gradio
    """
    
    # Ejemplos de argumentos con falacias y sesgos
    ejemplos = [
        ["Eres un ignorante, así que tu opinión sobre economía no vale nada."],
        ["Si permitimos el matrimonio entre personas del mismo sexo, luego querrán casarse con animales, y después con objetos. Terminará siendo un caos total."],
        ["Todos los políticos son corruptos, lo sé porque vi en las noticias que arrestaron a dos alcaldes."],
        ["Los científicos dicen que el cambio climático es real, por lo tanto debe ser cierto."],
        ["Piensa en los niños que sufrirán si no apruebas esta ley. ¿Acaso quieres que sufran?"],
        ["Como siempre pensé, los jóvenes de hoy no quieren trabajar. Esto confirma mis sospechas."],
        ["Después de que comenzó a usar ese producto, le fue mejor en los negocios. Claramente, el producto causó su éxito."],
        ["O estás con nosotros o estás contra nosotros. No hay término medio."]
    ]
    
    # CSS personalizado
    css = """
    .gradio-container {
        font-family: 'Arial', sans-serif;
    }
    .title {
        text-align: center;
        color: #2c3e50;
    }
    .description {
        text-align: center;
        font-size: 1.1em;
        color: #555;
    }
    """
    
    # Crear interfaz
    with gr.Blocks(css=css, title="El Gran Coloso Transdimensional") as demo:
        gr.HTML("""
        <div class="title">
            <h1>🏛️ El Gran Coloso Transdimensional</h1>
            <h2>Purificador de Argumentos Dudosos y Desintegrador de Sofismas Eternos</h2>
        </div>
        """)
        
        gr.Markdown("""
        <div class="description">
        Sistema de Inteligencia Artificial para la detección de <strong>falacias argumentativas</strong> 
        y <strong>sesgos cognitivos</strong> en textos.
        
        **Ingrese un argumento o texto para analizar:**
        </div>
        """)
        
        with gr.Row():
            with gr.Column(scale=1):
                texto_input = gr.Textbox(
                    label="Texto a Analizar",
                    placeholder="Escriba aquí el argumento que desea analizar...",
                    lines=8,
                    max_lines=15
                )
                
                analizar_btn = gr.Button("🔍 Analizar Argumento", variant="primary", size="lg")
                
                gr.Markdown("### 📝 Ejemplos de argumentos con falacias:")
                gr.Examples(
                    examples=ejemplos,
                    inputs=texto_input,
                    label="Haga clic en un ejemplo para cargarlo"
                )
        
        with gr.Row():
            resultado_output = gr.HTML(label="Resultado del Análisis")
        
        # Conectar botón con función
        analizar_btn.click(
            fn=analizar_texto_interface,
            inputs=texto_input,
            outputs=resultado_output
        )
        
        gr.Markdown("""
        ---
        ### ℹ️ Información del Sistema
        
        **Modelo utilizado:** BETO (BERT base Spanish) - `dccuchile/bert-base-spanish-wwm-uncased`
        
        **Basado en:**
        - Ontología de sesgos y falacias (grafo de conocimiento)
        - Axiomas formales del dominio
        - Modelo simbólico y matemático de detección
        
        **Capacidades:**
        - ✅ Detección de falacias formales (Falsa Causa, Generalización Acelerada)
        - ✅ Detección de falacias informales (Ad Hominem, Apelación a la Emoción, Pendiente Resbaladiza, etc.)
        - ✅ Detección de sesgos cognitivos (Confirmación, Disponibilidad, Anclaje, etc.)
        - ✅ Señalamiento de fragmentos problemáticos en el texto
        - ✅ Explicaciones claras del porqué de cada detección
        
        **Leyenda de colores:**
        - 🔴 Rojo (fondo): Falacia detectada
        - 🟡 Amarillo (fondo): Sesgo cognitivo detectado
        """)
    
    return demo


if __name__ == "__main__":
    print("=" * 80)
    print("Iniciando El Gran Coloso Transdimensional")
    print("Purificador de Argumentos Dudosos y Desintegrador de Sofismas Eternos")
    print("=" * 80)
    
    demo = crear_interfaz()
    demo.launch(share=False, server_name="0.0.0.0", server_port=7861)
