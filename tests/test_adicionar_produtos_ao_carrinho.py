from pages.produtos import Produtos
from pages.carrinho import Carrinho


def test_adicionar_produtos_ao_carrinho(page):
    """
    Valida que múltiplos produtos podem ser adicionados ao carrinho.

    Cenário:
        1. Acessar a página de produtos
        2. Adicionar primeiro produto (índice 0) ao carrinho
        3. Continuar comprando
        4. Adicionar segundo produto (índice 1) ao carrinho
        5. Continuar comprando
        6. Acessar o carrinho
        7. Validar que ambos os produtos estão corretos

    Resultado Esperado:
        - Primeiro produto: "Blue Top" de "Women > Tops" com preço Rs. 500
        - Segundo produto: "Men Tshirt" de "Men > Tshirts" com preço Rs. 400
        - Ambos os produtos devem estar visíveis no carrinho com preços corretos
    """
    print("\n" + "="*80)
    print(test_adicionar_produtos_ao_carrinho.__doc__)
    print("="*80)
    produtos = Produtos(page)
    carrinho = Carrinho(page)
    produtos.acessar_produtos()
    produtos.adicionar_produto_ao_carrinho(indice_produto='0')
    produtos.botao_continuar_comprando.click()
    produtos.adicionar_produto_ao_carrinho(indice_produto='1')
    produtos.botao_continuar_comprando.click()
    produtos.botao_carrinho.first.click()
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
