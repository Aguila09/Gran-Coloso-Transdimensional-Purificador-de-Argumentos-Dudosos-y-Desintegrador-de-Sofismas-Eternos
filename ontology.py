"""
Ontología del Sistema de Detección de Sesgos y Falacias
Basado en el grafo de conocimiento definido en Información/Ontologia.txt
"""

from dataclasses import dataclass, field
from typing import List, Optional, Dict
from enum import Enum


class TipoFalaciaFormal(Enum):
    """Tipos de falacias formales según la ontología"""
    FALSA_CAUSA = "Falsa Causa"
    GENERALIZACION_ACELERADA = "Generalización Acelerada"


class TipoFalaciaInformal(Enum):
    """Tipos de falacias informales según la ontología"""
    AD_HOMINEM = "Ad Hominem"
    APELACION_A_LA_EMOCION = "Apelación a la Emoción"
    PENDIENTE_RESBALADIZA = "Pendiente Resbaladiza"
    APELACION_A_LA_AUTORIDAD = "Apelación a la Autoridad"
    HOMBRE_DE_PAJA = "Hombre de Paja"
    FALSA_DICOTOMIA = "Falsa Dicotomía"
    POST_HOC = "Post Hoc Ergo Propter Hoc"


class TipoSesgoPerceptivo(Enum):
    """Tipos de sesgos perceptivos según la ontología"""
    SESGO_DE_CONFIRMACION = "Sesgo de Confirmación"
    SESGO_DE_DISPONIBILIDAD = "Sesgo de Disponibilidad"


class TipoSesgoMotivacional(Enum):
    """Tipos de sesgos motivacionales según la ontología"""
    SESGO_DE_AUTOCOMPLACENCIA = "Sesgo de Autocomplacencia"


class TipoSesgoMemoria(Enum):
    """Tipos de sesgos de memoria según la ontología"""
    SESGO_DE_ANCLAJE = "Sesgo de Anclaje"


@dataclass
class Evidencia:
    """Representa evidencia que sustenta una premisa"""
    contenido: str
    fiabilidad: float = 0.5  # [0,1] según modelo matemático
    tipo: str = "general"


@dataclass
class Premisa:
    """Representa una premisa de un argumento"""
    texto: str
    evidencias: List[Evidencia] = field(default_factory=list)
    lenguaje_retorico: Optional[str] = None
    posicion_inicio: int = 0
    posicion_fin: int = 0


@dataclass
class Conclusion:
    """Representa la conclusión de un argumento"""
    texto: str
    posicion_inicio: int = 0
    posicion_fin: int = 0


@dataclass
class Falacia:
    """Representa una falacia detectada"""
    tipo_formal: Optional[TipoFalaciaFormal] = None
    tipo_informal: Optional[TipoFalaciaInformal] = None
    confianza: float = 0.0  # Probabilidad de detección
    explicacion: str = ""
    posicion_inicio: int = 0
    posicion_fin: int = 0
    
    def get_tipo(self) -> str:
        """Retorna el tipo de falacia como string"""
        if self.tipo_formal:
            return self.tipo_formal.value
        elif self.tipo_informal:
            return self.tipo_informal.value
        return "Desconocida"


@dataclass
class SesgoCognitivo:
    """Representa un sesgo cognitivo detectado"""
    tipo_perceptivo: Optional[TipoSesgoPerceptivo] = None
    tipo_motivacional: Optional[TipoSesgoMotivacional] = None
    tipo_memoria: Optional[TipoSesgoMemoria] = None
    confianza: float = 0.0
    explicacion: str = ""
    posicion_inicio: int = 0
    posicion_fin: int = 0
    
    def get_tipo(self) -> str:
        """Retorna el tipo de sesgo como string"""
        if self.tipo_perceptivo:
            return self.tipo_perceptivo.value
        elif self.tipo_motivacional:
            return self.tipo_motivacional.value
        elif self.tipo_memoria:
            return self.tipo_memoria.value
        return "Desconocido"


@dataclass
class Argumento:
    """Representa un argumento extraído del texto"""
    premisas: List[Premisa] = field(default_factory=list)
    conclusion: Optional[Conclusion] = None
    falacias: List[Falacia] = field(default_factory=list)
    posicion_inicio: int = 0
    posicion_fin: int = 0


@dataclass
class Fuente:
    """Representa la fuente del texto"""
    nombre: str
    credibilidad: float = 0.5  # [0,1] según modelo matemático
    medio: str = "desconocido"


@dataclass
class Texto:
    """Representa el texto analizado (entidad principal de la ontología)"""
    contenido: str
    argumentos: List[Argumento] = field(default_factory=list)
    sesgos_cognitivos: List[SesgoCognitivo] = field(default_factory=list)
    fuente: Optional[Fuente] = None
    tipo_texto: str = "general"


@dataclass
class ResultadoAnalisis:
    """Resultado del análisis producido por la IA Detectora"""
    texto_original: str
    falacias_detectadas: List[Falacia] = field(default_factory=list)
    sesgos_detectados: List[SesgoCognitivo] = field(default_factory=list)
    argumentos_extraidos: List[Argumento] = field(default_factory=list)
    confianza_general: float = 0.0
    metricas: Dict[str, float] = field(default_factory=dict)
