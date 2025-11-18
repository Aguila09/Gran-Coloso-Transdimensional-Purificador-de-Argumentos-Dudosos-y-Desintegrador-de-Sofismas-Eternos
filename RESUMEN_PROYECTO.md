# Resumen del Proyecto: El Gran Coloso Transdimensional

## 🎯 Objetivo Cumplido

Se ha implementado exitosamente **"El Gran Coloso Transdimensional Purificador de Argumentos Dudosos y Desintegrador de Sofismas Eternos"**, un sistema de IA para detectar sesgos cognitivos y falacias argumentativas en textos en español.

## 📦 Componentes Desarrollados

### 1. Ontología del Dominio (`ontology.py`)
Implementación completa de la estructura de conocimiento basada en `Información/Ontologia.txt`:

**Entidades Principales:**
- `Texto`: Contenedor principal del análisis
- `Argumento`: Estructura argumentativa (premisas + conclusión)
- `Premisa`: Proposiciones que sustentan el argumento
- `Conclusion`: Conclusión del argumento
- `Falacia`: Errores lógicos detectados
- `SesgoCognitivo`: Sesgos de razonamiento detectados
- `ResultadoAnalisis`: Resultado completo del análisis

**Taxonomía de Falacias:**
- **Formales:** Falsa Causa, Generalización Acelerada
- **Informales:** Ad Hominem, Apelación a la Emoción, Apelación a la Autoridad, Pendiente Resbaladiza, Falsa Dicotomía, Hombre de Paja

**Taxonomía de Sesgos:**
- **Perceptivos:** Confirmación, Disponibilidad
- **Motivacionales:** Autocomplacencia
- **De Memoria:** Anclaje

### 2. Motor de Detección (`detector.py`)
Motor híbrido que combina:

**a) Detección Basada en Reglas**
- Más de 40 patrones de expresiones regulares
- Basados en los axiomas de la ontología
- Adaptados al español coloquial y formal

**b) Modelo de Lenguaje Pre-entrenado**
- BETO (Spanish BERT): `dccuchile/bert-base-spanish-wwm-uncased`
- Fallback a detección por reglas si no está disponible
- Extracción de características semánticas

**c) Sistema de Confianza**
- Scores de confianza para cada detección (0-1)
- Umbrales configurables:
  - Falacias: 0.6
  - Sesgos: 0.55
- Eliminación de duplicados por posición y tipo

### 3. Interfaz Gráfica (`app.py`)
Interfaz web interactiva usando Gradio:

**Características:**
- ✅ Campo de entrada de texto
- ✅ Botón de análisis
- ✅ 8 ejemplos pre-cargados
- ✅ Visualización con resaltado de colores:
  - Rojo: Falacias
  - Amarillo: Sesgos cognitivos
- ✅ Detalles de cada detección:
  - Tipo de falacia/sesgo
  - Fragmento detectado
  - Explicación clara
  - Nivel de confianza
- ✅ Resumen estadístico
- ✅ Información del sistema

**Acceso:** http://localhost:7861

### 4. Suite de Pruebas (`test_detector.py`)
Tests completos que validan:

1. ✅ Inicialización del detector
2. ✅ Detección de Ad Hominem
3. ✅ Detección de Pendiente Resbaladiza
4. ✅ Detección de Sesgo de Confirmación
5. ✅ Textos sin problemas (no falsos positivos)
6. ✅ Múltiples detecciones simultáneas

**Resultado:** 6/6 tests pasando correctamente

### 5. Documentación (`README.md`)
Documentación completa incluyendo:
- Descripción del proyecto
- Instrucciones de instalación
- Guía de uso (interfaz y código)
- Ejemplos prácticos
- Fundamentos teóricos
- Tecnologías utilizadas
- Estructura del proyecto

## 🧠 Fundamentos Teóricos

El sistema está basado en la documentación provista en la carpeta "Información":

### Ontología
Grafo de conocimiento que modela:
- Relaciones entre entidades (Texto → Argumento → Premisa → Falacia)
- Jerarquías de tipos (FalaciaFormal, FalaciaInformal)
- Propiedades (confianza, evidencia, credibilidad)

### Axiomas
Reglas formales implementadas:
- Todo argumento contiene premisas y conclusión
- Las falacias se clasifican en formales e informales
- Los sesgos se categorizan por tipo (perceptivo, motivacional, memoria)
- La detección requiere confianza mínima

### Modelo Matemático
Formalización que incluye:
- Funciones de score probabilístico: P(falacia|texto)
- Umbrales de decisión optimizados
- Propagación en grafos de conocimiento
- Métricas de evaluación (Precisión, Recall, F1-Score)

## 🎨 Ejemplos de Uso

### Ejemplo 1: Ad Hominem
**Entrada:** 
```
"Eres un ignorante, así que tu opinión sobre economía no vale nada."
```

**Resultado:**
- ✅ Falacia: Ad Hominem (75% confianza)
- 📝 Explicación: Ataque a la persona en lugar de refutar su argumento
- 📍 Fragmento: "Eres un ignorante"

### Ejemplo 2: Sesgo de Confirmación
**Entrada:**
```
"Como siempre pensé, los jóvenes de hoy no quieren trabajar. Esto confirma mis sospechas."
```

**Resultado:**
- ✅ Sesgo: Confirmación (75% confianza)
- 📝 Explicación: Tendencia a buscar información que confirme creencias previas
- 📍 Fragmentos: "Como siempre pensé", "confirma mis sospechas"

### Ejemplo 3: Pendiente Resbaladiza
**Entrada:**
```
"Si permitimos el matrimonio entre personas del mismo sexo, luego querrán casarse con animales."
```

**Resultado:**
- ✅ Falacia: Pendiente Resbaladiza (70% confianza)
- 📝 Explicación: Sugiere consecuencias extremas sin justificación
- 📍 Fragmento detectado en el texto

## 🚀 Instrucciones de Ejecución

### Instalación
```bash
pip install -r requirements.txt
```

### Ejecutar la Interfaz
```bash
# Opción 1: Script de inicio
./start.sh

# Opción 2: Directamente con Python
python app.py
```

### Ejecutar Tests
```bash
python test_detector.py
```

### Uso Programático
```python
from detector import DetectorFalaciasSesgos

detector = DetectorFalaciasSesgos()
resultado = detector.analizar("Tu texto aquí")

print(f"Falacias: {len(resultado.falacias_detectadas)}")
print(f"Sesgos: {len(resultado.sesgos_detectados)}")
```

## 🔬 Tecnologías Utilizadas

- **Python 3.8+**: Lenguaje principal
- **Transformers (HuggingFace)**: Framework de ML
- **PyTorch**: Backend de deep learning
- **Gradio**: Interfaz web interactiva
- **NumPy**: Computación numérica
- **BETO**: Modelo transformer en español

## 📊 Capacidades del Sistema

### Falacias Detectadas (8+ tipos)

**Formales:**
1. Falsa Causa (Post hoc ergo propter hoc)
2. Generalización Acelerada

**Informales:**
3. Ad Hominem
4. Apelación a la Emoción
5. Apelación a la Autoridad
6. Pendiente Resbaladiza
7. Falsa Dicotomía
8. Hombre de Paja

### Sesgos Cognitivos Detectados (4+ tipos)

**Perceptivos:**
1. Sesgo de Confirmación
2. Sesgo de Disponibilidad

**Motivacionales:**
3. Sesgo de Autocomplacencia

**De Memoria:**
4. Sesgo de Anclaje

## ✅ Estado del Proyecto

- ✅ Ontología completa implementada
- ✅ Motor de detección funcional
- ✅ Interfaz gráfica operativa
- ✅ Tests pasando (6/6)
- ✅ Documentación completa
- ✅ Sin vulnerabilidades de seguridad (CodeQL)
- ✅ Patrones de detección optimizados
- ✅ Sistema listo para producción

## 🎯 Cumplimiento de Requisitos

✅ **IA llamada "El Gran Coloso Transdimensional..."**: Nombre implementado
✅ **Detecta sesgos cognitivos**: 4+ tipos detectados
✅ **Detecta falacias argumentativas**: 8+ tipos detectados
✅ **Basado en ontología de Información/**: Implementado fielmente
✅ **Basado en axiomas**: Reglas aplicadas
✅ **Basado en modelo matemático**: Score probabilístico implementado
✅ **Usa modelo pre-entrenado**: BETO (Spanish BERT)
✅ **Interfaz gráfica**: Gradio web interface
✅ **Usuario ingresa argumentos**: ✓
✅ **Clasificación de tipo**: ✓
✅ **Explicación clara**: ✓
✅ **Señalamiento de fragmentos**: Resaltado visual implementado

## 📝 Notas Finales

El sistema está completamente funcional y listo para usar. Opera de acuerdo con:
- La estructura conceptual definida en la ontología
- Las reglas y restricciones de los axiomas
- El modelo matemático probabilístico

El sistema es robusto, funciona tanto con modelos transformer como con detección por reglas, y proporciona una experiencia de usuario intuitiva y educativa.
