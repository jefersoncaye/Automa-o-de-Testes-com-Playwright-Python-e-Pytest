from playwright.sync_api import expect
from pages.cadastro_login import CadastroLogin
from pages.produtos import Produtos
from pages.carrinho import Carrinho

def teste_login(page):
    login = CadastroLogin(page)
    login.acessar_cadastro_login()
    login.fazer_login(email='teste@testeabcde.com', senha='123456789')
    expect(page.get_by_role("link", name="Logout")).to_be_visible()

def test_adicionar_produtos_ao_carrinho(page):
    produtos = Produtos(page)
    produtos.acessar_produtos()
    produtos.adicionar_produto_ao_carrinho(indice_produto='0')
    produtos.botao_continuar_comprando.click()
    produtos.adicionar_produto_ao_carrinho(indice_produto='1')
    produtos.botao_continuar_comprando.click()

def test_validar_carrinho(page):
    carrinho = Carrinho(page)
    carrinho.acessar_carrinho()
    carrinho.validar_carrinho(indice_produto='0',
                              cabecalho_descricao_produto='Blue Top',
                              descricao_produto='Women > Tops',
                              preco_produto='Rs. 500',
                              preco_total_produto='Rs. 500')
    carrinho.validar_carrinho(indice_produto='1',
                              cabecalho_descricao_produto='Men Tshirt',
                              descricao_produto='Men > Tshirts',
                              preco_produto='Rs. 400',
                              preco_total_produto='Rs. 400')