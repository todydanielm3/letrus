#!/usr/bin/env python3
"""
Testes automatizados simplificados para o Detector de Plágio
"""

def test_text_processor():
    """Testa o processador de texto"""
    print("🧪 Testando CompactTextProcessor...")
    
    from detector_compacto import CompactTextProcessor
    processor = CompactTextProcessor()
    
    # Teste 1: Processamento básico
    text = "Este é um teste simples."
    result = processor.process(text)
    assert isinstance(result, list), "Resultado deve ser lista"
    assert len(result) > 0, "Deve processar algum token"
    assert "teste" in result, "Deve manter palavra importante"
    print("  ✅ Processamento básico")
    
    # Teste 2: Texto vazio
    result = processor.process("")
    assert result == [], "Texto vazio deve retornar lista vazia"
    print("  ✅ Texto vazio")
    
    # Teste 3: N-gramas
    tokens = ["pedro", "alvares", "cabral"]
    ngrams = processor.get_ngrams(tokens, 2)
    assert len(ngrams) == 2, "Deve gerar 2 bigramas"
    assert "pedro alvares" in ngrams, "Deve conter bigrama correto"
    print("  ✅ N-gramas")
    
    print("✅ CompactTextProcessor - Todos os testes passaram!\n")


def test_plagiarism_detector():
    """Testa o detector de plágio"""
    print("🧪 Testando CompactPlagiarismDetector...")
    
    from detector_compacto import CompactPlagiarismDetector
    
    detector = CompactPlagiarismDetector()
    
    # Base de teste
    test_docs = [
        {
            'id': 'doc1',
            'title': 'Brasil Colonial',
            'content': 'Pedro Álvares Cabral descobriu o Brasil em 1500 comandando a esquadra portuguesa.'
        },
        {
            'id': 'doc2',
            'title': 'Independência',
            'content': 'Dom Pedro I proclamou a independência do Brasil em 1822 às margens do Ipiranga.'
        }
    ]
    
    detector.load_documents(test_docs)
    
    # Teste 1: Carregamento
    assert len(detector.documents) == 2, "Deve carregar 2 documentos"
    assert len(detector.doc_vectors) == 2, "Deve gerar 2 vetores"
    print("  ✅ Carregamento de documentos")
    
    # Teste 2: Similaridade alta
    texto_similar = "Cabral descobriu o Brasil em 1500 com a esquadra"
    results = detector.detect(texto_similar, top_k=2)
    assert len(results) > 0, "Deve retornar resultados"
    assert results[0].similarity > 30, f"Similaridade baixa: {results[0].similarity}%"
    print(f"  ✅ Detecção de similaridade: {results[0].similarity}%")
    
    # Teste 3: Similaridade baixa
    texto_diferente = "A culinária italiana é muito diversificada"
    results = detector.detect(texto_diferente, top_k=2)
    assert len(results) > 0, "Deve retornar resultados"
    print(f"  ✅ Texto diferente: {results[0].similarity}%")
    
    print("✅ CompactPlagiarismDetector - Todos os testes passaram!\n")


def test_integration():
    """Testa integração completa"""
    print("🧪 Testando Integração Completa...")
    
    from detector_compacto import CompactPlagiarismDetector, COMPACT_DATABASE
    
    detector = CompactPlagiarismDetector()
    detector.load_documents(COMPACT_DATABASE)
    
    # Teste com base real
    assert len(detector.documents) > 0, "Base de dados deve estar carregada"
    print(f"  ✅ Base carregada: {len(detector.documents)} documentos")
    
    # Teste de detecção
    texto_historia = "Pedro Álvares Cabral chegou ao Brasil em 1500"
    results = detector.detect(texto_historia, top_k=3)
    
    assert len(results) > 0, "Deve detectar similaridades"
    assert results[0].similarity >= 0, "Similaridade deve ser válida"
    
    print(f"  ✅ Detecção funcionando: {results[0].similarity}% com '{results[0].document_title}'")
    print("✅ Integração Completa - Todos os testes passaram!\n")


def test_wikipedia_mock():
    """Testa funcionalidade sem depender da Wikipedia"""
    print("🧪 Testando funcionalidade core...")
    
    from detector_compacto import CompactTextProcessor, get_risk_level
    
    # Teste processador
    processor = CompactTextProcessor()
    tokens = processor.process("História do Brasil é fascinante")
    assert "história" in tokens or "brasil" in tokens, "Deve processar termos importantes"
    print("  ✅ Processamento de texto")
    
    # Teste função auxiliar
    risk, color = get_risk_level(85)
    assert "Alto" in risk, "Deve identificar alto risco"
    print("  ✅ Classificação de risco")
    
    risk, color = get_risk_level(25)
    assert "Baixo" in risk, "Deve identificar baixo risco" 
    print("  ✅ Níveis de risco")
    
    print("✅ Funcionalidades Core - Todos os testes passaram!\n")


def run_all_tests():
    """Executa todos os testes"""
    print("🇧🇷 DETECTOR DE PLÁGIO - TESTES AUTOMATIZADOS")
    print("=" * 60)
    
    tests = [
        test_text_processor,
        test_plagiarism_detector,
        test_integration,
        test_wikipedia_mock
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except Exception as e:
            print(f"❌ FALHA em {test.__name__}: {e}")
            failed += 1
    
    print("=" * 60)
    print(f"📊 RESULTADOS FINAIS:")
    print(f"✅ Testes que passaram: {passed}")
    print(f"❌ Testes que falharam: {failed}")
    print(f"📈 Taxa de sucesso: {passed/(passed+failed)*100:.1f}%")
    
    if failed == 0:
        print("\n🎉 TODOS OS TESTES PASSARAM! Sistema pronto para produção.")
        return 0
    else:
        print(f"\n💔 {failed} teste(s) falharam. Verificar implementação.")
        return 1


if __name__ == "__main__":
    import sys
    exit_code = run_all_tests()
    sys.exit(exit_code)
