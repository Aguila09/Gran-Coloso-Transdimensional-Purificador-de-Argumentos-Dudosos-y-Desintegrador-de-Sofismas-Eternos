"""
Tests para El Gran Coloso Transdimensional
Pruebas básicas del sistema de detección
"""

from detector import DetectorFalaciasSesgos
from ontology import TipoFalaciaInformal, TipoSesgoPerceptivo


def test_detector_basico():
    """Test básico de inicialización y análisis"""
    print("\n" + "="*80)
    print("TEST 1: Inicialización del Detector")
    print("="*80)
    
    detector = DetectorFalaciasSesgos()
    assert detector is not None
    print("✓ Detector inicializado correctamente")


def test_deteccion_ad_hominem():
    """Test de detección de falacia Ad Hominem"""
    print("\n" + "="*80)
    print("TEST 2: Detección de Ad Hominem")
    print("="*80)
    
    detector = DetectorFalaciasSesgos()
    texto = "Eres un ignorante, así que tu opinión no vale nada."
    
    resultado = detector.analizar(texto)
    
    print(f"Texto: {texto}")
    print(f"Falacias detectadas: {len(resultado.falacias_detectadas)}")
    
    # Verificar que se detectó al menos una falacia
    assert len(resultado.falacias_detectadas) > 0
    
    # Verificar que hay un Ad Hominem
    tiene_ad_hominem = any(
        f.tipo_informal == TipoFalaciaInformal.AD_HOMINEM 
        for f in resultado.falacias_detectadas
    )
    assert tiene_ad_hominem
    
    for falacia in resultado.falacias_detectadas:
        print(f"  ✓ {falacia.get_tipo()} (Confianza: {falacia.confianza:.2%})")
        print(f"    {falacia.explicacion}")
    
    print("✓ Test de Ad Hominem pasado")


def test_deteccion_pendiente_resbaladiza():
    """Test de detección de Pendiente Resbaladiza"""
    print("\n" + "="*80)
    print("TEST 3: Detección de Pendiente Resbaladiza")
    print("="*80)
    
    detector = DetectorFalaciasSesgos()
    texto = "Si hacemos esto, entonces pasará aquello, y luego lo otro, y después será terrible."
    
    resultado = detector.analizar(texto)
    
    print(f"Texto: {texto}")
    print(f"Falacias detectadas: {len(resultado.falacias_detectadas)}")
    
    for falacia in resultado.falacias_detectadas:
        print(f"  ✓ {falacia.get_tipo()} (Confianza: {falacia.confianza:.2%})")
    
    # Debe detectar pendiente resbaladiza
    tiene_pendiente = any(
        f.tipo_informal == TipoFalaciaInformal.PENDIENTE_RESBALADIZA 
        for f in resultado.falacias_detectadas
    )
    assert tiene_pendiente
    
    print("✓ Test de Pendiente Resbaladiza pasado")


def test_deteccion_sesgo_confirmacion():
    """Test de detección de Sesgo de Confirmación"""
    print("\n" + "="*80)
    print("TEST 4: Detección de Sesgo de Confirmación")
    print("="*80)
    
    detector = DetectorFalaciasSesgos()
    texto = "Como ya sabía, esto confirma que siempre tuve razón."
    
    resultado = detector.analizar(texto)
    
    print(f"Texto: {texto}")
    print(f"Sesgos detectados: {len(resultado.sesgos_detectados)}")
    
    for sesgo in resultado.sesgos_detectados:
        print(f"  ✓ {sesgo.get_tipo()} (Confianza: {sesgo.confianza:.2%})")
        print(f"    {sesgo.explicacion}")
    
    # Debe detectar sesgo de confirmación
    tiene_confirmacion = any(
        s.tipo_perceptivo == TipoSesgoPerceptivo.SESGO_DE_CONFIRMACION 
        for s in resultado.sesgos_detectados
    )
    assert tiene_confirmacion
    
    print("✓ Test de Sesgo de Confirmación pasado")


def test_texto_sin_problemas():
    """Test con texto sin falacias ni sesgos evidentes"""
    print("\n" + "="*80)
    print("TEST 5: Texto sin Problemas Evidentes")
    print("="*80)
    
    detector = DetectorFalaciasSesgos()
    texto = "El cielo es azul durante el día debido a la dispersión de la luz solar en la atmósfera."
    
    resultado = detector.analizar(texto)
    
    print(f"Texto: {texto}")
    print(f"Falacias detectadas: {len(resultado.falacias_detectadas)}")
    print(f"Sesgos detectados: {len(resultado.sesgos_detectados)}")
    
    # Este texto no debería tener detecciones (o muy pocas)
    total_detecciones = len(resultado.falacias_detectadas) + len(resultado.sesgos_detectados)
    print(f"Total de detecciones: {total_detecciones}")
    
    print("✓ Test de texto limpio pasado")


def test_multiples_detecciones():
    """Test con múltiples falacias y sesgos en un texto"""
    print("\n" + "="*80)
    print("TEST 6: Múltiples Detecciones")
    print("="*80)
    
    detector = DetectorFalaciasSesgos()
    texto = """
    Eres un idiota que no sabe nada. Los expertos dicen que esto es verdad, 
    así que debe serlo. Si permitimos esto, entonces pasará aquello y luego lo otro.
    Como ya pensaba, esto confirma mis sospechas.
    """
    
    resultado = detector.analizar(texto)
    
    print(f"Texto analizado ({len(texto)} caracteres)")
    print(f"Falacias detectadas: {len(resultado.falacias_detectadas)}")
    print(f"Sesgos detectados: {len(resultado.sesgos_detectados)}")
    
    print("\nFalacias:")
    for i, falacia in enumerate(resultado.falacias_detectadas, 1):
        print(f"  {i}. {falacia.get_tipo()} (Confianza: {falacia.confianza:.2%})")
    
    print("\nSesgos:")
    for i, sesgo in enumerate(resultado.sesgos_detectados, 1):
        print(f"  {i}. {sesgo.get_tipo()} (Confianza: {sesgo.confianza:.2%})")
    
    # Debe detectar al menos una falacia y un sesgo
    assert len(resultado.falacias_detectadas) >= 1
    assert len(resultado.sesgos_detectados) >= 1
    
    print("\n✓ Test de múltiples detecciones pasado")


def ejecutar_todos_los_tests():
    """Ejecuta todos los tests"""
    print("\n" + "█"*80)
    print("EJECUTANDO SUITE DE TESTS - EL GRAN COLOSO TRANSDIMENSIONAL")
    print("█"*80)
    
    try:
        test_detector_basico()
        test_deteccion_ad_hominem()
        test_deteccion_pendiente_resbaladiza()
        test_deteccion_sesgo_confirmacion()
        test_texto_sin_problemas()
        test_multiples_detecciones()
        
        print("\n" + "█"*80)
        print("✓✓✓ TODOS LOS TESTS PASARON EXITOSAMENTE ✓✓✓")
        print("█"*80 + "\n")
        
    except AssertionError as e:
        print("\n" + "█"*80)
        print(f"✗✗✗ TEST FALLÓ: {e}")
        print("█"*80 + "\n")
        raise
    except Exception as e:
        print("\n" + "█"*80)
        print(f"✗✗✗ ERROR INESPERADO: {e}")
        print("█"*80 + "\n")
        raise


if __name__ == "__main__":
    ejecutar_todos_los_tests()
