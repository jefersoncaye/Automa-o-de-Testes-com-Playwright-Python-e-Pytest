from pages.base_page import BasePage


class DetalheProduto(BasePage):

    def __init__(self, page):
        super().__init__(page)
        self.nome_produto = page.get_by_role("heading", name="Blue Top")
        self.preco = page.get_by_text("Rs. 500")
        self.disponibilidade = page.get_by_text("Availability: In Stock")
        self.condicao = page.get_by_text("Condition: New")
        self.marca = page.get_by_text("Brand: Polo")
        self.botao_adicionar_carrinho = page.get_by_role("button", name="Add to cart")
        self.modal_titulo = page.get_by_role("heading", name="Added!")
        self.modal_mensagem = page.get_by_text("Your product has been added to cart.")
        self.botao_continuar_comprando = page.get_by_role("button", name="Continue Shopping")

    def adicionar_ao_carrinho(self):
        self.botao_adicionar_carrinho.click()