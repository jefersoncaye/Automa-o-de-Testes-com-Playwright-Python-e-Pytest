from playwright.sync_api import expect
from pages.contato import Contato


def test_enviar_formulario_com_sucesso(page):
    contato = Contato(page)
    contato.acessar_contato()
    contato.preencher_formulario(
        nome="João Silva",
        email="joao.silva@email.com",
        assunto="Dúvida sobre o site",
        mensagem="Olá, gostaria de saber mais informações sobre os produtos disponíveis no site."
    )
    contato.enviar_formulario()
    expect(contato.mensagem_sucesso).to_be_visible()


def test_enviar_formulario_com_campos_vazios(page):
    contato = Contato(page)
    contato.acessar_contato()
    contato.botao_enviar.click()
    expect(contato.mensagem_sucesso).not_to_be_visible()
    expect(contato.campo_nome).to_be_visible()