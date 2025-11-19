from pages.produtos import Produtos
from pages.carrinho import Carrinho


def test_adicionar_produto_caso_preco_menor_que_500(page):
    produtos = Produtos(page)
    produtos.acessar_produtos()
    preco_produto = int(produtos.card_produto.nth(1).locator('.productinfo h2').inner_text().replace('Rs. ', ''))
    print(preco_produto)
    print(type(preco_produto))
    if preco_produto <= 500:
        produtos.adicionar_produto_ao_carrinho(indice_produto=1)
        print('Produto com preço menor que 500, FOI adicionado ao carrinho')
    else:
        print('Produto com preço maior que 500, NÃO FOI foi adicionado ao carrinho')

def test_excluir_todos_produtos_carrinho(page):
    carrinho = Carrinho(page)
    carrinho.acessar_carrinho()
    while carrinho.botao_deletar_produto.first.is_visible():
        carrinho.botao_deletar_produto.first.click()
        page.wait_for_timeout(1000)