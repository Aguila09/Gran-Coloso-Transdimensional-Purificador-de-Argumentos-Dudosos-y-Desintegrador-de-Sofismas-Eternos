# 🏛️ El Gran Coloso Transdimensional

## Purificador de Argumentos Dudosos y Desintegrador de Sofismas Eternos

Sistema de Inteligencia Artificial para la detección automática de **falacias argumentativas** y **sesgos cognitivos** en textos en español.

---

## 🎯 Características

- ✅ **Detección de Falacias Formales**: Falsa Causa, Generalización Acelerada
- ✅ **Detección de Falacias Informales**: Ad Hominem, Apelación a la Emoción, Pendiente Resbaladiza, Apelación a la Autoridad, Hombre de Paja, Falsa Dicotomía
- ✅ **Detección de Sesgos Cognitivos**: Sesgo de Confirmación, Sesgo de Disponibilidad, Sesgo de Anclaje, Sesgo de Autocomplacencia
- ✅ **Interfaz Gráfica Intuitiva**: Interfaz web para ingresar textos y visualizar resultados
- ✅ **Explicaciones Claras**: Cada detección incluye explicación del porqué
- ✅ **Señalamiento Visual**: Fragmentos problemáticos resaltados en el texto
- ✅ **Nivel de Confianza**: Cada detección incluye un score de confianza

---

## 🧠 Arquitectura

El sistema está basado en:

1. **Ontología del Dominio**: Grafo de conocimiento que representa relaciones entre textos, argumentos, falacias y sesgos
2. **Axiomas Formales**: Reglas lógicas que gobiernan las relaciones en la ontología
3. **Modelo Matemático**: Modelo simbólico que combina:
   - Clasificación probabilística
   - Reglas basadas en patrones
   - Razonamiento sobre grafos

### Modelo de IA Utilizado

**BETO (Spanish BERT)**: `dccuchile/bert-base-spanish-wwm-uncased`

- Modelo transformer pre-entrenado en español
- Especializado en comprensión de lenguaje natural
- Utilizado para extracción de características y clasificación

El sistema implementa un enfoque **híbrido** que combina:
- **Machine Learning**: Modelo transformer para análisis semántico
- **Reglas Simbólicas**: Patrones basados en los axiomas de la ontología
- **Razonamiento Lógico**: Aplicación de reglas formales del dominio

---

## 📦 Instalación

### Requisitos Previos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)

### Pasos de Instalación

1. **Clonar el repositorio**:
```bash
git clone https://github.com/Aguila09/Gran-Coloso-Transdimensional-Purificador-de-Argumentos-Dudosos-y-Desintegrador-de-Sofismas-Eternos.git
cd Gran-Coloso-Transdimensional-Purificador-de-Argumentos-Dudosos-y-Desintegrador-de-Sofismas-Eternos
```

2. **Instalar dependencias**:
```bash
pip install -r requirements.txt
```

---

## 🚀 Uso

### Ejecutar la Interfaz Gráfica

```bash
python app.py
```

Esto iniciará un servidor web local. Abra su navegador en:
```
http://localhost:7860
```

### Uso desde Código Python

```python
from detector import DetectorFalaciasSesgos

# Crear instancia del detector
detector = DetectorFalaciasSesgos()

# Analizar un texto
texto = "Eres un ignorante, así que tu opinión no vale nada."
resultado = detector.analizar(texto)

# Revisar resultados
print(f"Falacias detectadas: {len(resultado.falacias_detectadas)}")
for falacia in resultado.falacias_detectadas:
    print(f"  - {falacia.get_tipo()}: {falacia.explicacion}")
    print(f"    Confianza: {falacia.confianza:.2%}")
```

---

## 📚 Estructura del Proyecto

```
.
├── app.py                  # Interfaz gráfica Gradio
├── detector.py             # Motor de detección principal
├── ontology.py             # Clases de la ontología del dominio
├── requirements.txt        # Dependencias del proyecto
├── test_detector.py        # Tests del sistema
├── Informacion/            # Documentación del dominio
│   ├── Ontologia.txt       # Grafo de conocimiento
│   ├── blog_axiomas_grafo_full.html
│   ├── Modelo_simbólico__modelo_matemático_.pdf
│   └── ...
└── README.md              # Este archivo
```

---

## 🧪 Ejemplos de Uso

### Ejemplo 1: Falacia Ad Hominem
**Entrada**: "Eres un ignorante, así que tu opinión sobre economía no vale nada."

**Salida**:
- **Falacia Detectada**: Ad Hominem
- **Explicación**: Ataque a la persona en lugar de refutar su argumento
- **Confianza**: 75%

### Ejemplo 2: Pendiente Resbaladiza
**Entrada**: "Si permitimos el matrimonio entre personas del mismo sexo, luego querrán casarse con animales, y después con objetos. Terminará siendo un caos total."

**Salida**:
- **Falacia Detectada**: Pendiente Resbaladiza
- **Explicación**: Se sugiere que una acción llevará inevitablemente a consecuencias extremas sin justificación
- **Confianza**: 70%

### Ejemplo 3: Sesgo de Confirmación
**Entrada**: "Como siempre pensé, los jóvenes de hoy no quieren trabajar. Esto confirma mis sospechas."

**Salida**:
- **Sesgo Detectado**: Sesgo de Confirmación
- **Explicación**: Tendencia a buscar, interpretar y recordar información que confirma creencias previas
- **Confianza**: 75%

---

## 🔬 Fundamentos Teóricos

El sistema se basa en la documentación contenida en la carpeta `Informacion/`:

1. **Ontología**: Define las entidades del dominio (Texto, Argumento, Premisa, Falacia, Sesgo, etc.) y sus relaciones

2. **Axiomas**: Reglas formales que gobiernan el comportamiento del sistema:
   - Todo argumento se forma de premisas y conclusión
   - Las falacias pueden ser formales o informales
   - Los sesgos se clasifican en perceptivos, motivacionales o de memoria
   - La detección requiere evidencia y confianza mínima

3. **Modelo Matemático**: Formalización que incluye:
   - Funciones de score probabilístico
   - Umbrales de decisión
   - Propagación en grafos de conocimiento
   - Métricas de evaluación (Precisión, Recall, F1-Score)

---

## 🛠️ Tecnologías Utilizadas

- **Python 3.8+**: Lenguaje principal
- **Transformers (HuggingFace)**: Framework de ML para modelos de lenguaje
- **PyTorch**: Backend de deep learning
- **Gradio**: Framework para interfaces web interactivas
- **NumPy**: Computación numérica
- **BETO**: Modelo transformer en español

---

## 📊 Tipos de Falacias Detectadas

### Falacias Formales
- **Falsa Causa**: Asumir causalidad por correlación temporal
- **Generalización Acelerada**: Concluir regla general de casos insuficientes

### Falacias Informales
- **Ad Hominem**: Atacar a la persona en lugar del argumento
- **Apelación a la Emoción**: Usar emociones en lugar de lógica
- **Apelación a la Autoridad**: Apelar a autoridad sin evidencia
- **Pendiente Resbaladiza**: Sugerir consecuencias extremas sin justificación
- **Falsa Dicotomía**: Presentar solo dos opciones cuando hay más
- **Hombre de Paja**: Distorsionar el argumento del oponente

---

## 🧠 Tipos de Sesgos Cognitivos Detectados

### Sesgos Perceptivos
- **Sesgo de Confirmación**: Buscar información que confirme creencias previas
- **Sesgo de Disponibilidad**: Juzgar probabilidad por facilidad de recordar ejemplos

### Sesgos Motivacionales
- **Sesgo de Autocomplacencia**: Atribuir éxitos a uno mismo y fracasos a factores externos

### Sesgos de Memoria
- **Sesgo de Anclaje**: Dependencia excesiva de la primera información recibida

---

## 🤝 Contribuciones

Este proyecto está abierto a contribuciones. Para contribuir:

1. Fork el repositorio
2. Cree una rama para su feature (`git checkout -b feature/AmazingFeature`)
3. Commit sus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abra un Pull Request

---

## 📝 Licencia

Este proyecto está desarrollado como parte de un trabajo académico.

---

## 👤 Autor

Victor Alejandro Rivera Avila

---

## 🙏 Agradecimientos

- Ontología y modelo matemático basados en investigación académica
- Modelo BETO desarrollado por dccuchile
- Framework Gradio por HuggingFace

---

## 📧 Contacto

Para preguntas, sugerencias o reportar problemas, por favor abra un issue en GitHub.
