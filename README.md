# 🌙 LunarBase — Simulador de Sobrevivência Lunar com Dados NASA

**FIAP — Global Solution 2026.1 | Inteligência Artificial — Fases 3 e 4**

| | |
|---|---|
| **Aluna** | Flavia Nunes Bocchino |
| **RM** | 564213 |
| **Demo ao vivo** | https://flahbocchino.github.io/lunarbase/ |
| **Vídeo** | https://youtu.be/Wcb475c3Q6o |

---

## O que é

Simulador interativo de sobrevivência lunar que usa dados reais da NASA para calcular o risco da missão com Machine Learning. O jogador assume o papel de astronauta da missão Artemis e precisa sobreviver 30 dias lunares gerenciando recursos críticos (O₂, energia, água, temperatura) enquanto enfrenta eventos baseados na atividade espacial real do dia.

---

## Como funciona

```
NASA DONKI + NeoWs (APIs reais)
        ↓
Python + pandas + RandomForestClassifier (Google Colab)
        ↓
nasa_data.json (nível de risco do dia)
        ↓
Jogo HTML/JS + LunaBot (GitHub Pages)
```

1. O script Python coleta dados reais da NASA e classifica o risco em 4 níveis (Baixo/Moderado/Alto/Crítico)
2. O JSON gerado é lido pelo jogo, que ajusta a dificuldade com base no risco real do dia
3. O LunaBot responde consultas técnicas com base em documentação oficial NASA/ESA

---

## Tecnologias

| Tecnologia | Uso |
|---|---|
| Python + pandas | Coleta e processamento de dados |
| scikit-learn RandomForestClassifier | Classificação de risco da missão |
| NASA DONKI API | Eventos solares reais (CMEs, flares) |
| NASA NeoWs API | Asteroides próximos |
| HTML5 + CSS3 + JavaScript | Jogo interativo |
| GitHub Pages | Deploy gratuito, sem servidor |
| Google Colab | Execução do pipeline Python |

---

## Como executar

**1. Gerar dados NASA (Google Colab)**
- Abra `colab/lunarbase_nasa.py` no Google Colab
- Execute todas as células
- Baixe o `nasa_data.json` gerado

**2. Atualizar dados no repositório**
- Faça upload do `nasa_data.json` na raiz do repositório

**3. Jogar**
- Acesse https://flahbocchino.github.io/lunarbase/

---

## Estrutura do repositório

```
lunarbase/
├── index.html          # Jogo completo
├── nasa_data.json      # Dados NASA processados
├── colab/
│   └── lunarbase_nasa.py  # Pipeline Python + ML
├── docs/               # Documentação PDF
└── assets/             # Recursos estáticos
```

---

## Referências

- NASA DONKI: https://kauai.ccmc.gsfc.nasa.gov/DONKI/
- NASA NeoWs: https://api.nasa.gov/
- NASA Artemis: https://www.nasa.gov/artemis
- scikit-learn: https://scikit-learn.org/

> Dados baseados em documentação pública da NASA e ESA. Base de conhecimento atualizada até 08/06/2026.
