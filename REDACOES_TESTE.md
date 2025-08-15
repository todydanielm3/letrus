# 📝 Redações de Teste para Avaliação

Esta pasta contém redações de exemplo sobre História do Brasil para testar o detector de plágio.

## 🎯 **Casos de Teste Preparados**

### **1. Alto Plágio (≥70%)**
**Redação A1**: Cópia quase literal da Wikipedia
> "Pedro Álvares Cabral foi um fidalgo, comandante militar, navegador e explorador português, creditado como o descobridor do Brasil. Cabral conduziu a primeira expedição substancial às terras que viria a ser chamadas de Brasil, reivindicando-as para Portugal."

**Redação A2**: Paráfrase próxima
> "Cabral foi o comandante português responsável por descobrir o Brasil. Ele liderou a esquadra que chegou às terras brasileiras e as reivindicou para Portugal em 1500."

### **2. Plágio Médio (40-69%)**
**Redação M1**: Mistura de fontes
> "O descobrimento do Brasil aconteceu quando a expedição de Cabral chegou ao território. A independência posterior foi proclamada por Dom Pedro I, que declarou a separação de Portugal em 1822."

**Redação M2**: Paráfrase moderada  
> "A chegada dos portugueses ao Brasil marcou o início da colonização. Séculos depois, o país conquistou sua liberdade política através da proclamação feita às margens do Ipiranga."

### **3. Baixo Plágio (<40%)**
**Redação B1**: Texto original com contexto histórico
> "A formação do Brasil como nação passou por diversos períodos importantes. Desde a chegada dos europeus até a construção de uma identidade nacional própria, o país vivenciou transformações profundas que moldaram sua cultura única."

**Redação B2**: Análise pessoal
> "Estudar a história brasileira nos permite compreender as raízes da nossa sociedade contemporânea. Os eventos históricos influenciaram diretamente a formação do caráter nacional que observamos hoje."

### **4. Casos Específicos**
**Redação E1**: Era Vargas
> "Getúlio Vargas governou o Brasil durante quinze anos consecutivos, implementando políticas trabalhistas que revolucionaram as relações de trabalho no país e estabeleceram direitos fundamentais para os trabalhadores."

**Redação E2**: Ditadura Militar  
> "O regime militar brasileiro durou de 1964 a 1985, período marcado pela repressão política e pela censura. O movimento Diretas Já foi fundamental para o retorno da democracia."

## 🔬 **Como Testar**

1. Execute a aplicação Docker:
```bash
./docker-manager.sh run
```

2. Acesse: http://localhost:8501

3. Cole cada redação na interface

4. Analise os resultados:
   - % de similaridade
   - Documento mais similar encontrado
   - Frases em comum detectadas
   - Nível de risco calculado

## 📊 **Resultados Esperados**

| Redação | Similaridade Esperada | Documento Principal | Risco |
|---------|----------------------|-------------------|--------|
| A1 | 80-95% | Descobrimento do Brasil | 🚨 Alto |
| A2 | 70-85% | Pedro Álvares Cabral | 🚨 Alto |
| M1 | 50-65% | Descobrimento/Independência | ⚠️ Médio |
| M2 | 45-60% | Independência do Brasil | ⚠️ Médio |
| B1 | 20-35% | Vários documentos | ✅ Baixo |
| B2 | 15-30% | Vários documentos | ✅ Baixo |
| E1 | 60-75% | Getúlio Vargas | ⚠️ Médio |
| E2 | 55-70% | Ditadura militar | ⚠️ Médio |

## 📋 **Critérios de Avaliação**

### **Funcionamento Correto:**
- ✅ Detecção precisa de alto plágio (A1, A2)
- ✅ Identificação de plágio médio (M1, M2, E1, E2)
- ✅ Reconhecimento de textos originais (B1, B2)

### **Qualidade da Análise:**
- ✅ Frases similares identificadas corretamente
- ✅ Documentos fonte identificados
- ✅ Percentuais de similaridade coerentes
- ✅ Classificação de risco apropriada

### **Interface Funcional:**
- ✅ Carregamento rápido (< 2 minutos)
- ✅ Análise em tempo real (< 5 segundos)
- ✅ Resultados bem formatados
- ✅ Links para fontes funcionando

---

**📝 Base utilizada**: 25 artigos de História do Brasil da Wikipedia em português
**🎯 Cobertura**: Período colonial, império, república e Brasil contemporâneo
