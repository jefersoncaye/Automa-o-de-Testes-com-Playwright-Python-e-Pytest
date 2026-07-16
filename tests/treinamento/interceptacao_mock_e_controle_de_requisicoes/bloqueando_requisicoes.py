from playwright.sync_api import Page, expect


def fazer_login(page: Page):
    page.goto("http://localhost:5000/login")
    page.fill("#input-email", "cliente@loja.com")
    page.fill("#input-senha", "senha123")
    page.click("#botao-entrar")
    page.wait_for_url("**/produtos")


def test_bloquear_imagens_por_padrao_de_url(page: Page):
    fazer_login(page)

    def bloquear_imagem(route):
        route.abort()

    page.pause()
    page.route("**/static/img/*.svg", bloquear_imagem)
    page.reload()

    # A página continua funcional: produtos aparecem normalmente,
    # só as imagens é que não carregam.
    expect(page.locator('[data-testid^="produto-"]')).to_have_count(6)


def test_bloquear_por_tipo_de_recurso(page: Page):
    fazer_login(page)

    def bloquear_apenas_imagens(route):
        if route.request.resource_type == "image":
            route.abort()
        else:
            route.continue_()

    page.pause()
    page.route("**/*", bloquear_apenas_imagens)
    page.reload()

    expect(page.locator('[data-testid^="produto-"]')).to_have_count(6)