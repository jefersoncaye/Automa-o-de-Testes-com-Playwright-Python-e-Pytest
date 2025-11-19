from pages.base_page import BasePage
from playwright.sync_api import expect


class Carrinho(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.label_cabecalho_descricao_produto = page.locator(
            '.cart_description h4')
        self.label_descricao_produto = page.locator('.cart_description p')
        self.label_preco_produto = page.locator('.cart_price')
        self.label_preco_total = page.locator('.cart_total_price')
        self.botao_excluir_produto = page.locator('.cart_quantity_delete')

    def validar_carrinho(
            self,
            indice_produto,
            cabecalho_descricao_produto,
            descricao_produto,
            preco_produto,
            preco_total_produto):
        expect(self.label_cabecalho_descricao_produto.nth(
            indice_produto)).to_have_text(cabecalho_descricao_produto)
        expect(self.label_descricao_produto.nth(
            indice_produto)).to_have_text(descricao_produto)
        expect(self.label_preco_produto.nth(
            indice_produto)).to_have_text(preco_produto)
        expect(self.label_preco_total.nth(indice_produto)
               ).to_have_text(preco_total_produto)
