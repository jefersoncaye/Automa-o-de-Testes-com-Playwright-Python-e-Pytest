# Loja Mock

Aplicação de e-commerce fake, extremamente simples, criada para servir de alvo
estável e 100% local em aulas de automação de testes com Playwright + Python +
Pytest. O foco não é a aplicação em si, e sim oferecer endpoints e telas
previsíveis para exercícios de interceptação/mock de requisições de rede.

## Stack

- Backend: Python 3.12+ e Flask (sem banco de dados, tudo em memória)
- Frontend: HTML + CSS + JavaScript puro, sem build step e sem frameworks
- Front e back servidos na mesma origem (`http://localhost:5000`), sem CORS

## Instalação

```bash
pip install -r requirements.txt
```

## Executando

```bash
python app.py
```

A aplicação sobe em `http://localhost:5000`.

## Credenciais de teste

- E-mail: `cliente@loja.com`
- Senha: `senha123`

## Páginas

- `/login` — formulário de login (fetch para `/api/login`)
- `/produtos` — catálogo de produtos (fetch para `/api/produtos`)
- `/carrinho` — carrinho de compras (fetch para `/api/carrinho`)

## Endpoints da API

| Método | Rota                     | Descrição                                   |
|--------|---------------------------|----------------------------------------------|
| POST   | `/api/login`               | Autentica e cria sessão                      |
| POST   | `/api/logout`               | Encerra a sessão                             |
| GET    | `/api/produtos`             | Lista produtos (aceita `?categoria=`)        |
| GET    | `/api/carrinho`             | Lista itens do carrinho da sessão atual      |
| POST   | `/api/carrinho`             | Adiciona um produto ao carrinho              |
| DELETE | `/api/carrinho/<produto_id>`| Remove um produto do carrinho                |
| POST   | `/api/reset`                | Reseta todo o estado em memória (produtos e carrinhos) |

O carrinho é isolado por sessão (cookie), permitindo que testes com contextos
diferentes do Playwright rodem em paralelo sem interferência.

## Estrutura de pastas

```
loja_mock/
├── app.py
├── requirements.txt
├── README.md
├── templates/
│   ├── login.html
│   ├── produtos.html
│   └── carrinho.html
└── static/
    ├── css/style.css
    ├── js/login.js
    ├── js/produtos.js
    ├── js/carrinho.js
    └── img/produto-1.svg ... produto-6.svg
```
