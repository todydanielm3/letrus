#!/usr/bin/env python3
"""
Demonstração do Detector de Plágio - História do Brasil
"""

from detector_compacto import CompactPlagiarismDetector, load_wikipedia_documents
import wikipedia

def demo_historia_brasil():
    """Demonstra o funcionamento com História do Brasil"""
    
    print("🇧🇷 DETECTOR DE PLÁGIO - HISTÓRIA DO BRASIL")
    print("=" * 50)
    
    # Configura idioma
    wikipedia.set_lang('pt')
    
    # Carrega dados
    print("📖 Carregando base de dados da Wikipedia...")
    documents = load_wikipedia_documents()
    print(f"✅ {len(documents)} artigos sobre História do Brasil carregados\n")
    
    # Inicializa detector
    detector = CompactPlagiarismDetector()
    detector.load_documents(documents)
    print("🤖 Detector inicializado\n")
    
    # Testes com diferentes períodos da História do Brasil
    test_cases = [
        {
            "periodo": "🚢 DESCOBRIMENTO",
            "texto": "Pedro Álvares Cabral comandou a esquadra portuguesa que chegou ao Brasil em 22 de abril de 1500, marcando o início da colonização portuguesa.",
            "tipo": "Alto plágio esperado"
        },
        {
            "periodo": "👑 INDEPENDÊNCIA", 
            "texto": "Dom Pedro I proclamou a independência do Brasil às margens do rio Ipiranga em 7 de setembro de 1822, rompendo os laços com Portugal.",
            "tipo": "Alto plágio esperado"
        },
        {
            "periodo": "⛓️ ABOLIÇÃO",
            "texto": "A Lei Áurea foi assinada pela Princesa Isabel em 1888, abolindo definitivamente a escravidão no território brasileiro.",
            "tipo": "Médio plágio esperado"
        },
        {
            "periodo": "🏛️ REPÚBLICA",
            "texto": "Deodoro da Fonseca liderou o movimento que derrubou a monarquia e instaurou a república em 15 de novembro de 1889.",
            "tipo": "Médio plágio esperado"
        },
        {
            "periodo": "🔧 ERA VARGAS",
            "texto": "Getúlio Vargas governou o Brasil por 15 anos, implementando importantes reformas trabalhistas e industriais.",
            "tipo": "Médio plágio esperado"
        },
        {
            "periodo": "🎨 TEXTO ORIGINAL",
            "texto": "A culinária brasileira contemporânea combina influências indígenas, africanas e europeias de forma única e saborosa.",
            "tipo": "Baixo plágio esperado"
        }
    ]
    
    # Executa testes
    for i, caso in enumerate(test_cases, 1):
        print(f"{i}. {caso['periodo']}")
        print(f"   Texto: \"{caso['texto']}\"")
        print(f"   Expectativa: {caso['tipo']}")
        
        # Analisa
        resultados = detector.detect(caso['texto'], top_k=3)
        
        if resultados:
            melhor = resultados[0]
            print(f"   📊 Maior similaridade: {melhor.similarity}% ({melhor.document_title})")
            
            # Determina nível
            if melhor.similarity >= 70:
                nivel = "🚨 Alto"
                cor = "VERMELHO"
            elif melhor.similarity >= 40:
                nivel = "⚠️ Médio"
                cor = "AMARELO"
            else:
                nivel = "✅ Baixo"
                cor = "VERDE"
                
            print(f"   🎯 Nível de risco: {nivel} ({cor})")
            
            # Top 3 documentos similares
            print(f"   📚 Top 3 documentos similares:")
            for j, res in enumerate(resultados[:3], 1):
                print(f"      {j}. {res.document_title} ({res.similarity}%)")
            
            # Mostra frases encontradas
            if melhor.matched_segments:
                print(f"   🔍 Frases similares: {', '.join(melhor.matched_segments[:2])}")
        else:
            print("   ❌ Nenhuma similaridade detectada")
            
        print()
    
    print("🎉 Demonstração concluída!")
    print("\n💡 Para usar a interface web completa, execute:")
    print("   streamlit run detector_compacto.py")
    print("\n📚 Base de dados atual:")
    print(f"   • {len(documents)} artigos sobre História do Brasil")
    print("   • Cobertura do período colonial até a república")
    print("   • Dados atualizados da Wikipédia em português")

if __name__ == "__main__":
    demo_historia_brasil()
