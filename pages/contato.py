from pages.base_page import BasePage


class Contato(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.campo_nome = page.get_by_role("textbox", name="Name")
        self.campo_email = page.get_by_role("textbox", name="Email", exact=True)
        self.campo_assunto = page.get_by_role("textbox", name="Subject")
        self.campo_mensagem = page.get_by_placeholder("Your Message Here")
        self.botao_enviar = page.get_by_role("button", name="Submit")
        self.mensagem_sucesso = page.locator("#contact-page .status.alert-success")

    def acessar_contato(self):
        self.page.goto("contact_us")

    def preencher_formulario(self, nome, email, assunto, mensagem):
        self.campo_nome.fill(nome)
        self.campo_email.fill(email)
        self.campo_assunto.fill(assunto)
        self.campo_mensagem.fill(mensagem)

    def enviar_formulario(self):
        self.page.evaluate("window.confirm = () => true")
        self.botao_enviar.click()