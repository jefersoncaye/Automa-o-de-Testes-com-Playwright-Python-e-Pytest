import json

from playwright.sync_api import Page, expect


def fazer_login(page: Page):
    page.goto("http://localhost:5000/login")
    page.fill("#input-email", "cliente@loja.com")
    page.fill("#input-senha", "senha123")
    page.click("#botao-entrar")
    page.wait_for_url("**/produtos")


def test_mock_lista_vazia_de_produtos(page: Page):
    fazer_login(page)

    def mock_produtos_vazios(route):
        route.fulfill(
            status=200,
            content_type="application/json",
            body="[]",
        )
    page.route("**/api/produtos", mock_produtos_vazios)
    page.reload()  # recarrega /produtos, agora com o mock já ativo

    expect(page.locator('[data-testid^="produto-"]')).to_have_count(0)


def test_mock_produto_customizado(page: Page):
    fazer_login(page)

    produtos_fake = [
        {
            "id": 1,
            "nome": "Produto Fake Caríssimo",
            "preco": 9999.99,
            "estoque": 1,
            "imagem": "/static/img/produto-1.svg",
        },
        {
            "id": 2,
            "nome": "Produto Fake Caríssimo 2",
            "preco": 9999.99,
            "estoque": 1,
            "imagem": "/static/img/produto-2.svg",
        }
    ]

    def mock_catalogo_customizado(route):
        route.fulfill(
            status=200,
            content_type="application/json",
            body=json.dumps(produtos_fake),
        )
    page.route("**/api/produtos", mock_catalogo_customizado)
    page.reload()

    expect(page.locator('[data-testid^="produto-"]')).to_have_count(1)
    expect(page.get_by_text("Produto Fake Caríssimo")).to_be_visible()