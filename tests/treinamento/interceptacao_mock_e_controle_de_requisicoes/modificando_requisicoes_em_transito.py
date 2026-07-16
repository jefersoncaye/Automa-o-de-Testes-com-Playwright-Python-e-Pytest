import json

from playwright.sync_api import Page, expect


def fazer_login(page: Page):
    page.goto("http://localhost:5000/login")
    page.fill("#input-email", "cliente@loja.com")
    page.fill("#input-senha", "senha123")
    page.click("#botao-entrar")
    page.wait_for_url("**/produtos")


def test_forcar_erro_de_estoque_modificando_body(page: Page):
    fazer_login(page)

    def trocar_produto_no_carrinho(route):
        # Independente do que o clique realmente mandou, troca o
        # produto_id para o produto sem estoque (id 3).
        novo_body = json.dumps({"produto_id": 3, "quantidade": 1})
        route.continue_(post_data=novo_body)

    page.route("**/api/carrinho", trocar_produto_no_carrinho)
    page.pause()
    # Clica em "adicionar" de um produto QUALQUER com estoque — não
    # importa qual, porque o corpo real vai ser trocado em trânsito.
    page.click('[data-testid="botao-adicionar-1"]')

    # A API responde 409 (sem estoque) para o produto 3, e o front
    # mostra a mensagem de erro na tela.
    expect(page.locator("#mensagem-erro")).to_be_visible()


def test_modificar_header_em_transito(page: Page):
    fazer_login(page)

    def adicionar_header_customizado(route):
        headers = {**route.request.headers, "x-teste-automatizado": "true"}
        route.continue_(headers=headers)

    page.route("**/api/carrinho", adicionar_header_customizado)
    page.pause()
    with page.expect_request("**/api/carrinho") as requisicao_info:
        page.click('[data-testid="botao-adicionar-2"]')

    requisicao = requisicao_info.value
    print(requisicao.post_data)
    assert requisicao.headers["x-teste-automatizado"] == "true"