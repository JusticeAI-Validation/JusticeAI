# 📋 Resumo Executivo - justiceai

**Data**: 2026-02-08
**Versão**: 1.0
**Autor**: Gustavo Haase (Product Owner)
**Status**: ✅ Aprovado para Execução

---

## 🎯 Visão Geral

**justiceai** é uma biblioteca Python open-source para análise de fairness em modelos de Machine Learning, com foco em:

1. **Produção-first**: Monitoring contínuo, não apenas análise pontual
2. **Compliance Brasil/LATAM**: Templates para LGPD e BACEN
3. **Developer Experience**: API de 1 linha, framework-agnostic
4. **Reports Standalone**: HTML com Plotly interativo, offline

### Elevator Pitch (30s)

> "Enquanto Fairlearn e AIF360 são ferramentas acadêmicas que param no notebook, **justiceai** é a primeira biblioteca focada em levar fairness para produção, com monitoring contínuo, compliance LGPD/BACEN e relatórios prontos para stakeholders. Instalou, rodou `audit(model, data)`, gerou HTML — simples assim."

---

## 📊 Por Que Este Projeto?

### Problema de Mercado

| Ferramenta Atual | Limitação | justiceai Resolve |
|------------------|-----------|-------------------|
| **Fairlearn** | Acadêmica, não vai pra produção | Monitoring contínuo, CI/CD integration |
| **AIF360** | 70 métricas = confuso | 15 métricas curadas + interpretação |
| **Google Fairness Indicators** | Lock-in TensorFlow | Framework-agnostic (sklearn → PyTorch) |
| **What-If Tool** | Só exploração, sem automação | Dual-mode: exploração + automação |
| **Todas** | Zero compliance Brasil | Templates LGPD/BACEN nativos |

### Diferenciação

**Único no mercado** a oferecer:
1. ✅ MLOps-first (drift detection, alerting)
2. ✅ Compliance Brasil (LGPD Art. 20, BACEN Res. 4.658)
3. ✅ Reports HTML standalone (Plotly interativo, offline)
4. ✅ API 1-liner: `audit(model, data).show()`

---

## 🗓️ Timeline e Milestones

### Fase 1: MVP (12 semanas = 3 meses)

```
┌─────────────────────────────────────────────────────┐
│  SPRINT 0  │  SPRINT 1  │  SPRINT 2  │  SPRINT 3  │
│  (2 sem)   │  (2 sem)   │  (2 sem)   │  (2 sem)   │
├────────────┼────────────┼────────────┼────────────┤
│  Setup &   │  Métricas  │  Reports   │  API +     │
│  Fundação  │  Core      │  HTML      │  Docs      │
└────────────┴────────────┴────────────┴────────────┘
     ↓             ↓            ↓            ↓
  Feb 8-22     Feb 22-      Mar 8-22    Mar 22-
                Mar 8                    Abr 5

┌─────────────────────────────────────────────────────┐
│  SPRINT 4  │  SPRINT 5  │                           │
│  (2 sem)   │  (2 sem)   │                           │
├────────────┼────────────┼──────────────────────────┤
│ Compliance │ Polish &   │  🚀 v1.0.0 Launch        │
│ + Monitor  │ Release    │                           │
└────────────┴────────────┴──────────────────────────┘
     ↓             ↓                  ↓
  Abr 5-19     Abr 19-          Maio 3, 2026
                Maio 3          (PyPI Release)
```

### Milestones Críticos

| Data | Milestone | Entregáveis |
|------|-----------|-------------|
| **22 Fev** | ✅ Sprint 0 Done | Projeto estruturado, CI/CD, docs base |
| **8 Mar** | ✅ Sprint 1 Done | 15 métricas funcionando, coverage 90% |
| **22 Mar** | ✅ Sprint 2 Done | Reports HTML com Plotly |
| **5 Abr** | ✅ Sprint 3 Done | API pública, docs completas |
| **19 Abr** | ✅ Sprint 4 Done | Compliance LGPD, monitoring |
| **3 Maio** | 🚀 **v1.0.0 Launch** | PyPI release, marketing |

---

## 📈 Métricas de Sucesso

### Técnicas (MVP - 3 Maio)

| Métrica | Target MVP | Como Medir |
|---------|-----------|------------|
| **Code Coverage** | ≥ 90% | pytest-cov |
| **Type Coverage** | 100% (APIs públicas) | mypy strict |
| **Pylint Score** | ≥ 9.0 | pylint |
| **Bugs Críticos** | 0 | GitHub Issues |
| **Documentação** | 100% APIs | mkdocstrings |

### Negócio (3 meses pós-launch)

| Métrica | Target 3M | Como Medir |
|---------|-----------|------------|
| **Downloads PyPI** | 500+ | pypistats |
| **Stars GitHub** | 200+ | GitHub API |
| **Contributors** | 5+ | GitHub |
| **Empresas Usando** | 3+ | Validação direta |
| **NPS** | ≥ 8 | Survey early adopters |

---

## 💰 Investimento Necessário

### Recursos Humanos

| Papel | Dedicação | Período |
|-------|-----------|---------|
| **Product Owner** | 20% (8h/sem) | 12 semanas |
| **Developer 1** | 50% (20h/sem) | 12 semanas |
| **Developer 2** | 50% (20h/sem) | 12 semanas |
| **Total** | 90% FTE | 3 meses |

**Horas Totais**: ~480 horas (2 devs × 20h/sem × 12 sem)

### Custos Diretos

| Item | Custo Estimado |
|------|----------------|
| **Desenvolvimento** | R$ 0 (time interno) |
| **Infra GitHub Actions** | R$ 0 (free tier) |
| **Codecov** | R$ 0 (open source) |
| **Domínio** | R$ 50/ano (opcional) |
| **Docs Hosting** | R$ 0 (GitHub Pages) |
| **PyPI** | R$ 0 (grátis) |
| **TOTAL** | < R$ 100 |

**ROI**: Praticamente zero custo monetário, todo investimento é tempo de dev.

---

## 🎯 Stack Tecnológico

### Core Dependencies

```toml
python = ">=3.10,<3.13"
numpy = ">=1.24.0"
pandas = ">=2.0.0"
scikit-learn = ">=1.3.0"
scipy = ">=1.11.0"
plotly = ">=5.14.0"      # Visualização
jinja2 = ">=3.1.0"        # Templates
pydantic = ">=2.0.0"      # Validação
```

### Dev/Quality Tools

```toml
# Gerenciamento
poetry = ">=1.7.0"

# Testes
pytest = ">=7.0"
pytest-cov = ">=4.0"

# Qualidade
black = ">=23.0"          # Formatação
ruff = ">=0.1.0"          # Linting
mypy = ">=1.0"            # Type checking
pylint = ">=3.0"          # Análise estática
isort = ">=5.12"          # Import sorting

# Docs
mkdocs-material = ">=9.0"
mkdocstrings-python = ">=1.0"

# Build
build = ">=1.0"
twine = ">=4.0"
```

### Infrastructure

- **Version Control**: Git + GitHub
- **CI/CD**: GitHub Actions (free tier)
- **Coverage**: Codecov (free for open source)
- **Docs**: GitHub Pages ou ReadTheDocs (free)
- **Package Registry**: PyPI (free)

**Conclusão**: Stack 100% gratuito para open source.

---

## 🚧 Riscos e Mitigações

### Riscos Técnicos

| Risco | Probabilidade | Impacto | Mitigação |
|-------|---------------|---------|-----------|
| **R1**: Dependências quebram | MÉDIA | MÉDIO | Pin versões exatas, CI multi-version |
| **R2**: Coverage < 90% | MÉDIA | ALTO | DoD rigoroso, code review obrigatório |
| **R3**: Performance ruim | BAIXA | MÉDIO | Benchmarks desde Sprint 1 |

### Riscos de Negócio

| Risco | Probabilidade | Impacto | Mitigação |
|-------|---------------|---------|-----------|
| **R4**: Baixa adoção | MÉDIA | ALTO | Marketing pré-launch, early adopters, docs ++ |
| **R5**: Concorrente similar | BAIXA | MÉDIO | Foco em diferenciais (Brasil, MLOps) |
| **R6**: Scope creep | ALTA | ALTO | Backlog priorizado, PO forte, sprints fixas |

### Riscos de Equipe

| Risco | Probabilidade | Impacto | Mitigação |
|-------|---------------|---------|-----------|
| **R7**: Time indisponível | MÉDIA | ALTO | Buffer 20% em sprints, backlog flexível |
| **R8**: Burnout | BAIXA | MÉDIO | Sprints sustentáveis (não overtime) |

---

## ✅ Próximos Passos Imediatos

### Esta Semana (8-14 Fev)

- [ ] **Aprovar este planejamento** com stakeholders
- [ ] **Criar repositório GitHub** `justiceai` (público)
- [ ] **Setup projeto**: Executar US-001 (Poetry setup)
- [ ] **Convidar early adopters**: 5-10 fintechs/startups ML
- [ ] **Configurar CI/CD**: US-002 (GitHub Actions)

### Próxima Semana (15-21 Fev)

- [ ] **Finalizar Sprint 0**: US-003 a US-006
- [ ] **Sprint Review**: Demo interno
- [ ] **Retrospectiva**: O que funcionou? Ajustes?
- [ ] **Planejar Sprint 1**: Breakdown de US-007 a US-012

### Mês 1 (Fev 22 - Mar 21)

- [ ] **Completar Sprint 1** (Métricas Core)
- [ ] **Completar Sprint 2** (Reports HTML)
- [ ] **Primeiros early adopters testando**
- [ ] **Ajustar roadmap** baseado em feedback

---

## 📞 Comunicação e Governança

### Daily Standups (Assíncrono)

**Formato**: Slack/GitHub Discussions
**Frequência**: Diário
**Template**:
```
🟢 O que fiz ontem?
🔵 O que farei hoje?
🔴 Impedimentos?
```

### Sprint Reviews

**Frequência**: Fim de cada sprint (a cada 2 semanas)
**Participantes**: Time + stakeholders
**Agenda**:
1. Demo de features (15 min)
2. Métricas da sprint (5 min)
3. Feedback e ajustes (10 min)

### Sprint Retrospectives

**Frequência**: Fim de cada sprint
**Participantes**: Time apenas
**Agenda**:
1. O que funcionou bem? (10 min)
2. O que pode melhorar? (10 min)
3. Action items (5 min)

### Comunicação com Early Adopters

**Canal**: GitHub Discussions + Email
**Frequência**: Bi-semanal (update newsletter)
**Conteúdo**: Progresso, features novas, como contribuir

---

## 🎓 Lições do DeepBridge

Este projeto aproveita lições aprendidas do **DeepBridge**:

### ✅ O Que Manter

1. **Poetry** para gerenciamento de deps
2. **Máxima qualidade** (coverage 90%+, type hints, linting)
3. **Estrutura modular** (core, reports, utils)
4. **Templates Jinja2** para reports
5. **Plotly** para visualizações

### 🔄 O Que Melhorar

1. **API mais simples**: DeepBridge é verboso, justiceai será 1-liner
2. **Docs desde dia 1**: DeepBridge teve docs como afterthought
3. **Testes desde dia 1**: Não acumular debt técnico
4. **Marketing proativo**: DeepBridge é pouco conhecido

### 🆕 O Que Adicionar

1. **Compliance Brasil**: LGPD/BACEN (único no mercado)
2. **Monitoring produção**: Drift detection, alerting
3. **Framework-agnostic**: DeepBridge é muito sklearn-centric
4. **Early adopters program**: Validar com usuários reais

---

## 📚 Documentação do Planejamento

Este planejamento está organizado em:

1. **`PLANEJAMENTO_AGIL.md`** (este arquivo): Visão geral, sprints, cronograma
2. **`PRODUCT_BACKLOG_DETALHADO.md`**: User stories completas (INVEST)
3. **`README.md`**: Documentação pública do projeto
4. **`GUIA_QUALIDADE_CODIGO_PYTHON.md`**: (link) Padrões de código
5. **`GUIA_BUILD_PUBLICACAO_PYTHON.md`**: (link) Como buildar e publicar

### Onde Estão os Arquivos?

```
/home/guhaase/projetos/justiceai/
├── PLANEJAMENTO_AGIL.md              # ← Você está aqui
├── PRODUCT_BACKLOG_DETALHADO.md      # User stories
├── RESUMO_EXECUTIVO.md               # Este arquivo
├── README.md                         # Documentação pública
└── (em breve)
    ├── pyproject.toml
    ├── justiceai/
    ├── tests/
    └── docs/
```

**Referências**:
- **Guias DeepBridge**: `/home/guhaase/projetos/DeepBridge/desenvolvimento/`
  - `GUIA_QUALIDADE_CODIGO_PYTHON.md`
  - `GUIA_BUILD_PUBLICACAO_PYTHON.md`

---

## 🚀 Call to Action

### Para o Product Owner (Gustavo)

- [x] ✅ Aprovar este planejamento
- [ ] ⏳ Criar repo GitHub
- [ ] ⏳ Convidar early adopters
- [ ] ⏳ Comunicar kickoff para time

### Para o Time de Dev

- [ ] ⏳ Ler planejamento completo
- [ ] ⏳ Setup ambiente de dev
- [ ] ⏳ Começar Sprint 0 (US-001)
- [ ] ⏳ Daily standups assíncronos

### Para Early Adopters

- [ ] ⏳ Fornecer feedback sobre roadmap
- [ ] ⏳ Testar MVP quando pronto
- [ ] ⏳ Sugerir features críticas

---

## 🎉 Conclusão

**justiceai** é um projeto ambicioso mas viável:

✅ **Escopo bem definido**: 5 sprints, 12 semanas, MVP claro
✅ **Diferenciação clara**: MLOps + Compliance Brasil
✅ **Stack validado**: Baseado em DeepBridge (funciona)
✅ **Investimento baixo**: <R$ 100, todo em tempo de dev
✅ **Riscos mitigados**: Planejamento ágil, iterativo

**Próximo passo**: Executar Sprint 0 (semanas 1-2) e validar velocity.

---

**Status**: ✅ **APROVADO - PRONTO PARA EXECUÇÃO**

**Kickoff**: Segunda-feira, 10 de Fevereiro de 2026

**Let's build something great! ⚖️**

---

**Documento criado**: 2026-02-08
**Autor**: Gustavo Haase (Product Owner)
**Versão**: 1.0
**Licença**: MIT (como o projeto)
