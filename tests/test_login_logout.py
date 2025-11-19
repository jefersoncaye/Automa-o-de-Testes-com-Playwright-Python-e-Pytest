from pages.cadastro_login import CadastroLogin
from playwright.sync_api import expect

def teste_login_invalido(page):
    login = CadastroLogin(page)
    login.acessar_cadastro_login()
    login.fazer_login(email='ashuiehasueh@sajuiehasueh.com', senha='15645645')
    expect(page.get_by_text("Your email or password is")).to_be_visible()

def teste_login_valido(page):
    login = CadastroLogin(page)
    login.acessar_cadastro_login()
    login.fazer_login(email='teste@testeabcde.com', senha='123456789')
    expect(page.get_by_role("link", name="Logout")).to_be_visible()
    expect(page.get_by_text("Logged in as Fulano")).to_be_visible()

def teste_logout(page):
    login = CadastroLogin(page)
    login.acessar_home()
    login.botao_logout.click()
    expect(page.get_by_role("heading", name="Login to your account")).to_be_visible()

def teste_usuario_nao_logado(page):
    login = CadastroLogin(page)
    login.acessar_home()
    expect(page.get_by_role("link", name="Logout")).not_to_be_visible()