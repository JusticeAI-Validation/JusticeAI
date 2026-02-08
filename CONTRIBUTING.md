# Contribuindo para justiceai

Obrigado por seu interesse em contribuir para o justiceai! Este documento fornece diretrizes para contribuir com o projeto.

## Desenvolvimento

### Requisitos
- Python >=3.11,<3.13
- Poetry >=1.7.0

### Setup

```bash
# 1. Fork e clone o repositório
git clone https://github.com/SEU-USUARIO/JusticeAI.git
cd JusticeAI

# 2. Instalar dependências
poetry install

# 3. Ativar ambiente virtual
poetry shell

# 4. Instalar pre-commit hooks
poetry run pre-commit install
```

### Workflow de Desenvolvimento

1. **Criar branch para sua feature**
   ```bash
   git checkout -b feature/nome-da-feature
   ```

2. **Fazer mudanças**
   - Escreva código limpo e bem documentado
   - Adicione testes para novas funcionalidades
   - Mantenha coverage ≥ 90%

3. **Rodar qualidade**
   ```bash
   make quality
   ```
   Isso irá:
   - Formatar código (Black, isort)
   - Executar linters (Ruff, Pylint)
   - Verificar tipos (MyPy)
   - Rodar testes (Pytest)

4. **Commit suas mudanças**
   ```bash
   git commit -m "feat: adiciona nova funcionalidade"
   ```

   Usamos [Conventional Commits](https://www.conventionalcommits.org/):
   - `feat:` Nova funcionalidade
   - `fix:` Correção de bug
   - `docs:` Mudanças na documentação
   - `test:` Adicionar/modificar testes
   - `refactor:` Refatoração de código
   - `style:` Formatação, ponto e vírgula, etc
   - `chore:` Atualização de dependências, etc

5. **Push e abrir Pull Request**
   ```bash
   git push origin feature/nome-da-feature
   ```

## Padrões de Código

### Python
- Siga PEP 8
- Use type hints em todas funções públicas
- Docstrings no estilo Google
- Linha máxima: 88 caracteres (Black default)

### Testes
- Coverage mínimo: 90%
- Um teste para cada funcionalidade
- Testes devem ser independentes
- Use fixtures quando apropriado

### Documentação
- Docstrings para todas funções/classes públicas
- Exemplos nos docstrings para funções críticas
- Atualizar README.md se necessário

## Reportar Bugs

Abra uma issue com:
- Descrição clara do problema
- Passos para reproduzir
- Comportamento esperado
- Comportamento atual
- Versão do Python e justiceai
- Stacktrace (se aplicável)

## Solicitar Features

Abra uma issue com:
- Descrição clara da feature
- Por que é útil
- Exemplos de uso

## Code of Conduct

- Seja respeitoso e profissional
- Aceite feedback construtivo
- Foque no que é melhor para a comunidade

## Dúvidas?

- Abra uma issue
- Email: gustavo.haase@gmail.com
- GitHub Discussions (em breve)

---

**Obrigado por contribuir! 🎉**
