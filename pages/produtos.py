from pages.base_page import BasePage


class Produtos(BasePage):

    def __init__(self, page):
        super().__init__(page)
        self.card_produto = page.locator('.single-products')
        self.botao_adicionar_carrinho = page.locator(
            '.overlay-content:visible .btn')
        self.botao_continuar_comprando = page.get_by_role(
            "button", name="Continue Shopping")

    def adicionar_produto_ao_carrinho(self, indice_produto='0'):
        self.card_produto.nth(indice_produto).hover()
        self.botao_adicionar_carrinho.nth(indice_produto).click()
