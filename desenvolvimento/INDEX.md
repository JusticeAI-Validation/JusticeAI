# 📚 Índice de Documentação de Desenvolvimento - justiceai

**Bem-vindo à documentação de desenvolvimento do justiceai!**

Esta pasta contém todo o planejamento detalhado por sprint, guias técnicos e documentação de processo.

---

## 🗺️ Navegação Rápida

### 📋 Por Sprint

| Sprint | Período | Objetivo | Status | Link |
|--------|---------|----------|--------|------|
| **Sprint 0** | 8-22 Fev | Fundação do Projeto | ⏳ TODO | [SPRINT_0.md](sprints/SPRINT_0.md) |
| **Sprint 1** | 22 Fev - 8 Mar | Métricas Core | ⏳ TODO | [SPRINT_1.md](sprints/SPRINT_1.md) |
| **Sprint 2** | 8-22 Mar | Reports HTML | ⏳ TODO | [SPRINT_2.md](sprints/SPRINT_2.md) |
| **Sprint 3** | 22 Mar - 5 Abr | API Pública + Docs | ⏳ TODO | [SPRINT_3.md](sprints/SPRINT_3.md) |
| **Sprint 4** | 5-19 Abr | Compliance + Monitoring | ⏳ TODO | [SPRINT_4.md](sprints/SPRINT_4.md) |
| **Sprint 5** | 19 Abr - 3 Mai | Polish & Release | ⏳ TODO | [SPRINT_5.md](sprints/SPRINT_5.md) |

### 📊 Visão Geral

```
Timeline MVP (12 semanas):

FEV       MAR       ABR       MAI
├─────────┼─────────┼─────────┼───┐
│ Sprint0 │ Sprint1 │ Sprint2 │ S3│ S4│ S5│
│ Setup   │ Metrics │ Reports │API│Cmp│Rel│
└─────────┴─────────┴─────────┴───┴───┴───┘
                                        ▲
                                   v1.0.0
                                  3 Maio
```

---

## 📁 Estrutura de Documentação

```
desenvolvimento/
├── INDEX.md                    # ← Você está aqui
├── sprints/                    # Planejamento detalhado por sprint
│   ├── SPRINT_0.md            # Setup & Fundação
│   ├── SPRINT_1.md            # Métricas Core
│   ├── SPRINT_2.md            # Reports HTML
│   ├── SPRINT_3.md            # API Pública + Docs
│   ├── SPRINT_4.md            # Compliance + Monitoring
│   └── SPRINT_5.md            # Polish & Release
└── (futuro)
    ├── guias/                 # Guias técnicos específicos
    ├── retrospectivas/        # Retrospectivas de cada sprint
    └── demos/                 # Materiais de demo
```

---

## 🎯 Como Usar Esta Documentação

### Se você é Desenvolvedor

**Começando agora?**
1. Leia: [../RESUMO_EXECUTIVO.md](../RESUMO_EXECUTIVO.md) (15 min)
2. Veja qual sprint estamos: Tabela acima
3. Abra o documento da sprint atual
4. Execute as tarefas listadas

**Durante uma sprint?**
1. Consulte o documento da sprint atual
2. Atualize status das user stories conforme progresso
3. Documente decisões técnicas no próprio arquivo
4. Prepare demo ao final

### Se você é Product Owner

**Planejando uma sprint?**
1. Revise o documento da sprint
2. Ajuste prioridades se necessário
3. Adicione/remova user stories conforme feedback
4. Comunique mudanças ao time

**Durante a sprint?**
1. Monitore progresso via status das US
2. Valide critérios de aceite
3. Prepare sprint review

### Se você é Stakeholder

**Quer saber o progresso?**
1. Veja a tabela de sprints acima
2. Abra o documento da sprint atual
3. Check "Entregáveis" e "Métricas de Sucesso"

---

## 📋 Conteúdo de Cada Sprint

Cada documento de sprint contém:

### Estrutura Padrão
- **Objetivos da Sprint**: O que queremos alcançar
- **User Stories**: Funcionalidades a implementar
  - Prioridade
  - Estimativa
  - Critérios de aceite
  - Tarefas técnicas
  - Definition of Done
- **Tarefas Técnicas**: Breakdown semanal
- **Métricas de Sucesso**: Como medir progresso
- **Riscos e Mitigações**: O que pode dar errado
- **Entregáveis**: O que será entregue

---

## 🔍 Detalhamento das Sprints

### Sprint 0: Fundação (2 semanas)
**Foco**: Setup profissional
- Poetry, CI/CD, linters, testes
- Estrutura de diretórios
- Documentação base
- **Entregáveis**: Projeto profissional pronto para desenvolvimento

### Sprint 1: Métricas Core (2 semanas)
**Foco**: Implementar métricas de fairness
- 15+ métricas (pre e post-training)
- Confusion matrix por grupo
- Threshold analysis
- **Entregáveis**: Core funcional com coverage ≥ 95%

### Sprint 2: Reports HTML (2 semanas)
**Foco**: Sistema de relatórios
- Data transformer
- Plotly charts
- Template HTML
- **Entregáveis**: Reports HTML standalone interativos

### Sprint 3: API + Docs (2 semanas)
**Foco**: API pública e documentação
- Model adapters (sklearn, XGBoost, etc.)
- API 1-liner
- MkDocs completo
- **Entregáveis**: API pronta para usuários finais

### Sprint 4: Compliance (2 semanas)
**Foco**: Diferencial Brasil
- LGPD compliance
- BACEN compliance
- Drift detection
- **Entregáveis**: Compliance único no mercado

### Sprint 5: Polish & Release (2 semanas)
**Foco**: Lançamento
- Code review
- Benchmarks
- PyPI release
- **Entregáveis**: v1.0.0 lançada

---

## 📊 Métricas Consolidadas (Todas Sprints)

| Métrica | Target Total |
|---------|--------------|
| **User Stories** | ~35 stories |
| **Story Points** | ~280 SP |
| **Code Coverage** | ≥ 95% |
| **Funcionalidades** | 7 épicos |
| **Duração Total** | 12 semanas |

---

## 🔗 Links Úteis

### Documentação Principal
- [RESUMO_EXECUTIVO.md](../RESUMO_EXECUTIVO.md) - Visão geral executiva
- [PLANEJAMENTO_AGIL.md](../PLANEJAMENTO_AGIL.md) - Planejamento completo
- [PRODUCT_BACKLOG_DETALHADO.md](../PRODUCT_BACKLOG_DETALHADO.md) - Backlog completo
- [README.md](../README.md) - Documentação pública

### Guias Técnicos (DeepBridge)
- [GUIA_QUALIDADE_CODIGO_PYTHON.md](../../DeepBridge/desenvolvimento/GUIA_QUALIDADE_CODIGO_PYTHON.md)
- [GUIA_BUILD_PUBLICACAO_PYTHON.md](../../DeepBridge/desenvolvimento/GUIA_BUILD_PUBLICACAO_PYTHON.md)

### Referências Externas
- [Poetry Documentation](https://python-poetry.org/docs/)
- [GitHub Actions](https://docs.github.com/actions)
- [Fairlearn](https://fairlearn.org/)
- [AIF360](https://aif360.readthedocs.io/)

---

## 🔄 Processo de Atualização

### Quem Atualiza
- **Devs**: Status de user stories, decisões técnicas
- **PO**: Prioridades, critérios de aceite
- **Scrum Master**: Métricas, riscos, impedimentos

### Quando Atualizar
- **Diariamente**: Status das user stories em progresso
- **Fim de sprint**: Retrospectiva, lições aprendidas
- **Mudanças significativas**: Ajustes de escopo, novos riscos

### Como Atualizar
1. Editar arquivo Markdown relevante
2. Commit com mensagem descritiva
3. Comunicar mudanças ao time

---

## 📞 Contatos

**Product Owner**: Gustavo Haase
- Email: gustavo.haase@gmail.com
- GitHub: @guhaase

---

## 🎓 Padrões de Documentação

Inspirados no DeepBridge, seguimos:

1. **Markdown** para todos os docs
2. **Estrutura consistente** entre sprints
3. **Emojis** para legibilidade
4. **Links internos** para navegação
5. **Versionamento** via Git

---

## 🚀 Quick Start

**Primeira vez aqui?**
```bash
# 1. Clone o repo
git clone https://github.com/guhaase/justiceai.git
cd justiceai

# 2. Leia documentação base
cat README.md
cat RESUMO_EXECUTIVO.md

# 3. Veja sprint atual
cd desenvolvimento/sprints
cat SPRINT_0.md  # ou a sprint atual

# 4. Setup ambiente
poetry install
```

---

## 📅 Histórico de Atualizações

| Data | Sprint | Mudança | Autor |
|------|--------|---------|-------|
| 2026-02-08 | - | Criação inicial de todas as sprints | Gustavo Haase |
| - | - | - | - |

---

**Última Atualização**: 2026-02-08
**Mantido por**: Gustavo Haase (Product Owner)
**Formato**: Markdown com estrutura padronizada

---

<p align="center">
  <b>⚖️ justiceai - Documentação de Desenvolvimento</b>
  <br>
  <sub>Organizada por Sprint, Focada em Resultados</sub>
</p>
