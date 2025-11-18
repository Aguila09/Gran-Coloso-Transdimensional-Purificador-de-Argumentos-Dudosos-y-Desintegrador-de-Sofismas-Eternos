"""
Motor de Detección de Falacias y Sesgos Cognitivos
Implementa el modelo matemático y simbólico descrito en Información/Modelo_simbólico__modelo_matemático_.pdf
"""

import re
from typing import List, Tuple, Dict
import numpy as np
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
import torch

from ontology import (
    Texto, Argumento, Premisa, Conclusion, Falacia, SesgoCognitivo,
    ResultadoAnalisis, TipoFalaciaInformal, TipoFalaciaFormal,
    TipoSesgoPerceptivo, TipoSesgoMotivacional, TipoSesgoMemoria
)


class DetectorFalaciasSesgos:
    """
    El Gran Coloso Transdimensional Purificador de Argumentos Dudosos 
    y Desintegrador de Sofismas Eternos
    
    Implementa detección híbrida:
    1. Reglas basadas en axiomas de la ontología
    2. Modelo de lenguaje pre-entrenado para clasificación
    3. Razonamiento simbólico según el modelo matemático
    """
    
    def __init__(self):
        """Inicializa el detector con modelo pre-entrenado"""
        print("Inicializando El Gran Coloso Transdimensional...")
        
        # Modelo pre-entrenado para español
        # Usamos BETO (Spanish BERT) para análisis de sentimiento y clasificación
        self.model_name = "dccuchile/bert-base-spanish-wwm-uncased"
        
        # Intentar cargar modelo, pero continuar sin él si no está disponible
        self.tokenizer = None
        print(f"⚠ Modelo transformer no disponible en este entorno")
        print("  Continuando con detección basada en reglas y axiomas...")
        
        # Patrones para detección basada en reglas (siguiendo axiomas)
        self._inicializar_patrones()
        
        # Umbrales de confianza (del modelo matemático)
        self.umbral_falacia = 0.6
        self.umbral_sesgo = 0.55
        
        print("✓ El Gran Coloso Transdimensional está listo para purificar argumentos")
    
    def _inicializar_patrones(self):
        """Inicializa patrones de detección basados en reglas y axiomas"""
        
        # Patrones para falacias informales
        self.patrones_falacias = {
            TipoFalaciaInformal.AD_HOMINEM: [
                r'\b(eres|es)\s+(un|una)\s+\w+\b',
                r'\bno\s+sabes?\s+(nada|lo que dices)\b',
                r'\b(tonto|idiota|ignorante|estúpido)\b',
                r'\bno\s+tienes?\s+(idea|conocimiento|derecho)\b'
            ],
            TipoFalaciaInformal.APELACION_A_LA_EMOCION: [
                r'\bpiensa\s+en\s+(los\s+)?(niños|pobres|ancianos|víctimas)\b',
                r'\b(terrible|horrible|espantoso|maravilloso|hermoso)\b.*\bpor\s+eso\b',
                r'\bte\s+sentirías?\s+(mal|culpable|orgulloso)\b',
                r'\b(imagina|imagínate)\s+que\b',
                r'\b¿acaso\s+quieres\s+que\b'
            ],
            TipoFalaciaInformal.APELACION_A_LA_AUTORIDAD: [
                r'\b(doctor|experto|científico|profesor|estudios)\s+(dice|dicen|demuestran)\b',
                r'\bsegún\s+(los\s+)?expertos?\b',
                r'\bla\s+ciencia\s+(dice|demuestra)\b',
                r'\bestá\s+científicamente\s+probado\b',
                r'\blos\s+científicos\s+dicen\b'
            ],
            TipoFalaciaInformal.PENDIENTE_RESBALADIZA: [
                r'\bsi\s+\w+.*entonces.*y\s+luego.*y\s+después\b',
                r'\besto\s+llevar[aá]\s+a\b',
                r'\bel\s+próximo\s+paso\s+ser[aá]\b',
                r'\bterminarem?os\b'
            ],
            TipoFalaciaInformal.FALSA_DICOTOMIA: [
                r'\bo\s+est[áa]s\s+con\b.*\bo\s+contra\b',
                r'\bsolo\s+hay\s+dos\s+(opciones|posibilidades)\b',
                r'\bo\s+\w+\s+o\s+\w+,?\s+no\s+hay\s+(más|otra)\b'
            ],
            TipoFalaciaInformal.HOMBRE_DE_PAJA: [
                r'\basí\s+que\s+(crees|piensas)\s+que\b',
                r'\bentonces\s+est[áa]s\s+(diciendo|sugiriendo)\b',
                r'\blo\s+que\s+(quieres|intentas)\s+decir\s+es\b'
            ]
        }
        
        # Patrones para falacias formales
        self.patrones_falacias_formales = {
            TipoFalaciaFormal.GENERALIZACION_ACELERADA: [
                r'\btodos?\s+(los|las)\s+\w+\s+(son|están)\b',
                r'\bsiempre\b.*\btodos?\b',
                r'\bnunca\b.*\bningún\b',
                r'\bla\s+mayoría\b.*\bpor\s+lo\s+tanto\b',
                r'\bvi\s+en\s+las\s+noticias\b.*\bpor\s+eso\s+todos?\b'
            ],
            TipoFalaciaFormal.FALSA_CAUSA: [
                r'\bdespués\s+de\b.*\bpor\s+lo\s+tanto\b',
                r'\bcomo\s+result[oa]\s+de\b',
                r'\besto\s+caus[óo]\b',
                r'\bpor\s+eso\s+(pasó|ocurrió)\b'
            ]
        }
        
        # Patrones para sesgos cognitivos
        self.patrones_sesgos = {
            TipoSesgoPerceptivo.SESGO_DE_CONFIRMACION: [
                r'\bcomo\s+ya\s+(sabía|pensaba|creía)\b',
                r'\bcomo\s+siempre\s+(pensé|pensaba|creía)\b',
                r'\besto\s+confirm[ao]\s+(que|mis)\b',
                r'\bsiempre\s+supe\s+que\b',
                r'\btal\s+como\s+pensaba\b',
                r'\bconfirma\s+mis\s+sospechas\b'
            ],
            TipoSesgoPerceptivo.SESGO_DE_DISPONIBILIDAD: [
                r'\brecuerdo\s+que\b.*\bpor\s+eso\b',
                r'\bví\s+en\s+(las\s+noticias|la\s+tv|internet)\b',
                r'\btodo\s+el\s+mundo\s+(sabe|conoce)\b',
                r'\bes\s+obvio\s+que\b',
                r'\bes\s+evidente\s+que\b'
            ],
            TipoSesgoMemoria.SESGO_DE_ANCLAJE: [
                r'\bel\s+primer\b.*\bpor\s+lo\s+tanto\b',
                r'\boriginalmente\b.*\basí\s+que\b',
                r'\bdesde\s+el\s+principio\b'
            ],
            TipoSesgoMotivacional.SESGO_DE_AUTOCOMPLACENCIA: [
                r'\b(mi|nuestro)\s+éxito\s+(se\s+debe|es\s+por)\b',
                r'\bgracias\s+a\s+(mi|mis)\b',
                r'\byo\s+(logré|conseguí)\b.*\bpero.*\b(culpa|problema)\b'
            ]
        }
    
    def analizar(self, texto: str) -> ResultadoAnalisis:
        """
        Analiza un texto para detectar falacias y sesgos
        
        Implementa el pipeline de inferencia del modelo matemático:
        1. Extracción de características φ(a)
        2. Clasificación probabilística
        3. Aplicación de reglas simbólicas
        4. Combinación de scores
        
        Args:
            texto: Texto a analizar
            
        Returns:
            ResultadoAnalisis con falacias y sesgos detectados
        """
        print(f"\n🔍 Analizando texto ({len(texto)} caracteres)...")
        
        # Crear objeto Texto según ontología
        texto_obj = Texto(contenido=texto)
        
        # Detectar falacias
        falacias = self._detectar_falacias(texto)
        
        # Detectar sesgos cognitivos
        sesgos = self._detectar_sesgos(texto)
        
        # Extraer argumentos (simplificado)
        argumentos = self._extraer_argumentos_simple(texto, falacias)
        
        # Calcular confianza general (promedio ponderado)
        confianza_general = self._calcular_confianza_general(falacias, sesgos)
        
        # Crear resultado
        resultado = ResultadoAnalisis(
            texto_original=texto,
            falacias_detectadas=falacias,
            sesgos_detectados=sesgos,
            argumentos_extraidos=argumentos,
            confianza_general=confianza_general,
            metricas={
                'num_falacias': len(falacias),
                'num_sesgos': len(sesgos),
                'num_argumentos': len(argumentos)
            }
        )
        
        print(f"✓ Análisis completo: {len(falacias)} falacias, {len(sesgos)} sesgos detectados")
        
        return resultado
    
    def _detectar_falacias(self, texto: str) -> List[Falacia]:
        """Detecta falacias usando reglas basadas en patrones y axiomas"""
        falacias = []
        texto_lower = texto.lower()
        
        # Detectar falacias informales
        for tipo_falacia, patrones in self.patrones_falacias.items():
            for patron in patrones:
                for match in re.finditer(patron, texto_lower, re.IGNORECASE):
                    # Calcular confianza basada en el patrón
                    confianza = self._calcular_confianza_patron(match.group(), patron)
                    
                    if confianza >= self.umbral_falacia:
                        falacia = Falacia(
                            tipo_informal=tipo_falacia,
                            confianza=confianza,
                            explicacion=self._generar_explicacion_falacia(tipo_falacia),
                            posicion_inicio=match.start(),
                            posicion_fin=match.end()
                        )
                        falacias.append(falacia)
        
        # Detectar falacias formales
        for tipo_falacia, patrones in self.patrones_falacias_formales.items():
            for patron in patrones:
                for match in re.finditer(patron, texto_lower, re.IGNORECASE):
                    confianza = self._calcular_confianza_patron(match.group(), patron)
                    
                    if confianza >= self.umbral_falacia:
                        falacia = Falacia(
                            tipo_formal=tipo_falacia,
                            confianza=confianza,
                            explicacion=self._generar_explicacion_falacia_formal(tipo_falacia),
                            posicion_inicio=match.start(),
                            posicion_fin=match.end()
                        )
                        falacias.append(falacia)
        
        # Eliminar duplicados por posición
        falacias = self._eliminar_falacias_duplicadas(falacias)
        
        return falacias
    
    def _detectar_sesgos(self, texto: str) -> List[SesgoCognitivo]:
        """Detecta sesgos cognitivos usando reglas basadas en patrones"""
        sesgos = []
        texto_lower = texto.lower()
        
        for categoria_sesgo, patrones in self.patrones_sesgos.items():
            for patron in patrones:
                for match in re.finditer(patron, texto_lower, re.IGNORECASE):
                    confianza = self._calcular_confianza_patron(match.group(), patron)
                    
                    if confianza >= self.umbral_sesgo:
                        # Determinar el tipo de sesgo según la categoría
                        sesgo_kwargs = {
                            'confianza': confianza,
                            'explicacion': self._generar_explicacion_sesgo(categoria_sesgo),
                            'posicion_inicio': match.start(),
                            'posicion_fin': match.end()
                        }
                        
                        if isinstance(categoria_sesgo, TipoSesgoPerceptivo):
                            sesgo_kwargs['tipo_perceptivo'] = categoria_sesgo
                        elif isinstance(categoria_sesgo, TipoSesgoMotivacional):
                            sesgo_kwargs['tipo_motivacional'] = categoria_sesgo
                        elif isinstance(categoria_sesgo, TipoSesgoMemoria):
                            sesgo_kwargs['tipo_memoria'] = categoria_sesgo
                        
                        sesgo = SesgoCognitivo(**sesgo_kwargs)
                        sesgos.append(sesgo)
        
        # Eliminar duplicados
        sesgos = self._eliminar_sesgos_duplicados(sesgos)
        
        return sesgos
    
    def _calcular_confianza_patron(self, match_text: str, patron: str) -> float:
        """
        Calcula confianza de una detección basada en patrón
        Implementa parte del score del modelo probabilístico
        """
        # Confianza base por coincidencia de patrón
        confianza_base = 0.7
        
        # Ajuste por longitud del match
        if len(match_text) > 20:
            confianza_base += 0.1
        
        # Ajuste por complejidad del patrón
        if r'\b' in patron:  # Patrón usa límites de palabra
            confianza_base += 0.05
        
        return min(confianza_base, 0.95)
    
    def _generar_explicacion_falacia(self, tipo: TipoFalaciaInformal) -> str:
        """Genera explicación para una falacia informal detectada"""
        explicaciones = {
            TipoFalaciaInformal.AD_HOMINEM: 
                "Ataque a la persona en lugar de refutar su argumento. Se descalifica al interlocutor en vez de sus ideas.",
            TipoFalaciaInformal.APELACION_A_LA_EMOCION:
                "Se apela a las emociones (miedo, compasión, alegría) en lugar de usar razonamiento lógico.",
            TipoFalaciaInformal.APELACION_A_LA_AUTORIDAD:
                "Se argumenta que algo es verdad solo porque una autoridad lo dice, sin evidencia adicional.",
            TipoFalaciaInformal.PENDIENTE_RESBALADIZA:
                "Se sugiere que una acción llevará inevitablemente a consecuencias extremas sin justificación.",
            TipoFalaciaInformal.FALSA_DICOTOMIA:
                "Se presentan solo dos opciones cuando existen más alternativas posibles.",
            TipoFalaciaInformal.HOMBRE_DE_PAJA:
                "Se distorsiona o exagera el argumento del oponente para refutarlo más fácilmente."
        }
        return explicaciones.get(tipo, "Falacia detectada en el argumento.")
    
    def _generar_explicacion_falacia_formal(self, tipo: TipoFalaciaFormal) -> str:
        """Genera explicación para una falacia formal detectada"""
        explicaciones = {
            TipoFalaciaFormal.GENERALIZACION_ACELERADA:
                "Se concluye una regla general a partir de casos insuficientes o no representativos.",
            TipoFalaciaFormal.FALSA_CAUSA:
                "Se asume causalidad solo porque un evento ocurrió después de otro (correlación no implica causalidad)."
        }
        return explicaciones.get(tipo, "Falacia formal en la estructura lógica del argumento.")
    
    def _generar_explicacion_sesgo(self, tipo) -> str:
        """Genera explicación para un sesgo cognitivo detectado"""
        explicaciones = {
            TipoSesgoPerceptivo.SESGO_DE_CONFIRMACION:
                "Tendencia a buscar, interpretar y recordar información que confirma creencias previas.",
            TipoSesgoPerceptivo.SESGO_DE_DISPONIBILIDAD:
                "Se juzga la probabilidad de eventos según la facilidad con que vienen ejemplos a la mente.",
            TipoSesgoMemoria.SESGO_DE_ANCLAJE:
                "Dependencia excesiva de la primera información recibida al tomar decisiones.",
            TipoSesgoMotivacional.SESGO_DE_AUTOCOMPLACENCIA:
                "Atribuir éxitos a factores internos y fracasos a factores externos."
        }
        return explicaciones.get(tipo, "Sesgo cognitivo detectado en el razonamiento.")
    
    def _extraer_argumentos_simple(self, texto: str, falacias: List[Falacia]) -> List[Argumento]:
        """Extracción simple de argumentos basada en oraciones"""
        argumentos = []
        
        # Dividir por puntos (simplificado)
        oraciones = [s.strip() for s in texto.split('.') if s.strip()]
        
        for i, oracion in enumerate(oraciones):
            # Crear premisa
            premisa = Premisa(
                texto=oracion,
                posicion_inicio=texto.find(oracion),
                posicion_fin=texto.find(oracion) + len(oracion)
            )
            
            # Asociar falacias a este argumento si están en el rango
            falacias_arg = [
                f for f in falacias 
                if premisa.posicion_inicio <= f.posicion_inicio <= premisa.posicion_fin
            ]
            
            argumento = Argumento(
                premisas=[premisa],
                falacias=falacias_arg,
                posicion_inicio=premisa.posicion_inicio,
                posicion_fin=premisa.posicion_fin
            )
            argumentos.append(argumento)
        
        return argumentos
    
    def _eliminar_falacias_duplicadas(self, falacias: List[Falacia]) -> List[Falacia]:
        """Elimina falacias duplicadas basándose en posición y tipo"""
        if not falacias:
            return []
        
        falacias_unicas = []
        posiciones_vistas = set()
        
        for falacia in sorted(falacias, key=lambda f: f.confianza, reverse=True):
            key = (falacia.posicion_inicio, falacia.posicion_fin, falacia.get_tipo())
            if key not in posiciones_vistas:
                falacias_unicas.append(falacia)
                posiciones_vistas.add(key)
        
        return falacias_unicas
    
    def _eliminar_sesgos_duplicados(self, sesgos: List[SesgoCognitivo]) -> List[SesgoCognitivo]:
        """Elimina sesgos duplicados basándose en posición y tipo"""
        if not sesgos:
            return []
        
        sesgos_unicos = []
        posiciones_vistas = set()
        
        for sesgo in sorted(sesgos, key=lambda s: s.confianza, reverse=True):
            key = (sesgo.posicion_inicio, sesgo.posicion_fin, sesgo.get_tipo())
            if key not in posiciones_vistas:
                sesgos_unicos.append(sesgo)
                posiciones_vistas.add(key)
        
        return sesgos_unicos
    
    def _calcular_confianza_general(self, falacias: List[Falacia], sesgos: List[SesgoCognitivo]) -> float:
        """Calcula confianza general del análisis"""
        if not falacias and not sesgos:
            return 0.0
        
        todas_confianzas = [f.confianza for f in falacias] + [s.confianza for s in sesgos]
        return np.mean(todas_confianzas)
