import pytest
from pages.cadastro_login import CadastroLogin
from playwright.sync_api import expect


@pytest.mark.parametrize("email,senha", [
    ("usuario_falso@fake.com", "qualquersenha"),
    ("naoexiste@dominio.org", "senha123"),
    ("xyz@emailinexistente.net", "abc456"),
], ids=["fake_usuario", "fake_dominio", "email_inexistente"])
def teste_login_email_invalido(page, email, senha):
    login = CadastroLogin(page)
    login.acessar_cadastro_login()
    login.fazer_login(email=email, senha=senha)
    expect(page.get_by_text("Your email or password is")).to_be_visible()


@pytest.mark.parametrize("senha", [
    "senhaerrada",
    "123456789errado",
    "SENHAERRADA",
], ids=["alfanumerica", "longa_errada", "maiuscula"])
def teste_login_senha_incorreta(page, senha):
    login = CadastroLogin(page)
    login.acessar_cadastro_login()
    login.fazer_login(email="teste@testeabcde.com", senha=senha)
    expect(page.get_by_text("Your email or password is")).to_be_visible()


@pytest.mark.parametrize("email,senha", [
    ("", ""),
    ("", "123456"),
    ("teste@testeabcde.com", ""),
], ids=["ambos_vazios", "email_vazio", "senha_vazia"])
def teste_login_campos_vazios(page, email, senha):
    login = CadastroLogin(page)
    login.acessar_cadastro_login()
    login.fazer_login(email=email, senha=senha)
    expect(page.get_by_role("heading", name="Login to your account")).to_be_visible()