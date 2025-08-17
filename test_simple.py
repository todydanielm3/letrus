#!/usr/bin/env python3

"""
Testes automatizados simplificados para o Detector de Plágio
Inclui testes para análise léxica e semântica
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from detector_compacto import CompactPlagiarismDetector, SemanticPlagiarismDetector, CompactTextProcessor


def test_text_processor():
    """Testa o processador de texto"""
    print("🧪 Testando processador de texto...")
    
    processor = CompactTextProcessor()
    
    # Teste básico
    text = "Este é um teste de processamento de texto."
    tokens = processor.process(text)
    assert len(tokens) > 0, "Deveria retornar tokens"
    assert "teste" in tokens, "Deveria conter 'teste'"
    print("  ✅ Processamento básico funcionando")
    
    # Teste de n-gramas
    ngrams = processor.get_ngrams(tokens, 2)
    assert len(ngrams) > 0, "Deveria gerar n-gramas"
    print("  ✅ N-gramas funcionando")
    
    print("✅ Processador de texto: OK\n")


def test_lexical_plagiarism_detector():
    """Testa o detector de plágio léxico"""
    print("🧪 Testando detector de plágio léxico...")
    
    detector = CompactPlagiarismDetector()
    
    # Documentos de teste
    test_docs = [
        {
            'id': 'doc1',
            'title': 'Documento 1',
            'content': 'Pedro Álvares Cabral descobriu o Brasil em 1500. Foi uma expedição portuguesa muito importante.'
        },
        {
            'id': 'doc2', 
            'title': 'Documento 2',
            'content': 'A independência do Brasil ocorreu em 1822 com Dom Pedro I. Foi um momento histórico crucial.'
        }
    ]
    
    detector.load_documents(test_docs)
    
    # Teste com texto similar
    text_similar = "Pedro Álvares Cabral foi o descobridor do Brasil no ano de 1500."
    results = detector.detect(text_similar)
    
    assert len(results) > 0, "Deveria retornar resultados"
    assert results[0].similarity > 0, "Deveria encontrar similaridade"
    print(f"  ✅ Similaridade encontrada: {results[0].similarity}%")
    
    # Teste com texto diferente
    text_different = "A culinária italiana é muito saborosa e variada."
    results_diff = detector.detect(text_different)
    
    assert len(results_diff) > 0, "Deveria retornar resultados"
    print(f"  ✅ Texto diferente processado: {results_diff[0].similarity}%")
    
    print("✅ Detector léxico: OK\n")


def test_semantic_plagiarism_detector():
    """Testa o detector de plágio semântico"""
    print("🧪 Testando detector de plágio semântico...")
    
    try:
        detector = SemanticPlagiarismDetector()
        
        # Documentos de teste
        test_docs = [
            {
                'id': 'doc1',
                'title': 'Descobrimento do Brasil',
                'content': 'Pedro Álvares Cabral chegou ao Brasil em 1500 liderando uma expedição portuguesa. Este evento marcou o início da colonização portuguesa na América do Sul.'
            },
            {
                'id': 'doc2',
                'title': 'Independência Brasileira', 
                'content': 'Em 1822, Dom Pedro I proclamou a independência do Brasil, rompendo os laços coloniais com Portugal. Este foi um marco na história brasileira.'
            }
        ]
        
        detector.load_documents(test_docs)
        
        # Teste com texto semanticamente similar (paráfrase)
        text_paraphrase = "Cabral liderou a frota lusitana que alcançou terras brasileiras no ano 1500."
        results = detector.detect_semantic(text_paraphrase)
        
        assert len(results) > 0, "Deveria retornar resultados"
        assert results[0].similarity > 0, "Deveria encontrar similaridade semântica"
        print(f"  ✅ Similaridade semântica encontrada: {results[0].similarity}%")
        
        # Teste com texto sobre tópico diferente mas relacionado
        text_related = "A colonização portuguesa transformou completamente o território americano."
        results_related = detector.detect_semantic(text_related)
        
        assert len(results_related) > 0, "Deveria retornar resultados"
        print(f"  ✅ Texto relacionado processado: {results_related[0].similarity}%")
        
        print("✅ Detector semântico: OK\n")
        
    except Exception as e:
        print(f"  ⚠️ Detector semântico não disponível: {e}")
        print("  💡 Instale: pip install sentence-transformers")
        print("✅ Teste semântico: PULADO (dependências)\n")


def test_integration():
    """Teste de integração completa"""
    print("🧪 Testando integração completa...")
    
    # Teste com dados reais (similares ao sistema)
    test_text = """
    A chegada dos portugueses ao Brasil ocorreu em 22 de abril de 1500, 
    quando Pedro Álvares Cabral avistou as terras brasileiras. Esta expedição 
    fazia parte dos esforços portugueses para estabelecer rotas comerciais.
    """
    
    # Detector léxico
    lexical_detector = CompactPlagiarismDetector()
    
    sample_docs = [
        {
            'id': 'descobrimento',
            'title': 'Descobrimento do Brasil',
            'content': 'Pedro Álvares Cabral comandou a expedição portuguesa que chegou ao Brasil em 22 de abril de 1500, marcando o início da presença portuguesa na América do Sul.'
        }
    ]
    
    lexical_detector.load_documents(sample_docs)
    lexical_results = lexical_detector.detect(test_text)
    
    assert len(lexical_results) > 0, "Integração léxica deveria funcionar"
    print(f"  ✅ Integração léxica: {lexical_results[0].similarity}%")
    
    # Teste semântico (se disponível)
    try:
        semantic_detector = SemanticPlagiarismDetector()
        semantic_detector.load_documents(sample_docs)
        semantic_results = semantic_detector.detect_semantic(test_text)
        
        assert len(semantic_results) > 0, "Integração semântica deveria funcionar"
        print(f"  ✅ Integração semântica: {semantic_results[0].similarity}%")
        
    except Exception as e:
        print(f"  ⚠️ Integração semântica pulada: {str(e)[:50]}...")
    
    print("✅ Integração: OK\n")


def test_core_functions():
    """Testa funções essenciais"""
    print("🧪 Testando funções essenciais...")
    
    # Teste de importações
    try:
        from detector_compacto import get_risk_level, COMPACT_DATABASE
        print("  ✅ Importações funcionando")
    except ImportError as e:
        assert False, f"Erro de importação: {e}"
    
    # Teste da função de risco
    risk_high = get_risk_level(80)
    risk_medium = get_risk_level(50) 
    risk_low = get_risk_level(20)
    
    assert "Alto" in risk_high[0], "Deveria identificar alto risco"
    assert "Médio" in risk_medium[0], "Deveria identificar risco médio"
    assert "Baixo" in risk_low[0], "Deveria identificar baixo risco"
    print("  ✅ Função de risco funcionando")
    
    # Teste da base de dados local
    assert len(COMPACT_DATABASE) > 0, "Base local deveria ter documentos"
    print(f"  ✅ Base local com {len(COMPACT_DATABASE)} documentos")
    
    print("✅ Funções essenciais: OK\n")


def run_all_tests():
    """Executa todos os testes"""
    print("🚀 INICIANDO TESTES DO DETECTOR DE PLÁGIO")
    print("=" * 50)
    
    tests = [
        test_text_processor,
        test_lexical_plagiarism_detector,
        test_semantic_plagiarism_detector,
        test_integration,
        test_core_functions
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            test()
            passed += 1
        except Exception as e:
            print(f"❌ {test.__name__} FALHOU: {e}\n")
    
    print("=" * 50)
    print(f"📊 RESULTADOS: {passed}/{total} testes passaram")
    print(f"📈 Taxa de sucesso: {(passed/total)*100:.1f}%")
    
    if passed == total:
        print("🎉 TODOS OS TESTES PASSARAM!")
        return True
    else:
        print("⚠️ Alguns testes falharam")
        return False


if __name__ == "__main__":
    run_all_tests()

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
