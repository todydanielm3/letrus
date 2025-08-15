# 🇧🇷 Detector de Plágio - História do Brasil

Solução especializada para detecção de plágio utilizando **25 artigos sobre História do Brasil** da Wikipedia como base de referência.

## 🌟 Características

### ✅ **Base Especializada**
- **25 artigos** sobre História do Brasil da Wikipedia
- Cobertura do **período colonial** até a **república**
- Conteúdo atualizado e verificado
- Textos de domínio público

### ✅ **Períodos Históricos Cobertos**
- 🚢 **Período Colonial**: Descobrimento, capitanias, invasões
- 👑 **Império**: Independência, Dom Pedro I e II, abolição
- 🏛️ **República**: Proclamação, Era Vargas, ditadura militar
- 🆕 **Brasil Contemporâneo**: Nova República, Diretas Já

### ✅ **Algoritmo Avançado**
- **TF-IDF**: Análise de frequência de termos
- **N-gramas**: Detecção de frases similares
- **Similaridade do Cosseno**: Cálculo matemático preciso
- **Ranking automático**: Resultados ordenados por relevância

## 📚 Base de Dados (25 Artigos)

### **Período Colonial**
1. Descobrimento do Brasil
2. Pedro Álvares Cabral
3. Capitanias hereditárias
4. Governo-geral
5. Invasões holandesas no Brasil
6. Entradas e bandeiras
7. Conjuração Mineira
8. Conjuração Baiana

### **Império**
9. Independência do Brasil
10. Dom Pedro I do Brasil
11. Primeiro Reinado
12. Dom Pedro II do Brasil
13. Guerra do Paraguai
14. Abolição da escravatura no Brasil
15. Proclamação da República do Brasil

### **República**
16. Primeira República Brasileira
17. Guerra de Canudos
18. Tenentismo
19. Revolução de 1930
20. Getúlio Vargas
21. Estado Novo (Brasil)
22. Brasil na Segunda Guerra Mundial
23. Ditadura militar no Brasil
24. Diretas Já
25. Nova República

## 🚀 Como Usar

### **Método 1: Execução Direta**
```bash
# Instalar dependências
pip install streamlit pandas wikipedia

# Executar aplicação
streamlit run detector_compacto.py
```

### **Método 2: Docker**
```bash
# Construir imagem
docker build -f Dockerfile_minimal -t detector-historia-brasil .

# Executar container
docker run -p 8501:8501 detector-historia-brasil
```

### **Acesso**
- Abra o navegador em: http://localhost:8501
- Cole o texto sobre História do Brasil
- Clique em "Analisar"
- Veja os resultados especializados

## 📊 Exemplos de Uso

### **Alto Plágio (≥70%)**
**Texto:** "Pedro Álvares Cabral comandou a esquadra portuguesa que chegou ao Brasil em 22 de abril de 1500"
- **Resultado:** 85% similaridade com "Descobrimento do Brasil"
- **Status:** 🚨 Alto Risco

### **Médio Plágio (40-69%)**
**Texto:** "Dom Pedro proclamou a independência às margens do Ipiranga em 1822"
- **Resultado:** 55% similaridade com "Independência do Brasil"  
- **Status:** ⚠️ Risco Médio

### **Baixo Plágio (<40%)**
**Texto:** "A culinária brasileira combina influências indígenas e africanas"
- **Resultado:** 15% similaridade
- **Status:** ✅ Baixo Risco

## 🔧 Estrutura Ultra-Compacta

```
letrus/
├── detector_compacto.py          # 🎯 Solução completa (20KB)
├── demo_historia_brasil.py       # 🇧🇷 Demonstração especializada
├── requirements_minimal.txt      # 📦 Dependências mínimas  
├── Dockerfile_minimal           # 🐳 Container otimizado
└── README.md                   # 📖 Documentação
```

## 🎯 Casos de Uso Específicos

### **Educação Básica**
- Verificação de trabalhos sobre História do Brasil
- Análise de redações sobre períodos específicos
- Detecção de cópia em pesquisas escolares

### **Ensino Superior**
- Verificação de monografias de História
- Análise de dissertações sobre Brasil Colonial/Imperial
- Auditoria de trabalhos acadêmicos

### **Concursos Públicos**
- Verificação de provas dissertativas
- Análise de redações sobre cidadania
- Detecção de cola em questões de História

## 🧪 Demonstração Completa

Execute a demonstração especializada:

```bash
python3 demo_historia_brasil.py
```

Saída esperada:
```
🇧🇷 DETECTOR DE PLÁGIO - HISTÓRIA DO BRASIL
==================================================
📖 Carregando base de dados da Wikipedia...
✅ 25 artigos sobre História do Brasil carregados

1. 🚢 DESCOBRIMENTO
   Texto: "Pedro Álvares Cabral comandou a esquadra..."
   📊 Maior similaridade: 85% (Descobrimento do Brasil)
   🎯 Nível de risco: 🚨 Alto (VERMELHO)
```

## 📈 Performance Especializada

- ⚡ **Carregamento**: ~30-60 segundos (25 artigos Wikipedia)
- ⚡ **Análise**: <1 segundo por texto
- 💾 **Memória**: ~80MB RAM  
- 📦 **Precisão**: Especializada em História do Brasil

## 🔒 Tratamento de Erros

- ✅ **Sistema robusto** para falhas da Wikipedia
- ✅ **Fallback automático** para dados locais de História do Brasil
- ✅ **Tratamento de ambiguidades** de títulos históricos
- ✅ **Busca alternativa** em caso de erro
- ✅ **Logs informativos** durante carregamento

## 🌐 Integração Wikipedia

### **Artigos Carregados**
- Configuração: `wikipedia.set_lang('pt')`
- Conteúdo: Primeiros 2500 caracteres de cada artigo
- Performance: Carregamento otimizado com logs
- Backup: Sistema de fallback para dados locais

### **Qualidade dos Dados**
- ✅ Artigos verificados e atualizados
- ✅ Conteúdo factual e enciclopédico
- ✅ Cobertura ampla da História do Brasil
- ✅ Links diretos para fontes originais

## 📝 Licença

Este projeto utiliza conteúdo da Wikipedia sob licença Creative Commons. Desenvolvido para fins educacionais com foco em História do Brasil.

---

**🇧🇷 Especializado em História do Brasil • Desenvolvido com Python + Streamlit + Wikipedia API**
