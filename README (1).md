# 🌙 LunarBase — Simulador de Sobrevivência Lunar com IA e Dados NASA

**FIAP — Global Solution 2026.1 | Inteligência Artificial — Fases 3 e 4**

---

## Integrantes

| Nome | RM |
|------|-----|
| [SEU NOME COMPLETO] | [SEU RM] |

---

## Descrição do Projeto

LunarBase é uma prova de conceito (POC) de um jogo de sobrevivência lunar que integra **dados reais da NASA**, **Machine Learning** e **base de conhecimento técnico espacial** para responder ao desafio da Global Solution 2026.1:

> *Como tecnologias avançadas de Inteligência Artificial, automação e computação podem impulsionar soluções inovadoras para a nova economia espacial?*

O jogador assume o papel de astronauta em uma base lunar durante a missão Artemis. Precisa gerenciar recursos críticos (O₂, energia, água, temperatura) ao longo de 30 dias lunares, enfrentando eventos aleatórios baseados em condições espaciais reais.

---

## Arquitetura da Solução

```
┌─────────────────────────────────────────────────────────┐
│                  LUNARBASE ARCHITECTURE                 │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  [Google Colab — Python]                                │
│  ├── NASA DONKI API (tempestades solares, CMEs)        │
│  ├── NASA NeoWs API (asteroides próximos)              │
│  ├── pandas (processamento de dados)                   │
│  ├── scikit-learn RandomForestClassifier (ML)          │
│  └── Gera: nasa_data.json                              │
│                    ↓                                    │
│  [GitHub Pages — HTML/CSS/JS]                          │
│  ├── Consome nasa_data.json                            │
│  ├── Jogo de sobrevivência lunar interativo            │
│  ├── LunaBot (base de conhecimento técnico NASA)       │
│  └── Risco da missão ajustado por dados reais          │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

## Tecnologias Utilizadas

| Camada | Tecnologia | Finalidade |
|--------|-----------|------------|
| Coleta de dados | NASA DONKI API | Eventos solares reais (CMEs, flares) |
| Coleta de dados | NASA NeoWs API | Asteroides próximos da Terra/Lua |
| Processamento | Python + pandas | Normalização e análise dos dados |
| Machine Learning | scikit-learn RandomForestClassifier | Classificação de nível de risco da missão |
| Interface | HTML5 + CSS3 + JavaScript | Jogo interativo no browser |
| Deploy | GitHub Pages | Hospedagem gratuita, sem servidor |
| Execução Python | Google Colab | Pipeline de dados sem instalação local |

---

## Disciplinas Integradas

- **IA Generativa / Base de Conhecimento**: LunaBot com 12 respostas técnicas baseadas em documentação real NASA, ESA e publicações científicas revisadas
- **Machine Learning**: RandomForestClassifier classifica nível de risco (Baixo/Moderado/Alto/Crítico) com base em features extraídas dos dados NASA
- **Análise de Dados**: pandas processa e normaliza dados brutos das APIs NASA
- **APIs e Dados Reais**: NASA DONKI (DONKI.ccmc.gsfc.nasa.gov) e NASA NeoWs (api.nasa.gov)
- **Aplicação Distribuída**: pipeline Python (Colab) + frontend estático (GitHub Pages)
- **Automação**: coleta e processamento automático de dados espaciais reais

---

## Como Executar

### Passo 1 — Gerar dados NASA (Google Colab)

1. Acesse [Google Colab](https://colab.research.google.com)
2. Crie um novo notebook
3. Copie o conteúdo de `colab/lunarbase_nasa.py`
4. Execute as células em ordem (célula 1 a 7)
5. O arquivo `nasa_data.json` será gerado e baixado automaticamente

### Passo 2 — Subir o JSON no GitHub

1. Acesse seu repositório no GitHub
2. Clique em "Add file" → "Upload files"
3. Arraste o arquivo `nasa_data.json` baixado
4. Clique em "Commit changes"

### Passo 3 — Jogar

1. Acesse: `https://[seu-usuario].github.io/lunarbase/`
2. O jogo carrega os dados NASA automaticamente
3. Clique em "Avançar dia" para progredir na missão
4. Use o LunaBot para consultar protocolos de emergência
5. Sobreviva 30 dias lunares!

---

## Dados NASA Utilizados

| API | Endpoint | Dados |
|-----|----------|-------|
| NASA DONKI | `/WS/get/CME` | Coronal Mass Ejections (ejeções de massa coronal) |
| NASA DONKI | `/WS/get/FLR` | Solar Flares (erupções solares) |
| NASA DONKI | `/WS/get/GST` | Geomagnetic Storms (tempestades geomagnéticas) |
| NASA NeoWs | `/neo/rest/v1/feed` | Near Earth Objects (asteroides próximos) |

> **Aviso**: Dados baseados em documentação pública da NASA, ESA e publicações científicas revisadas. Base de conhecimento atualizada até **08/06/2026**.

---

## Estrutura do Repositório

```
lunarbase/
├── index.html              # Jogo completo (HTML/CSS/JS)
├── nasa_data.json          # Dados gerados pelo Colab (atualizar periodicamente)
├── colab/
│   └── lunarbase_nasa.py   # Script Python para Google Colab
└── README.md               # Este arquivo
```

---

## Resultados Esperados

- Classificação de risco em tempo real baseada em dados NASA reais
- Jogo funcional de sobrevivência lunar com 11 tipos de eventos
- LunaBot com 12 consultas técnicas baseadas em documentação NASA/ESA
- Pipeline completo de dados: coleta → ML → visualização interativa

---

## Link do Vídeo

[Inserir link do YouTube — não listado]

---

## Referências

- NASA DONKI: https://kauai.ccmc.gsfc.nasa.gov/DONKI/
- NASA NeoWs: https://api.nasa.gov/
- NASA Artemis Program: https://www.nasa.gov/artemis
- MOXIE Experiment: https://mars.nasa.gov/mars2020/spacecraft/instruments/moxie/
- Kilopower Project: https://www.nasa.gov/directorates/stmd/kilopower/
- NASA ECLSS: https://www.nasa.gov/international-space-station/eclss/
- LRO Mission: https://lunar.gsfc.nasa.gov/
