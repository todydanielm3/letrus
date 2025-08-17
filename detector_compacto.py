"""
Detector de Plágio - Versão Compacta com Wikipédia
Integra tudo em um único arquivo: detector + interface + dados da Wikipedia
Inclui análise léxica (TF-IDF) e semântica (embeddings)
"""

import streamlit as st
import pandas as pd
import re
import string
import math
import wikipedia
from typing import List, Dict, Tuple
from dataclasses import dataclass
from collections import Counter
from datetime import datetime
import json
import os
import pickle
import subprocess
import sys

# Importações básicas do numpy
try:
    import numpy as np
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "numpy"])
    import numpy as np

# Importações opcionais para análise semântica - importação dinâmica
SEMANTIC_AVAILABLE = False

def try_import_semantic_dependencies():
    """Tenta importar dependências semânticas dinamicamente"""
    global SEMANTIC_AVAILABLE
    try:
        from sentence_transformers import SentenceTransformer
        import torch
        SEMANTIC_AVAILABLE = True
        print("✅ Dependências semânticas carregadas")
        return True
    except ImportError as e:
        print("📦 Instalando dependências semânticas...")
        
        try:
            # Instala automaticamente as dependências necessárias
            packages = ['sentence-transformers', 'torch', 'numpy']
            for package in packages:
                print(f"  Instalando {package}...")
                subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            
            # Tenta importar novamente após instalação
            from sentence_transformers import SentenceTransformer
            import torch
            SEMANTIC_AVAILABLE = True
            print("✅ Dependências semânticas instaladas e carregadas!")
            return True
            
        except Exception as install_error:
            print(f"❌ Erro na instalação automática: {install_error}")
            print("🔄 Usando apenas análise léxica...")
            SEMANTIC_AVAILABLE = False
            return False


@dataclass
class SimilarityResult:
    """Resultado da comparação de similaridade"""
    document_id: str
    document_title: str
    document_content: str
    similarity: float
    matched_segments: List[str]


class CompactTextProcessor:
    """Processador de texto simplificado"""
    
    def __init__(self):
        # Stopwords essenciais
        self.stop_words = {
            'a', 'an', 'and', 'are', 'as', 'at', 'be', 'by', 'for', 'from', 'has', 'he', 'in', 'is', 'it',
            'of', 'on', 'that', 'the', 'to', 'was', 'will', 'with', 'this', 'but', 'they', 'have', 'had',
            'o', 'a', 'os', 'as', 'um', 'uma', 'de', 'do', 'da', 'em', 'no', 'na', 'por', 'para', 'com',
            'e', 'ou', 'mas', 'que', 'se', 'eu', 'ele', 'ela', 'ser', 'estar', 'ter', 'muito', 'mais'
        }
    
    def process(self, text: str) -> List[str]:
        """Processa texto e retorna tokens limpos"""
        if not text:
            return []
        
        # Limpa e tokeniza
        text = re.sub(r'[^\w\s]', ' ', text.lower())
        words = [w for w in text.split() if len(w) > 2 and w not in self.stop_words]
        return words
    
    def get_ngrams(self, tokens: List[str], n: int = 3) -> List[str]:
        """Gera n-gramas"""
        if len(tokens) < n:
            return []
        return [' '.join(tokens[i:i+n]) for i in range(len(tokens) - n + 1)]


class CompactPlagiarismDetector:
    """Detector de plágio compacto"""
    
    def __init__(self):
        self.processor = CompactTextProcessor()
        self.documents = []
        self.vocab = set()
        self.doc_vectors = []
    
    def load_documents(self, documents: List[Dict[str, str]]):
        """Carrega documentos"""
        self.documents = documents
        
        # Processa todos os documentos
        all_tokens = []
        for doc in documents:
            tokens = self.processor.process(doc['content'])
            all_tokens.append(tokens)
            self.vocab.update(tokens)
        
        # Calcula vetores TF-IDF simples
        self.doc_vectors = []
        for tokens in all_tokens:
            vector = self._calculate_tfidf(tokens, all_tokens)
            self.doc_vectors.append(vector)
    
    def _calculate_tfidf(self, tokens: List[str], all_docs: List[List[str]]) -> Dict[str, float]:
        """Calcula TF-IDF básico"""
        # TF
        tf = Counter(tokens)
        doc_len = len(tokens)
        for term in tf:
            tf[term] = tf[term] / doc_len
        
        # IDF e TF-IDF
        tfidf = {}
        total_docs = len(all_docs)
        
        for term in self.vocab:
            # IDF
            docs_with_term = sum(1 for doc in all_docs if term in doc)
            idf = math.log(total_docs / max(1, docs_with_term))
            
            # TF-IDF
            tfidf[term] = tf.get(term, 0) * idf
        
        return tfidf
    
    def _cosine_similarity(self, vec1: Dict[str, float], vec2: Dict[str, float]) -> float:
        """Similaridade do cosseno"""
        dot = sum(vec1[t] * vec2[t] for t in self.vocab)
        norm1 = math.sqrt(sum(v**2 for v in vec1.values()))
        norm2 = math.sqrt(sum(v**2 for v in vec2.values()))
        
        return dot / (norm1 * norm2) if norm1 and norm2 else 0
    
    def detect(self, text: str, top_k: int = 5) -> List[SimilarityResult]:
        """Detecta plágio"""
        if not self.documents:
            return []
        
        # Processa texto
        query_tokens = self.processor.process(text)
        query_ngrams = set(self.processor.get_ngrams(query_tokens))
        
        # Calcula vetor TF-IDF da query
        all_tokens = [self.processor.process(doc['content']) for doc in self.documents]
        query_vector = self._calculate_tfidf(query_tokens, all_tokens + [query_tokens])
        
        # Calcula similaridades
        results = []
        for i, doc in enumerate(self.documents):
            # Similaridade
            similarity = self._cosine_similarity(query_vector, self.doc_vectors[i])
            
            # Frases em comum
            doc_tokens = self.processor.process(doc['content'])
            doc_ngrams = set(self.processor.get_ngrams(doc_tokens))
            common_phrases = list(query_ngrams.intersection(doc_ngrams))[:3]
            
            result = SimilarityResult(
                document_id=doc['id'],
                document_title=doc['title'],
                document_content=doc['content'][:300] + "..." if len(doc['content']) > 300 else doc['content'],
                similarity=round(similarity * 100, 2),
                matched_segments=common_phrases
            )
            results.append(result)
        
        # Ordena e retorna
        results.sort(key=lambda x: x.similarity, reverse=True)
        return results[:top_k]


class SemanticPlagiarismDetector:
    """Detector de plágio usando análise semântica com embeddings"""
    
    def __init__(self, model_name: str = 'paraphrase-multilingual-MiniLM-L12-v2'):
        """Inicializa o detector semântico"""
        self.model_name = model_name
        self.model = None
        self.documents = []
        self.document_embeddings = None
        self.cache_file = 'embeddings_cache.pkl'
        
    def _load_model(self):
        """Carrega o modelo de embeddings"""
        # Tenta importar e carregar as dependências
        if not try_import_semantic_dependencies():
            raise ImportError("Dependências semânticas não disponíveis")
            
        if self.model is None:
            try:
                from sentence_transformers import SentenceTransformer
                self.model = SentenceTransformer(self.model_name)
                print(f"✅ Modelo {self.model_name} carregado com sucesso")
            except Exception as e:
                print(f"❌ Erro ao carregar modelo: {e}")
                # Fallback para modelo menor
                try:
                    from sentence_transformers import SentenceTransformer
                    self.model = SentenceTransformer('paraphrase-multilingual-mpnet-base-v2')
                    print("✅ Modelo fallback carregado")
                except:
                    raise Exception("Não foi possível carregar nenhum modelo de embeddings")
    
    def load_documents(self, documents: List[Dict[str, str]]):
        """Carrega documentos e gera embeddings"""
        self.documents = documents
        self._load_model()
        
        # Verifica se existe cache
        if os.path.exists(self.cache_file):
            try:
                with open(self.cache_file, 'rb') as f:
                    cached_data = pickle.load(f)
                
                # Verifica se o cache é válido (mesmo número de documentos)
                if len(cached_data.get('embeddings', [])) == len(documents):
                    self.document_embeddings = cached_data['embeddings']
                    print(f"✅ Embeddings carregados do cache ({len(documents)} documentos)")
                    return
            except Exception as e:
                print(f"⚠️ Erro ao carregar cache: {e}")
        
        # Gera novos embeddings
        print(f"🔄 Gerando embeddings para {len(documents)} documentos...")
        texts = [doc['content'] for doc in documents]
        
        # Processa em lotes para economizar memória
        batch_size = 32
        embeddings = []
        
        for i in range(0, len(texts), batch_size):
            batch = texts[i:i + batch_size]
            batch_embeddings = self.model.encode(batch, convert_to_tensor=False, normalize_embeddings=True)
            embeddings.extend(batch_embeddings)
            print(f"  Processados {min(i + batch_size, len(texts))}/{len(texts)} documentos")
        
        self.document_embeddings = np.array(embeddings)
        
        # Salva no cache
        try:
            with open(self.cache_file, 'wb') as f:
                pickle.dump({'embeddings': self.document_embeddings}, f)
            print(f"💾 Embeddings salvos no cache")
        except Exception as e:
            print(f"⚠️ Erro ao salvar cache: {e}")
    
    def detect_semantic(self, text: str, top_k: int = 5) -> List[SimilarityResult]:
        """Detecta plágio usando análise semântica"""
        if not self.documents or self.document_embeddings is None:
            return []
        
        if self.model is None:
            self._load_model()
        
        # Gera embedding do texto de entrada
        query_embedding = self.model.encode([text], convert_to_tensor=False, normalize_embeddings=True)[0]
        
        # Calcula similaridades
        similarities = np.dot(self.document_embeddings, query_embedding)
        
        # Cria resultados
        results = []
        for i, similarity in enumerate(similarities):
            doc = self.documents[i]
            
            # Encontra segmentos mais similares (aproximação)
            sentences = text.split('.')[:3]  # Primeiras 3 frases
            matched_segments = [s.strip() for s in sentences if len(s.strip()) > 10][:3]
            
            result = SimilarityResult(
                document_id=doc['id'],
                document_title=doc['title'],
                document_content=doc['content'][:300] + "..." if len(doc['content']) > 300 else doc['content'],
                similarity=round(float(similarity) * 100, 2),
                matched_segments=matched_segments
            )
            results.append(result)
        
        # Ordena e retorna
        results.sort(key=lambda x: x.similarity, reverse=True)
        return results[:top_k]


# Configuração da Wikipédia
wikipedia.set_lang('pt')  # Configurar para português

def load_wikipedia_documents() -> List[Dict[str, str]]:
    """Carrega documentos da Wikipédia em português - História do Brasil"""
    
    # Lista de 25 artigos principais sobre História do Brasil (reduzido para performance)
    article_titles = [
        # Período Colonial
        'Descobrimento do Brasil',
        'Pedro Álvares Cabral',
        'Capitanias hereditárias',
        'Governo-geral',
        'Invasões holandesas no Brasil',
        'Entradas e bandeiras',
        'Conjuração Mineira',
        'Conjuração Baiana',
        
        # Império
        'Independência do Brasil',
        'Dom Pedro I do Brasil',
        'Primeiro Reinado',
        'Dom Pedro II do Brasil',
        'Guerra do Paraguai',
        'Abolição da escravatura no Brasil',
        'Proclamação da República do Brasil',
        
        # República
        'Primeira República Brasileira',
        'Guerra de Canudos',
        'Tenentismo',
        'Revolução de 1930',
        'Getúlio Vargas',
        'Estado Novo (Brasil)',
        'Brasil na Segunda Guerra Mundial',
        'Ditadura militar no Brasil',
        'Diretas Já',
        'Nova República'
    ]
    
    documents = []
    successful_loads = 0
    max_docs = 50  # Aumentado para carregar mais documentos
    failed_loads = []
    
    print(f"📖 Carregando {len(article_titles)} artigos sobre História do Brasil...")
    
    for i, title in enumerate(article_titles):
        if successful_loads >= max_docs:
            break
            
        try:
            print(f"  Carregando {i+1}/{len(article_titles)}: {title}")
            
            # Tenta buscar a página
            page = wikipedia.page(title, auto_suggest=True)
            
            # Extrai conteúdo (primeiros 3000 caracteres para melhor qualidade)
            content = page.content[:3000] if len(page.content) > 3000 else page.content
            
            doc = {
                'id': title.lower().replace(' ', '_').replace('ã', 'a').replace('ç', 'c'),
                'title': title,
                'content': content,
                'url': page.url
            }
            documents.append(doc)
            successful_loads += 1
            
        except wikipedia.exceptions.DisambiguationError as e:
            # Se houver desambiguação, pega a primeira opção
            try:
                page = wikipedia.page(e.options[0])
                content = page.content[:2500] if len(page.content) > 2500 else page.content
                
                doc = {
                    'id': title.lower().replace(' ', '_').replace('ã', 'a').replace('ç', 'c'),
                    'title': e.options[0],
                    'content': content,
                    'url': page.url
                }
                documents.append(doc)
                successful_loads += 1
            except:
                print(f"    ❌ Erro na desambiguação: {title}")
                continue
                
        except wikipedia.exceptions.PageError:
            # Se não encontrar a página, tenta uma busca
            try:
                search_results = wikipedia.search(title, results=1)
                if search_results:
                    page = wikipedia.page(search_results[0])
                    content = page.content[:2500] if len(page.content) > 2500 else page.content
                    
                    doc = {
                        'id': title.lower().replace(' ', '_').replace('ã', 'a').replace('ç', 'c'),
                        'title': search_results[0],
                        'content': content,
                        'url': page.url
                    }
                    documents.append(doc)
                    successful_loads += 1
            except:
                print(f"    ❌ Página não encontrada: {title}")
                continue
                
        except Exception as e:
            # Para qualquer outro erro, continua
            print(f"    ❌ Erro inesperado: {title} - {str(e)}")
            continue
    
    print(f"✅ Carregados {successful_loads} de {len(article_titles)} artigos sobre História do Brasil")
    return documents


# Base de dados backup (caso a Wikipedia falhe) - História do Brasil
COMPACT_DATABASE = [
    {
        'id': 'descobrimento_brasil',
        'title': 'Descobrimento do Brasil',
        'content': '''O descobrimento do Brasil refere-se ao episódio de chegada da esquadra portuguesa comandada por Pedro Álvares Cabral em 22 de abril de 1500 às terras que mais tarde seriam chamadas de Brasil. A expedição tinha como destino original as Índias, mas os ventos levaram a frota para oeste, resultando na descoberta acidental do território brasileiro. A terra foi inicialmente chamada de Terra de Vera Cruz e depois Terra de Santa Cruz.'''
    },
    {
        'id': 'independencia_brasil',
        'title': 'Independência do Brasil',
        'content': '''A Independência do Brasil foi um processo que se estendeu de 1821 a 1825 e colocou fim ao domínio político do Reino de Portugal sobre o Brasil. O episódio mais conhecido é o Grito do Ipiranga, proferido por Dom Pedro I em 7 de setembro de 1822, às margens do rio Ipiranga, proclamando a independência. Este evento marca o nascimento do Império do Brasil como nação soberana.'''
    },
    {
        'id': 'abolição_escravatura',
        'title': 'Abolição da Escravatura',
        'content': '''A abolição da escravatura no Brasil foi um processo gradual que culminou com a assinatura da Lei Áurea pela Princesa Isabel em 13 de maio de 1888. Esta lei extinguiu definitivamente a escravidão no país, libertando cerca de 700 mil escravos. O Brasil foi o último país das Américas a abolir a escravidão, após um longo processo de leis graduais como a Lei do Ventre Livre e a Lei dos Sexagenários.'''
    },
    {
        'id': 'proclamacao_republica',
        'title': 'Proclamação da República',
        'content': '''A Proclamação da República Brasileira foi um golpe de estado político-militar que ocorreu em 15 de novembro de 1889, que instaurou a forma federativa presidencialista de governo no Brasil, derrubando a monarquia constitucional parlamentarista do Império do Brasil. Foi liderada pelo Marechal Deodoro da Fonseca e contou com o apoio de republicanos civis e militares positivistas.'''
    },
    {
        'id': 'era_vargas',
        'title': 'Era Vargas',
        'content': '''A Era Vargas foi o período da história do Brasil entre 1930 e 1945, quando Getúlio Vargas governou o país de forma contínua. Este período é dividido em três fases: o Governo Provisório (1930-1934), o Governo Constitucional (1934-1937) e o Estado Novo (1937-1945). Durante este período, o Brasil passou por profundas transformações políticas, econômicas e sociais, incluindo a criação das leis trabalhistas.'''
    }
]


def get_risk_level(score: float) -> Tuple[str, str]:
    """Retorna nível de risco e cor"""
    if score >= 70:
        return "🚨 Alto Risco", "#ff4444"
    elif score >= 40:
        return "⚠️ Risco Médio", "#ffaa00"
    else:
        return "✅ Baixo Risco", "#00dd00"


def main():
    """Interface Streamlit"""
    
    # Configuração
    st.set_page_config(
        page_title="Detector de Plágio",
        page_icon="🔍",
        layout="wide"
    )
    
    # CSS
    st.markdown("""
    <style>
    .main-title {
        text-align: center;
        color: #1f77b4;
        font-size: 2.5rem;
        margin-bottom: 1rem;
    }
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #1f77b4;
        margin: 0.5rem 0;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Header
    st.markdown('<h1 class="main-title">🔍 Detector de Plágio</h1>', unsafe_allow_html=True)
    st.markdown("**Detecte similaridades em textos de forma simples e eficaz**")
    
    # Inicializa detectores
    @st.cache_resource
    def load_detectors():
        lexical_detector = CompactPlagiarismDetector()
        semantic_detector = None
        
        # Tenta carregar da Wikipedia primeiro
        try:
            with st.spinner("🌐 Carregando artigos da Wikipédia..."):
                wiki_docs = load_wikipedia_documents()
                
            if wiki_docs:
                lexical_detector.load_documents(wiki_docs)
                
                # Tenta carregar detector semântico
                try:
                    semantic_detector = SemanticPlagiarismDetector()
                    with st.spinner("🧠 Gerando embeddings semânticos..."):
                        semantic_detector.load_documents(wiki_docs)
                    st.success("✅ Detector semântico carregado!")
                except Exception as e:
                    st.warning(f"⚠️ Detector semântico não disponível: {e}")
                    semantic_detector = None
                
                st.session_state.database_source = "Wikipedia"
                st.session_state.documents = wiki_docs
                return lexical_detector, semantic_detector
        except Exception as e:
            st.warning(f"⚠️ Erro ao carregar da Wikipedia: {e}")
        
        # Fallback para dados locais
        lexical_detector.load_documents(COMPACT_DATABASE)
        
        try:
            semantic_detector = SemanticPlagiarismDetector()
            semantic_detector.load_documents(COMPACT_DATABASE)
            st.success("✅ Detector semântico carregado com dados locais!")
        except Exception as e:
            st.warning(f"⚠️ Detector semântico não disponível: {e}")
            semantic_detector = None
            
        st.session_state.database_source = "Local"
        st.session_state.documents = COMPACT_DATABASE
        return lexical_detector, semantic_detector

    lexical_detector, semantic_detector = load_detectors()
    
    # Sidebar
    with st.sidebar:
        st.header("📊 Informações")
        
        # Fonte dos dados
        source = st.session_state.get('database_source', 'Local')
        documents = st.session_state.get('documents', COMPACT_DATABASE)
        
        if source == "Wikipedia":
            st.success("🌐 Dados da Wikipédia")
        else:
            st.info("💾 Dados Locais")
            
        st.metric("Documentos na Base", len(documents))
        
        st.subheader("📚 Base de Dados")
        
        if documents:
            # Mostrar estatísticas
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Total", len(documents))
            with col2:
                wiki_count = sum(1 for doc in documents if 'url' in doc)
                st.metric("Com Links", wiki_count)
            
            # Organizar por período histórico
            periodos = {
                'Colonial': ['descobrimento', 'cabral', 'capitanias', 'governo', 'holandes', 'bandeiras', 'conjuração'],
                'Império': ['independencia', 'pedro', 'reinado', 'paraguai', 'abolição', 'proclamação'],
                'República': ['primeira', 'canudos', 'tenentismo', 'revolução', 'vargas', 'estado', 'guerra', 'ditadura', 'diretas', 'nova']
            }
            
            # Expandir documentos por período
            with st.expander("📖 Ver Todos os Documentos", expanded=False):
                
                # Agrupar documentos por período
                for periodo, keywords in periodos.items():
                    docs_periodo = [doc for doc in documents 
                                  if any(keyword in doc['id'].lower() for keyword in keywords)]
                    
                    if docs_periodo:
                        st.write(f"**📅 {periodo} ({len(docs_periodo)} docs):**")
                        for i, doc in enumerate(docs_periodo, 1):
                            title = doc['title']
                            if 'url' in doc and doc['url']:
                                st.markdown(f"  {i}. [{title}]({doc['url']})")
                            else:
                                st.markdown(f"  {i}. {title}")
                        st.write("")
                
                # Documentos não categorizados
                categorized_ids = set()
                for keywords in periodos.values():
                    for doc in documents:
                        if any(keyword in doc['id'].lower() for keyword in keywords):
                            categorized_ids.add(doc['id'])
                
                outros_docs = [doc for doc in documents if doc['id'] not in categorized_ids]
                if outros_docs:
                    st.write(f"**📋 Outros ({len(outros_docs)} docs):**")
                    for i, doc in enumerate(outros_docs, 1):
                        title = doc['title']
                        if 'url' in doc and doc['url']:
                            st.markdown(f"  {i}. [{title}]({doc['url']})")
                        else:
                            st.markdown(f"  {i}. {title}")
        
        else:
            st.warning("Nenhum documento carregado!")
            
        # Mostrar apenas os primeiros 5 na lista principal para economia de espaço
        st.write("**📝 Últimos 5 documentos:**")
        for doc in documents[:5]:
            if 'url' in doc:
                st.markdown(f"• [{doc['title']}]({doc['url']})")
            else:
                st.write(f"• {doc['title']}")
        
        if source == "Wikipedia":
            if st.button("🔄 Recarregar Wikipedia"):
                st.cache_resource.clear()
                st.rerun()
        
        st.subheader("ℹ️ Como Funciona")
        st.info("""
        1. **TF-IDF**: Analisa frequência de termos
        2. **N-gramas**: Encontra frases similares  
        3. **Cosseno**: Calcula similaridade
        4. **Ranking**: Ordena por relevância
        """)
        
        if source == "Wikipedia":
            st.subheader("🌐 Sobre a Wikipedia")
            st.info("""
            Utilizamos 50 artigos sobre **História do Brasil** 
            da Wikipédia em português como base de referência. 
            Cobrimos desde o período colonial até a república, 
            incluindo eventos, personagens e períodos importantes.
            """)
    
    # Interface principal
    st.subheader("📝 Texto para Análise")
    
    text_input = st.text_area(
        "Cole o texto aqui:",
        height=200,
        placeholder="Digite ou cole o texto que deseja verificar..."
    )
    
    # Botão de exemplo
    if st.button("📋 Usar Exemplo"):
        st.session_state.example = "Pedro Álvares Cabral comandou a esquadra portuguesa que chegou ao Brasil em 22 de abril de 1500, marcando o início da colonização portuguesa. A expedição de Cabral foi parte do esforço português para estabelecer rotas comerciais com as Índias."
        st.rerun()
    
    if 'example' in st.session_state:
        text_input = st.session_state.example
        del st.session_state.example
    
    # Abas para diferentes tipos de análise
    if text_input.strip():
        tab1, tab2 = st.tabs(["🔤 Análise Léxica (TF-IDF)", "🧠 Análise Semântica (Embeddings)"])
        
        with tab1:
            st.subheader("📊 Análise Léxica")
            st.caption("Compara palavras e frases exatas usando TF-IDF e n-gramas")
            
            if st.button("🔍 Analisar Léxico", type="primary", key="lexical_btn"):
                with st.spinner("Analisando similaridade léxica..."):
                    lexical_results = lexical_detector.detect(text_input)
                
                display_results(lexical_results, "Léxica", "🔤")
        
        with tab2:
            st.subheader("🧠 Análise Semântica")
            st.caption("Compara significado usando embeddings multilíngues")
            
            if st.button("🧠 Analisar Semântico", type="primary", key="semantic_btn"):
                # Tenta carregar detector semântico se não estiver disponível
                if semantic_detector is None:
                    with st.spinner("📦 Preparando análise semântica..."):
                        try:
                            temp_semantic_detector = SemanticPlagiarismDetector()
                            documents = st.session_state.get('documents', COMPACT_DATABASE)
                            temp_semantic_detector.load_documents(documents)
                            
                            with st.spinner("🧠 Analisando similaridade semântica..."):
                                semantic_results = temp_semantic_detector.detect_semantic(text_input)
                            
                            display_results(semantic_results, "Semântica", "🧠")
                            
                        except Exception as e:
                            st.error(f"❌ Erro na análise semântica: {e}")
                            st.info("💡 Instalando dependências automaticamente...")
                            # A instalação automática já foi configurada nas importações
                            st.rerun()
                else:
                    with st.spinner("🧠 Analisando similaridade semântica..."):
                        semantic_results = semantic_detector.detect_semantic(text_input)
                    
                    display_results(semantic_results, "Semântica", "🧠")
    
    else:
        st.info("💡 Digite um texto acima para começar a análise")


def display_results(results: List[SimilarityResult], analysis_type: str, icon: str):
    """Exibe os resultados da análise"""
    if not results:
        st.warning("Nenhum resultado encontrado")
        return
    
    # Gera chave única baseada no tipo de análise e hash dos resultados
    results_hash = str(hash(str([r.similarity for r in results])))
    unique_key = f"{analysis_type.lower()}_{results_hash}"
    
    st.success(f"✅ Análise {analysis_type} concluída!")
    
    # Métricas principais
    max_score = max(r.similarity for r in results)
    risk_text, risk_color = get_risk_level(max_score)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Maior Similaridade", f"{max_score}%")
    
    with col2:
        st.markdown(f'<div style="color: {risk_color}"><strong>{risk_text}</strong></div>', 
                   unsafe_allow_html=True)
    
    with col3:
        matches = sum(1 for r in results if r.matched_segments)
        st.metric("Documentos com Matches", matches)
    
    # Gráfico de barras simples
    df = pd.DataFrame([
        {"Documento": r.document_title[:30] + "..." if len(r.document_title) > 30 else r.document_title, 
         "Similaridade": r.similarity} 
        for r in results[:10]
    ])
    
    st.bar_chart(df.set_index("Documento"))
    
    # Resultados detalhados
    st.subheader(f"{icon} Resultados Detalhados")
    
    for i, result in enumerate(results, 1):
        with st.expander(f"#{i} - {result.document_title} ({result.similarity}%)"):
            
            # Informações do documento
            col_info1, col_info2 = st.columns(2)
            
            with col_info1:
                st.markdown(f"**📊 Similaridade:** {result.similarity}%")
                st.markdown(f"**📄 Documento:** {result.document_title}")
            
            with col_info2:
                if hasattr(result, 'url') and result.document_id in [doc.get('url', '') for doc in st.session_state.get('documents', [])]:
                    # Encontra URL do documento
                    doc_url = next((doc.get('url', '') for doc in st.session_state.get('documents', []) 
                                  if doc['id'] == result.document_id), '')
                    if doc_url:
                        st.markdown(f"**🔗 Link:** [Wikipedia]({doc_url})")
                
                if result.matched_segments:
                    st.markdown(f"**🎯 Segmentos:** {len(result.matched_segments)}")
            
            # Conteúdo
            st.markdown("**📖 Conteúdo:**")
            st.text(result.document_content)
            
            # Segmentos similares
            if result.matched_segments:
                st.markdown("**🎯 Segmentos Similares:**")
                for segment in result.matched_segments[:3]:
                    st.code(segment)
            
            # Download
            if st.button("💾 Baixar Resultados CSV", key=f"download_{unique_key}"):
                df = pd.DataFrame([
                    {
                        'Documento': r.document_title,
                        'Similaridade': r.similarity,
                        'Frases_Similares': '; '.join(r.matched_segments)
                    } for r in results
                ])
                
                csv = df.to_csv(index=False)
                st.download_button(
                    "📄 Download CSV",
                    csv,
                    f"analise_{analysis_type.lower()}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    "text/csv",
                    key=f"download_csv_{unique_key}"
                )
    # Footer
    st.markdown("---")
    st.markdown("**Detector de Plágio Compacto** - Versões Léxica e Semântica")


if __name__ == "__main__":
    main()
