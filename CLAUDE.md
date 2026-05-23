# CLAUDE.md

Este arquivo fornece orientações ao Claude Code (claude.ai/code) ao trabalhar com o código deste repositório.

## Visão Geral do Projeto

Projeto de curso de automação de testes com Playwright + Python + Pytest, voltado para o site [automationexercise.com](https://automationexercise.com/). Os testes são escritos em português (Brasil).

## Comandos

```bash
# Instalar dependências
pip install -r requirements.txt
playwright install

# Executar todos os testes (modo headed por padrão via pytest.ini)
pytest

# Executar um arquivo de teste específico
pytest tests/test_login_logout.py

# Executar um único teste pelo nome
pytest tests/test_login_logout.py::teste_login_valido

# Executar em modo headless
pytest --headed=false

# Executar com relatório HTML
pytest --html=report.html

# Visualizar trace (já habilitado no conftest.py):
playwright show-trace trace/trace.zip
```

Obs.: o `pytest.ini` define `--headed` e `testpaths = tests` por padrão. O diretório `tests/treinamento/` não é incluído na execução padrão.

## Arquitetura

### Page Object Model (POM)

Todas as interações com páginas ficam em `pages/`. Hierarquia de herança:

```
BasePage
├── CadastroLogin  (formulários de login e cadastro)
│   └── Inscreverse  (formulário completo de criação de conta)
├── Produtos       (listagem de produtos e adição ao carrinho)
└── Carrinho       (validação do carrinho)
```

- `BasePage` contém locators de navegação compartilhados e helpers `goto()` com URLs relativas (depende do `base_url` definido no conftest).
- As classes de página expõem locators como atributos de instância e agrupam ações em métodos.
- Os testes instanciam os page objects diretamente, recebendo a fixture `page`.

### Fixtures com Escopo de Sessão (`conftest.py`)

- `contexto` — contexto de browser com escopo de sessão, configurado com `base_url`, gravação de vídeo (`videos/`) e tracing. Salva o estado de autenticação em `playwright/auth/state.json` ao encerrar (para reuso de login).
- `page` — página com escopo de sessão derivada do `contexto`, com timeout padrão de 10 s e timeout de navegação de 30 s.
- Hook `pytest_runtest_makereport` — captura screenshot de página inteira em `imagens/` e anexa ao relatório HTML em caso de falha.

### Caminhos Importantes

| Caminho | Finalidade |
|---------|------------|
| `pages/` | Classes de Page Object |
| `tests/` | Suite principal de testes (coletada pelo pytest) |
| `tests/treinamento/` | Scripts exploratórios e de treinamento (fora da execução padrão) |
| `playwright/auth/state.json` | Estado de autenticação salvo (criado automaticamente após a primeira execução) |
| `trace/trace.zip` | Arquivo de trace do Playwright |
| `videos/` | Vídeos gravados dos testes |
| `imagens/` | Screenshots de falhas |
| `stores/` | Arquivos de dados diversos para testes |
