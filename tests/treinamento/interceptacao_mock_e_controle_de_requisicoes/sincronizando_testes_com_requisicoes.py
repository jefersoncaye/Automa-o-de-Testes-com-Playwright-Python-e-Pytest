from playwright.sync_api import Page, expect


def fazer_login(page: Page):
    page.goto("http://localhost:5000/login")
    page.fill("#input-email", "cliente@loja.com")
    page.fill("#input-senha", "senha123")
    page.click("#botao-entrar")
    page.wait_for_url("**/produtos")


def test_antipadrao(page: Page):
    fazer_login(page)
    page.click('[data-testid="botao-adicionar-1"]')
    page.wait_for_timeout(1000)
    expect(page.locator("#mensagem-erro")).to_be_hidden()


def test_sincronizar_com_expect_response(page: Page):
    fazer_login(page)

    def eh_resposta_de_adicionar_carrinho(response):
        return response.url.endswith("/api/carrinho") and response.request.method == "POST"

    with page.expect_response(eh_resposta_de_adicionar_carrinho) as resposta_info:
        page.click('[data-testid="botao-adicionar-1"]')

    resposta = resposta_info.value

    assert resposta.status == 200

    corpo = resposta.json()
    assert corpo["sucesso"] is True
    assert corpo["produto_id"] == 1