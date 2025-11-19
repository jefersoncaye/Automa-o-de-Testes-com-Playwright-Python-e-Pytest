from pages.base_page import BasePage
from playwright.sync_api import expect

def test_validar_home(page):
    """
    - Acessar o home
    - Validar se o cabeçalho "AutomationExercise" está visivel
    """
    print(test_validar_home.__doc__)
    pagina = BasePage(page)
    pagina.acessar_home()
    expect(page.get_by_role("heading", name="AutomationExercise")).to_be_visible()


def test_validar_produtos(page):
    """
    - Acessar o Produtos
    - Validar se a imagem "Website for practice" está visivel
    """
    print(test_validar_produtos.__doc__)
    pagina = BasePage(page)
    pagina.acessar_produtos()
    expect(page.get_by_role("img", name="Website for practice")).to_be_visible()


def test_validar_carrinho(page):
    """
    - Acessar o home
    - Validar se o texto "Home Shopping Cart" está visivel
    """
    print(test_validar_carrinho.__doc__)
    pagina = BasePage(page)
    pagina.acessar_carrinho()
    expect(page.get_by_text("Home Shopping Cart")).to_be_visible()


def test_validar_login(page):
    """
    - Acessar o home
    - Validar se o cabeçalho "Login to your account" está visivel
    """
    print(test_validar_login.__doc__)
    pagina = BasePage(page)
    pagina.acessar_cadastro_login()
    expect(page.get_by_role("heading", name="Login to your account")).to_be_visible()
