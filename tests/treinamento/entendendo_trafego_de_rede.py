from playwright.sync_api import Page


def test_observar_trafego_de_rede(page: Page):
    # Registra os listeners ANTES de navegar, para capturar
    # tudo que acontece já no carregamento da página.
    page.on("request", lambda request: print(f">> {request.method} {request.url}"))
    page.on("response", lambda response: print(f"<< {response.status} {response.url}"))

    page.goto("http://localhost:5000/produtos")

    # Nesse ponto, no console, já aparecem as chamadas reais disparadas
    # pela página: GET /api/produtos, GET /api/carrinho, e as imagens
    # locais /static/img/produto-N.svg.


def test_observar_apenas_chamadas_de_api(page: Page):
    # Na prática, quase sempre você só quer as chamadas para /api/,
    # ignorando CSS, JS e imagens. Dá pra filtrar direto no listener.
    def logar_apenas_api(request):
        if "/api/" in request.url:
            print(f">> {request.method} {request.url}")

    page.on("request", logar_apenas_api)
    page.goto("http://localhost:5000/produtos")


def test_login_dispara_requisicao_real(page: Page):
    # Confirma que o login da loja_mock usa fetch (não <form> nativo
    # com reload de página) — é isso que torna a chamada interceptável.
    requisicoes_login = []
    page.on("request", lambda r: requisicoes_login.append(r) if "/api/login" in r.url else None)

    page.goto("http://localhost:5000/login")
    page.fill("#input-email", "cliente@loja.com")
    page.fill("#input-senha", "senha123")
    page.click("#botao-entrar")

    page.wait_for_url("**/produtos")
    assert len(requisicoes_login) == 1
    assert requisicoes_login[0].method == "POST"