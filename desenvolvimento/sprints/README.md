# 📅 Sprints - justiceai

Documentação detalhada de cada sprint do projeto justiceai.

---

## 🗓️ Cronograma de Sprints

| Sprint | Período | Duração | Objetivo Principal | Documento |
|--------|---------|---------|-------------------|-----------|
| **Sprint 0** | 8-22 Fev 2026 | 2 semanas | Fundação do Projeto | [SPRINT_0.md](SPRINT_0.md) |
| **Sprint 1** | 22 Fev - 8 Mar 2026 | 2 semanas | Métricas Core | [SPRINT_1.md](SPRINT_1.md) |
| **Sprint 2** | 8-22 Mar 2026 | 2 semanas | Reports HTML | [SPRINT_2.md](SPRINT_2.md) |
| **Sprint 3** | 22 Mar - 5 Abr 2026 | 2 semanas | API Pública + Docs | [SPRINT_3.md](SPRINT_3.md) |
| **Sprint 4** | 5-19 Abr 2026 | 2 semanas | Compliance Brasil + Monitoring | [SPRINT_4.md](SPRINT_4.md) |
| **Sprint 5** | 19 Abr - 3 Mai 2026 | 2 semanas | Polish & Release v1.0.0 | [SPRINT_5.md](SPRINT_5.md) |

**Duração Total**: 12 semanas (3 meses)
**Launch Target**: 3 de Maio de 2026

---

## 📊 Visão Geral por Sprint

### Sprint 0: Fundação
**User Stories**: 6 | **Story Points**: 21 SP
- Setup Poetry
- CI/CD GitHub Actions
- Linters e formatters
- Framework de testes
- Documentação inicial
- Estrutura de módulos

### Sprint 1: Métricas Core
**User Stories**: 6 | **Story Points**: 66 SP
- 4 métricas pre-training
- 11 métricas post-training
- Confusion matrix por grupo
- Threshold analysis
- FairnessCalculator facade

### Sprint 2: Reports HTML
**User Stories**: 6 | **Story Points**: 64 SP
- Data transformer
- Chart factory (Plotly)
- Template HTML Jinja2
- HTML renderer
- Report builder
- Exemplos de reports

### Sprint 3: API Pública + Docs
**User Stories**: 6 | **Story Points**: 70 SP
- Model adapters (sklearn, XGBoost, etc.)
- FairnessEvaluator
- API `audit()` 1-liner
- MkDocs completo
- Jupyter notebooks
- Docstrings 100%

### Sprint 4: Compliance Brasil
**User Stories**: 5 | **Story Points**: 56 SP
- LGPD compliance reporter
- BACEN compliance reporter
- Fairness drift detection
- Alerting system
- Exemplo de monitoring

### Sprint 5: Polish & Release
**User Stories**: 6 | **Story Points**: 54 SP
- Code review completo
- Coverage ≥ 95%
- Performance benchmarks
- Packaging & PyPI
- Release v1.0.0
- Marketing materials

---

## 🎯 Como Usar

### Durante uma Sprint

1. **Abra o documento da sprint atual**
   ```bash
   cat SPRINT_X.md
   ```

2. **Consulte as User Stories**
   - Prioridade
   - Estimativa
   - Critérios de aceite
   - Tarefas técnicas

3. **Atualize o status conforme progresso**
   - [ ] TODO → [x] DONE
   - Documente decisões

4. **Prepare demo ao final**
   - Demonstre entregáveis
   - Colete feedback

### Planejando Próxima Sprint

1. **Review da sprint anterior**
   - O que funcionou?
   - O que melhorar?

2. **Refinamento do backlog**
   - Ajuste prioridades
   - Atualize estimativas

3. **Kick-off da nova sprint**
   - Compromisso do time
   - Alignment nos objetivos

---

## 📈 Progresso Consolidado

### Métricas Gerais

| Métrica | Target | Atual |
|---------|--------|-------|
| **Total Sprints** | 6 | 0 completadas |
| **Total Story Points** | ~280 SP | 0 completados |
| **Total User Stories** | ~35 stories | 0 completadas |
| **Code Coverage** | ≥ 95% | - |
| **Duração Total** | 12 semanas | 0 semanas |

### Status por Sprint

| Sprint | Status | Progresso |
|--------|--------|-----------|
| Sprint 0 | ⏳ TODO | 0% |
| Sprint 1 | ⏳ TODO | 0% |
| Sprint 2 | ⏳ TODO | 0% |
| Sprint 3 | ⏳ TODO | 0% |
| Sprint 4 | ⏳ TODO | 0% |
| Sprint 5 | ⏳ TODO | 0% |

---

## 🔗 Links Relacionados

- [Voltar para desenvolvimento/INDEX.md](../INDEX.md)
- [RESUMO_EXECUTIVO.md](../../RESUMO_EXECUTIVO.md)
- [PLANEJAMENTO_AGIL.md](../../PLANEJAMENTO_AGIL.md)
- [PRODUCT_BACKLOG_DETALHADO.md](../../PRODUCT_BACKLOG_DETALHADO.md)

---

**Última Atualização**: 2026-02-08
**Mantido por**: Gustavo Haase
