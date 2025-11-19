from pages.produtos import Produtos
from pages.carrinho import Carrinho


def test_adicionar_produtos_ao_carrinho(page):
    produtos = Produtos(page)
    carrinho = Carrinho(page)
    produtos.acessar_produtos()
    produtos.adicionar_produto_ao_carrinho(indice_produto='0')
    produtos.botao_continuar_comprando.click()
    produtos.adicionar_produto_ao_carrinho(indice_produto='1')
    produtos.botao_continuar_comprando.click()
    produtos.botao_carrinho.click()
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
