
class BasePage:
    def __init__(self, page):
        self.page = page
        self.botao_home = page.get_by_role("link", name="Home")
        self.botao_produtos = page.get_by_role("link", name="Products")
        self.botao_carrinho = page.get_by_role("link", name="Cart")
        self.botao_cadastro_login = page.get_by_role(
            "link", name="Signup / Login")
        self.botao_logout = page.get_by_role("link", name="Logout")

    def acessar_home(self):
        self.page.goto('')

    def acessar_carrinho(self):
        self.page.goto('view_cart')

    def acessar_produtos(self):
        self.page.goto('products')

    def acessar_cadastro_login(self):
        self.page.goto('login')
