#!/usr/bin/env python3
"""
Testes automatizados para o Detector de Plágio
Testa todas as funções principais do sistema
"""

import unittest
import sys
import os
from unittest.mock import patch, MagicMock

# Adiciona o diretório atual ao path para importar o detector
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from detector_compacto import (
    CompactTextProcessor, 
    CompactPlagiarismDetector, 
    SimilarityResult,
    COMPACT_DATABASE
)


class TestCompactTextProcessor(unittest.TestCase):
    """Testa o processador de texto"""
    
    def setUp(self):
        self.processor = CompactTextProcessor()
    
    def test_process_basic_text(self):
        """Testa processamento básico de texto"""
        text = "Este é um teste simples de processamento."
        result = self.processor.process(text)
        
        # Deve remover stopwords e pontuação
        self.assertIsInstance(result, list)
        self.assertTrue(len(result) > 0)
        self.assertNotIn("é", result)  # stopword removida
        self.assertNotIn("um", result)  # stopword removida
        self.assertIn("teste", result)  # palavra mantida
        self.assertIn("simples", result)  # palavra mantida
    
    def test_process_empty_text(self):
        """Testa processamento de texto vazio"""
        result = self.processor.process("")
        self.assertEqual(result, [])
        
        result = self.processor.process(None)
        self.assertEqual(result, [])
    
    def test_get_ngrams(self):
        """Testa geração de n-gramas"""
        tokens = ["pedro", "alvares", "cabral", "chegou", "brasil"]
        result = self.processor.get_ngrams(tokens, 3)
        
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 3)  # 5 tokens = 3 trigramas
        self.assertIn("pedro alvares cabral", result)
        self.assertIn("alvares cabral chegou", result)
        self.assertIn("cabral chegou brasil", result)
    
    def test_get_ngrams_insufficient_tokens(self):
        """Testa n-gramas com poucos tokens"""
        tokens = ["pedro", "cabral"]
        result = self.processor.get_ngrams(tokens, 3)
        self.assertEqual(result, [])  # Não há tokens suficientes


class TestCompactPlagiarismDetector(unittest.TestCase):
    """Testa o detector de plágio"""
    
    def setUp(self):
        self.detector = CompactPlagiarismDetector()
        
        # Base de teste pequena
        self.test_documents = [
            {
                'id': 'doc1',
                'title': 'Teste 1',
                'content': 'Pedro Álvares Cabral descobriu o Brasil em 1500 comandando a esquadra portuguesa.'
            },
            {
                'id': 'doc2', 
                'title': 'Teste 2',
                'content': 'A independência do Brasil foi proclamada por Dom Pedro I em 1822.'
            }
        ]
        
        self.detector.load_documents(self.test_documents)
    
    def test_load_documents(self):
        """Testa carregamento de documentos"""
        self.assertEqual(len(self.detector.documents), 2)
        self.assertTrue(len(self.detector.vocab) > 0)
        self.assertEqual(len(self.detector.doc_vectors), 2)
    
    def test_calculate_tfidf(self):
        """Testa cálculo TF-IDF"""
        tokens = ["pedro", "cabral", "brasil"]
        all_docs = [["pedro", "cabral"], ["brasil", "independencia"]]
        
        result = self.detector._calculate_tfidf(tokens, all_docs)
        
        self.assertIsInstance(result, dict)
        self.assertTrue(len(result) > 0)
        # TF-IDF deve ser > 0 para termos presentes
        self.assertTrue(result.get("pedro", 0) > 0)
    
    def test_cosine_similarity(self):
        """Testa similaridade do cosseno"""
        vec1 = {"word1": 0.5, "word2": 0.3, "word3": 0.0}
        vec2 = {"word1": 0.4, "word2": 0.2, "word3": 0.1}
        
        similarity = self.detector._cosine_similarity(vec1, vec2)
        
        self.assertIsInstance(similarity, float)
        self.assertTrue(0 <= similarity <= 1)  # Similaridade entre 0 e 1
    
    def test_detect_high_similarity(self):
        """Testa detecção de alta similaridade"""
        # Texto muito similar ao documento 1
        text = "Pedro Álvares Cabral descobriu o Brasil comandando a esquadra"
        
        results = self.detector.detect(text, top_k=2)
        
        self.assertIsInstance(results, list)
        self.assertTrue(len(results) > 0)
        self.assertIsInstance(results[0], SimilarityResult)
        
        # Primeira similaridade deve ser com doc1
        self.assertEqual(results[0].document_id, 'doc1')
        self.assertTrue(results[0].similarity > 50)  # Alta similaridade
    
    def test_detect_low_similarity(self):
        """Testa detecção de baixa similaridade"""
        # Texto completamente diferente
        text = "A culinária italiana é muito diversificada e saborosa"
        
        results = self.detector.detect(text, top_k=2)
        
        self.assertTrue(len(results) > 0)
        # Similaridade deve ser baixa
        self.assertTrue(results[0].similarity < 30)
    
    def test_detect_empty_text(self):
        """Testa detecção com texto vazio"""
        results = self.detector.detect("", top_k=2)
        # Deve retornar lista vazia ou com similaridades zero
        self.assertIsInstance(results, list)


class TestIntegration(unittest.TestCase):
    """Testes de integração do sistema completo"""
    
    def test_system_integration(self):
        """Testa integração completa do sistema"""
        # Usar base de dados padrão
        detector = CompactPlagiarismDetector()
        detector.load_documents(COMPACT_DATABASE)
        
        # Teste com texto sobre descobrimento
        text = "Cabral chegou ao Brasil em 1500 com sua esquadra portuguesa"
        results = detector.detect(text, top_k=3)
        
        self.assertTrue(len(results) > 0)
        self.assertTrue(results[0].similarity > 0)
        
        # Verificar estrutura do resultado
        result = results[0]
        self.assertTrue(hasattr(result, 'document_id'))
        self.assertTrue(hasattr(result, 'document_title'))
        self.assertTrue(hasattr(result, 'similarity'))
        self.assertTrue(hasattr(result, 'matched_segments'))


class TestWikipediaIntegration(unittest.TestCase):
    """Testa integração com Wikipedia (com mock para evitar dependência de rede)"""
    
    @patch('detector_compacto.wikipedia')
    def test_load_wikipedia_documents_mock(self, mock_wikipedia):
        """Testa carregamento da Wikipedia com mock"""
        # Mock da página da Wikipedia
        mock_page = MagicMock()
        mock_page.title = "Descobrimento do Brasil"
        mock_page.content = "Conteúdo de teste sobre o descobrimento do Brasil" * 50
        mock_page.url = "https://pt.wikipedia.org/wiki/Descobrimento_do_Brasil"
        
        mock_wikipedia.page.return_value = mock_page
        mock_wikipedia.set_lang = MagicMock()
        
        # Importar função de carregamento
        from detector_compacto import load_wikipedia_documents
        
        # Testar carregamento
        documents = load_wikipedia_documents()
        
        # Verificar se foi chamado corretamente
        mock_wikipedia.set_lang.assert_called_with('pt')
        self.assertTrue(len(documents) > 0)


def run_tests():
    """Executa todos os testes"""
    print("🧪 EXECUTANDO TESTES AUTOMATIZADOS")
    print("=" * 50)
    
    # Criar suite de testes
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Adicionar classes de teste
    test_classes = [
        TestCompactTextProcessor,
        TestCompactPlagiarismDetector, 
        TestIntegration,
        TestWikipediaIntegration
    ]
    
    for test_class in test_classes:
        tests = loader.loadTestsFromTestCase(test_class)
        suite.addTests(tests)
    
    # Executar testes
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Relatório final
    print("\n" + "=" * 50)
    print(f"📊 RELATÓRIO FINAL:")
    print(f"✅ Testes executados: {result.testsRun}")
    print(f"❌ Falhas: {len(result.failures)}")
    print(f"⚠️  Erros: {len(result.errors)}")
    
    if result.failures:
        print("\n🔥 FALHAS:")
        for test, traceback in result.failures:
            print(f"- {test}: {traceback}")
    
    if result.errors:
        print("\n💥 ERROS:")
        for test, traceback in result.errors:
            print(f"- {test}: {traceback}")
    
    success = len(result.failures) == 0 and len(result.errors) == 0
    
    if success:
        print("\n🎉 TODOS OS TESTES PASSARAM!")
        return 0
    else:
        print("\n💔 ALGUNS TESTES FALHARAM!")
        return 1


if __name__ == "__main__":
    exit_code = run_tests()
    sys.exit(exit_code)
