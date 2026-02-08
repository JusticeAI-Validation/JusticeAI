# 📚 Índice de Documentação - justiceai

**Bem-vindo ao justiceai!**

Esta página serve como **mapa de navegação** de toda a documentação do projeto.

---

## 🎯 Por Onde Começar?

### Se você é...

**👨‍💼 Gestor/Product Owner**
1. Leia: [`RESUMO_EXECUTIVO.md`](RESUMO_EXECUTIVO.md) (15 min)
2. Depois: [`PLANEJAMENTO_AGIL.md`](PLANEJAMENTO_AGIL.md) - Seções 1-3 (20 min)
3. Aprove e comunique ao time

**👨‍💻 Desenvolvedor (novo no projeto)**
1. Leia: [`README.md`](README.md) (5 min)
2. Depois: [`desenvolvimento/INDEX.md`](desenvolvimento/INDEX.md) - Navegue pelas sprints (10 min)
3. Depois: Abra o documento da sprint atual em [`desenvolvimento/sprints/`](desenvolvimento/sprints/) (30 min)
4. Setup ambiente: Siga [`GUIA_QUALIDADE_CODIGO_PYTHON.md`](../DeepBridge/desenvolvimento/GUIA_QUALIDADE_CODIGO_PYTHON.md)

**🧪 Early Adopter/Beta Tester**
1. Leia: [`README.md`](README.md) (5 min)
2. Veja: Roadmap em [`PLANEJAMENTO_AGIL.md`](PLANEJAMENTO_AGIL.md) - Seção 10
3. Forneça feedback: GitHub Discussions ou email

**🤝 Contribuidor Open Source**
1. Leia: [`README.md`](README.md) - Seção "Contribuindo"
2. Escolha issue: GitHub Issues (label: `good-first-issue`)
3. Siga: `CONTRIBUTING.md` (a ser criado na Sprint 0)

---

## 📂 Estrutura de Documentação

### 📋 Documentos de Planejamento

| Documento | Descrição | Audiência | Tempo Leitura |
|-----------|-----------|-----------|---------------|
| **[RESUMO_EXECUTIVO.md](RESUMO_EXECUTIVO.md)** | Visão geral, timeline, métricas, riscos | PO, Gestores | 15 min |
| **[PLANEJAMENTO_AGIL.md](PLANEJAMENTO_AGIL.md)** | Planejamento completo: sprints, épicos, DoD | Time completo | 60 min |
| **[PRODUCT_BACKLOG_DETALHADO.md](PRODUCT_BACKLOG_DETALHADO.md)** | User stories com critérios INVEST | Devs, PO | 90 min |
| **[desenvolvimento/INDEX.md](desenvolvimento/INDEX.md)** | Índice de desenvolvimento por sprint | Devs | 10 min |

### 📖 Documentação Pública

| Documento | Descrição | Audiência | Status |
|-----------|-----------|-----------|--------|
| **[README.md](README.md)** | Página inicial do GitHub, quick start | Todos | ✅ Criado |
| **LICENSE** | Licença MIT | Legal | ⏳ Sprint 0 |
| **CHANGELOG.md** | Histórico de mudanças (Keep a Changelog) | Usuários | ⏳ Sprint 0 |
| **CONTRIBUTING.md** | Guia de contribuição | Contributors | ⏳ Sprint 0 |

### 🛠️ Guias Técnicos (Referências DeepBridge)

Estes guias estão em `/home/guhaase/projetos/DeepBridge/desenvolvimento/`:

| Guia | Descrição | Quando Usar |
|------|-----------|-------------|
| **[GUIA_QUALIDADE_CODIGO_PYTHON.md](../DeepBridge/desenvolvimento/GUIA_QUALIDADE_CODIGO_PYTHON.md)** | Padrões de qualidade: coverage, type hints, linting | Setup, code review |
| **[GUIA_BUILD_PUBLICACAO_PYTHON.md](../DeepBridge/desenvolvimento/GUIA_BUILD_PUBLICACAO_PYTHON.md)** | Como buildar e publicar no PyPI | Sprint 5 (release) |

### 📚 Documentação de Usuário (Futuro - Sprint 3)

| Documento | Descrição | Status |
|-----------|-----------|--------|
| **docs/getting_started.md** | Tutorial inicial | ⏳ Sprint 3 |
| **docs/api_reference.md** | Referência completa da API | ⏳ Sprint 3 |
| **docs/tutorials/** | Tutoriais hands-on | ⏳ Sprint 3 |
| **docs/compliance_lgpd_bacen.md** | Guia de compliance | ⏳ Sprint 4 |
| **examples/notebooks/** | Jupyter notebooks | ⏳ Sprint 3 |

---

## 🗺️ Mapa de Navegação por Objetivo

### 🎯 "Quero entender o projeto em 5 minutos"

```
1. README.md (seção "O Problema")
2. README.md (seção "Quick Start")
3. README.md (seção "Comparação com Concorrentes")
```

### 📊 "Quero saber o planejamento completo"

```
1. RESUMO_EXECUTIVO.md (toda)
2. PLANEJAMENTO_AGIL.md (seções 1-6)
3. PLANEJAMENTO_AGIL.md (seção 10: Cronograma Visual)
```

### 💻 "Quero começar a desenvolver agora"

```
1. README.md (seção "Instalação para Desenvolvimento")
2. PRODUCT_BACKLOG_DETALHADO.md (US-001 a US-006)
3. GUIA_QUALIDADE_CODIGO_PYTHON.md (setup de ferramentas)
4. Executar: poetry install
5. Executar: make quality
```

### 🧪 "Quero testar/usar a biblioteca"

```
⏳ Aguarde Sprint 1 (22 Fev)
Enquanto isso:
1. Veja exemplos em README.md
2. Star no GitHub para acompanhar
3. Participe do early adopters program
```

### 🤝 "Quero contribuir"

```
1. README.md (seção "Contribuindo")
2. CONTRIBUTING.md (⏳ Sprint 0)
3. Escolha issue: GitHub → Issues → label "good-first-issue"
4. Fork → Branch → Code → PR
```

---

## 📅 Cronograma de Documentação

### Sprint 0 (8-22 Fev) - Docs Base

- [x] ✅ RESUMO_EXECUTIVO.md
- [x] ✅ PLANEJAMENTO_AGIL.md
- [x] ✅ PRODUCT_BACKLOG_DETALHADO.md
- [x] ✅ README.md
- [x] ✅ INDEX.md (este arquivo)
- [ ] ⏳ LICENSE
- [ ] ⏳ CHANGELOG.md
- [ ] ⏳ CONTRIBUTING.md
- [ ] ⏳ CODE_OF_CONDUCT.md
- [ ] ⏳ SECURITY.md

### Sprint 3 (22 Mar - 5 Abr) - Docs de Usuário

- [ ] ⏳ docs/getting_started.md
- [ ] ⏳ docs/api_reference.md (auto-gerado via mkdocstrings)
- [ ] ⏳ docs/tutorials/01_basic_usage.md
- [ ] ⏳ docs/tutorials/02_advanced_metrics.md
- [ ] ⏳ docs/tutorials/03_custom_reports.md
- [ ] ⏳ examples/notebooks/01_quickstart.ipynb

### Sprint 4 (5-19 Abr) - Docs de Compliance

- [ ] ⏳ docs/compliance_lgpd_bacen.md
- [ ] ⏳ docs/monitoring_production.md
- [ ] ⏳ examples/lgpd_report_example.py
- [ ] ⏳ examples/monitoring_setup.py

### Sprint 5 (19 Abr - 3 Mai) - Docs de Release

- [ ] ⏳ RELEASE_NOTES_v1.0.0.md
- [ ] ⏳ Blog post de lançamento
- [ ] ⏳ Atualizar README com badges reais
- [ ] ⏳ Vídeo demo (YouTube)

---

## 🔗 Links Rápidos

### Interno (Projeto)

- 📋 [Resumo Executivo](RESUMO_EXECUTIVO.md)
- 📅 [Planejamento Ágil](PLANEJAMENTO_AGIL.md)
- 📊 [Product Backlog](PRODUCT_BACKLOG_DETALHADO.md)
- 📖 [README](README.md)

### Externo (Referências)

- 🏛️ [Fairlearn (Microsoft)](https://fairlearn.org/)
- 🏛️ [AIF360 (IBM)](https://aif360.readthedocs.io/)
- 📚 [Guia Qualidade Código](../DeepBridge/desenvolvimento/GUIA_QUALIDADE_CODIGO_PYTHON.md)
- 📚 [Guia Build & Publicação](../DeepBridge/desenvolvimento/GUIA_BUILD_PUBLICACAO_PYTHON.md)

### GitHub (em breve)

- 🐙 GitHub Repository: https://github.com/guhaase/justiceai (⏳)
- 📦 PyPI Package: https://pypi.org/project/justiceai/ (⏳ Sprint 5)
- 📖 Documentation: https://justiceai.readthedocs.io (⏳ Sprint 3)

---

## 📞 Contatos

**Dúvidas sobre o planejamento?**
- **Product Owner**: Gustavo Haase
- **Email**: gustavo.haase@gmail.com
- **GitHub**: [@guhaase](https://github.com/guhaase)

**Quer contribuir?**
- **GitHub Discussions**: (em breve)
- **Slack**: (em breve, para early adopters)

---

## 🔄 Atualizações deste Índice

| Data | Mudança | Autor |
|------|---------|-------|
| 2026-02-08 | Criação inicial | Gustavo Haase |
| - | - | - |

**Este documento será atualizado conforme novos docs forem criados.**

---

## 💡 Como Usar Este Índice

1. **Bookmark esta página** no seu navegador
2. **Use Ctrl+F** para buscar tópicos específicos
3. **Siga os links** para navegação rápida
4. **Volte aqui** quando se perder na documentação

---

<p align="center">
  <b>⚖️ justiceai - Documentação Completa</b>
  <br>
  <sub>Organizada, Atualizada, Acessível</sub>
</p>
