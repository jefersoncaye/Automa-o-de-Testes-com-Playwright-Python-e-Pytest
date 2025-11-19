from pages.produtos import Produtos
from pages.carrinho import Carrinho


def test_adicionar_produto_ao_carrinho_caso_menor_que_500(page):
    produtos = Produtos(page)
    produtos.acessar_produtos()
    preco_produto = int(produtos.card_produto.nth(2).locator('.productinfo h2').inner_text().replace('Rs. ', ''))
    print(preco_produto)
    print(type(preco_produto))
    if preco_produto <= 500:
        produtos.adicionar_produto_ao_carrinho(indice_produto=2)
        print('Produto com valor menor que 500, adicionado ao carrinho')
    else:
        print('Produto com valor maior que 500, não foi adicionado ao carrinho')


def test_excluir_todos_produtos_carrinho(page):
    carrinho = Carrinho(page)
    carrinho.acessar_carrinho()
    page.pause()
    while carrinho.botao_excluir_produto.first.is_visible():
        carrinho.botao_excluir_produto.first.click()
        page.wait_for_timeout(1000)
