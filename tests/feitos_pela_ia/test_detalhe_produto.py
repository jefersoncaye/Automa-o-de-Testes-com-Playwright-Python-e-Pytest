from playwright.sync_api import expect
from pages.detalhe_produto import DetalheProduto

ENDPOINT = "product_details/1"


def test_nome_produto_visivel(page):
    page.goto(ENDPOINT)
    produto = DetalheProduto(page)
    expect(produto.nome_produto).to_be_visible()


def test_preco_produto_visivel(page):
    page.goto(ENDPOINT)
    produto = DetalheProduto(page)
    expect(produto.preco).to_be_visible()


def test_disponibilidade_em_estoque(page):
    page.goto(ENDPOINT)
    produto = DetalheProduto(page)
    expect(produto.disponibilidade).to_be_visible()


def test_condicao_novo(page):
    page.goto(ENDPOINT)
    produto = DetalheProduto(page)
    expect(produto.condicao).to_be_visible()


def test_marca_polo(page):
    page.goto(ENDPOINT)
    produto = DetalheProduto(page)
    expect(produto.marca).to_be_visible()


def test_adicionar_produto_ao_carrinho(page):
    page.goto(ENDPOINT)
    produto = DetalheProduto(page)
    produto.adicionar_ao_carrinho()
    expect(produto.modal_titulo).to_be_visible()
    expect(produto.modal_mensagem).to_be_visible()