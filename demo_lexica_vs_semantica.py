#!/usr/bin/env python3
"""
Demonstração das Diferenças entre Análise Léxica e Semântica
Exemplos práticos mostrando quando cada método é mais eficaz
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from detector_compacto import CompactPlagiarismDetector, SemanticPlagiarismDetector, SEMANTIC_AVAILABLE

def demo_differences():
    """Demonstra as diferenças entre análise léxica e semântica"""
    
    print("🔍 DEMONSTRAÇÃO: ANÁLISE LÉXICA vs SEMÂNTICA")
    print("=" * 60)
    
    # Documento base
    base_doc = {
        'id': 'descobrimento',
        'title': 'Descobrimento do Brasil',
        'content': '''Pedro Álvares Cabral comandou a expedição portuguesa que chegou ao Brasil 
        em 22 de abril de 1500, marcando o início da colonização portuguesa na América do Sul. 
        A esquadra de Cabral estava originalmente destinada às Índias, mas acabou descobrindo 
        as terras brasileiras durante a viagem.'''
    }
    
    # Diferentes tipos de texto para análise
    test_cases = [
        {
            'name': 'CÓPIA DIRETA',
            'text': 'Pedro Álvares Cabral comandou a expedição portuguesa que chegou ao Brasil em 22 de abril de 1500.',
            'description': 'Texto idêntico ao original'
        },
        {
            'name': 'PARÁFRASE SIMPLES',
            'text': 'Cabral liderou a expedição lusitana que alcançou terras brasileiras no dia 22 de abril de 1500.',
            'description': 'Mesmo conteúdo, palavras diferentes'
        },
        {
            'name': 'REFORMULAÇÃO SEMÂNTICA',
            'text': 'O navegador português chegou às terras sul-americanas no final do século XV, iniciando a presença lusitana no continente.',
            'description': 'Significado similar, estrutura completamente diferente'
        },
        {
            'name': 'CONTEXTO RELACIONADO',
            'text': 'A chegada dos europeus ao Novo Mundo transformou completamente a história da América.',
            'description': 'Tema relacionado, mas conteúdo diferente'
        },
        {
            'name': 'TEXTO NÃO RELACIONADO',
            'text': 'A culinária italiana é conhecida mundialmente por sua diversidade e sabor único.',
            'description': 'Completamente diferente'
        }
    ]
    
    # Inicializa detectores
    print("🔧 Inicializando detectores...")
    lexical_detector = CompactPlagiarismDetector()
    lexical_detector.load_documents([base_doc])
    
    semantic_detector = None
    if SEMANTIC_AVAILABLE:
        try:
            semantic_detector = SemanticPlagiarismDetector()
            semantic_detector.load_documents([base_doc])
            print("✅ Ambos os detectores carregados")
        except Exception as e:
            print(f"⚠️ Detector semântico não disponível: {e}")
    else:
        print("⚠️ Dependências semânticas não instaladas")
    
    print("\n📊 RESULTADOS COMPARATIVOS")
    print("-" * 60)
    
    # Tabela de resultados
    print(f"{'TIPO':<20} {'LÉXICA':<10} {'SEMÂNTICA':<12} {'DIFERENÇA':<10}")
    print("-" * 60)
    
    for case in test_cases:
        # Análise léxica
        lexical_results = lexical_detector.detect(case['text'])
        lexical_score = lexical_results[0].similarity if lexical_results else 0
        
        # Análise semântica
        semantic_score = 0
        if semantic_detector:
            try:
                semantic_results = semantic_detector.detect_semantic(case['text'])
                semantic_score = semantic_results[0].similarity if semantic_results else 0
            except:
                semantic_score = 0
        
        # Diferença
        difference = abs(semantic_score - lexical_score)
        
        print(f"{case['name']:<20} {lexical_score:<10.1f}% {semantic_score:<12.1f}% {difference:<10.1f}%")
    
    print("\n💡 ANÁLISE DOS RESULTADOS")
    print("-" * 60)
    
    print("🔤 ANÁLISE LÉXICA (TF-IDF):")
    print("  • Melhor para: Cópia direta, texto literal")
    print("  • Detecta: Palavras e frases idênticas")
    print("  • Limitação: Não entende sinônimos ou paráfrases")
    
    print("\n🧠 ANÁLISE SEMÂNTICA (Embeddings):")
    print("  • Melhor para: Paráfrases, sinônimos, contexto")
    print("  • Detecta: Significado similar mesmo com palavras diferentes")
    print("  • Vantagem: Entende contexto e relações semânticas")
    
    print("\n🎯 RECOMENDAÇÃO:")
    print("  • Use AMBAS as análises para detecção completa")
    print("  • Léxica: Detecta plágio direto")
    print("  • Semântica: Detecta plágio sofisticado")
    print("  • Combinação: Cobertura total de casos")


def demo_practical_examples():
    """Exemplos práticos de uso"""
    
    print("\n\n🎓 EXEMPLOS PRÁTICOS DE USO")
    print("=" * 60)
    
    scenarios = [
        {
            'title': 'TRABALHO ESCOLAR',
            'original': 'A Proclamação da República ocorreu em 15 de novembro de 1889.',
            'suspicious': 'Em 15 de novembro de 1889 aconteceu a Proclamação da República.',
            'analysis': 'Léxica detecta facilmente (alta similaridade de palavras)'
        },
        {
            'title': 'PARÁFRASE SOFISTICADA',
            'original': 'Dom Pedro I proclamou a independência do Brasil.',
            'suspicious': 'O primeiro imperador brasileiro declarou a autonomia nacional.',
            'analysis': 'Semântica detecta melhor (mesmo significado, palavras diferentes)'
        },
        {
            'title': 'REFORMULAÇÃO COMPLEXA',
            'original': 'A Guerra do Paraguai durou de 1864 a 1870.',
            'suspicious': 'O conflito com o Paraguai se estendeu por seis anos no século XIX.',
            'analysis': 'Apenas semântica detecta (contexto similar, estrutura diferente)'
        }
    ]
    
    for scenario in scenarios:
        print(f"\n📌 {scenario['title']}")
        print(f"Original: {scenario['original']}")
        print(f"Suspeito: {scenario['suspicious']}")
        print(f"Análise: {scenario['analysis']}")


if __name__ == "__main__":
    demo_differences()
    demo_practical_examples()
    
    print("\n\n🚀 PRÓXIMOS PASSOS")
    print("=" * 60)
    print("1. Execute: streamlit run detector_compacto.py")
    print("2. Teste os exemplos acima na interface")
    print("3. Compare os resultados das duas abas")
    print("4. Observe as diferenças nos scores")
    print("\n✨ Sistema pronto para detecção completa de plágio!")
