from pages.inscreverse import Inscreverse
from playwright.sync_api import expect


def test_registrar_novo_usuario(page):
    inscrever = Inscreverse(page)
    inscrever.acessar_home()
    inscrever.botao_cadastro_login.click()
    expect(page.get_by_text('New User Signup!', exact=True)).to_be_visible()
    inscrever.realizar_cadastro(
        nome='Fulano',
        email='teste123456789@teste.com')
    expect(
        page.get_by_text(
            'Enter Account Information',
            exact=True)).to_be_visible()
    inscrever.preencher_informacoes_da_conta(
        titulo='Mr',
        senha='123456',
        data_aniversario='08/08/2001',
        receive_special_offers_from=True,
        sign_up_for_our_newsletter=True)
    inscrever.preencher_informacoes_endereco(primeiro_nome='Fulano',
                                             sobrenome='Silva',
                                             empresa='Teste',
                                             endereco='Rua ali',
                                             pais='United States',
                                             estado='Nova York',
                                             cidade='Nova York',
                                             zipcode='10001',
                                             numero_telefone='55 999999999')
    inscrever.botao_criar_conta.click()
    expect(page.get_by_text('Account Created!')).to_be_visible()
    inscrever.botao_continuar.click()
    expect(page.get_by_text("Logged in as Fulano")).to_be_visible()


def test_deletar_novo_usuario(page):
    inscrever = Inscreverse(page)
    inscrever.acessar_home()
    inscrever.botao_deletar_conta.click()
    expect(page.get_by_text("Account Deleted!")).to_be_visible()
