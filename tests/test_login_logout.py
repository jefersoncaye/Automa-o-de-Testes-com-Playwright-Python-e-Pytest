from pages.cadastro_login import CadastroLogin
from playwright.sync_api import expect

def teste_login_invalido(page):
    """
    Valida que o login falha com credenciais inválidas.

    Cenário:
        1. Acessar a página de login/cadastro
        2. Tentar fazer login com email e senha incorretos
        3. Verificar que mensagem de erro é exibida

    Resultado Esperado:
        A mensagem "Your email or password is" deve ser visível indicando
        que o login falhou.
    """
    print("\n" + "="*80)
    print(teste_login_invalido.__doc__)
    print("="*80)
    login = CadastroLogin(page)
    login.acessar_cadastro_login()
    login.fazer_login(email='ashuiehasueh@sajuiehasueh.com', senha='15645645')
    expect(page.get_by_text("Your email or password is")).to_be_visible()

def teste_login_valido(page):
    """
    Valida que o login é bem-sucedido com credenciais válidas.

    Cenário:
        1. Acessar a página de login/cadastro
        2. Fazer login com credenciais válidas
        3. Verificar que o usuário foi autenticado

    Resultado Esperado:
        - Botão "Logout" deve estar visível
        - Mensagem "Logged in as Fulano" deve ser exibida na página
    """
    print("\n" + "="*80)
    print(teste_login_valido.__doc__)
    print("="*80)
    login = CadastroLogin(page)
    login.acessar_cadastro_login()
    login.fazer_login(email='teste123456789@teste.com', senha='123456')
    expect(page.get_by_role("link", name="Logout")).to_be_visible()
    expect(page.get_by_text("Logged in as Fulano")).to_be_visible()

def teste_logout(page):
    """
    Valida que o logout funciona corretamente.

    Cenário:
        1. Acessar a página inicial (home)
        2. Clicar no botão de logout
        3. Verificar que o usuário foi desconectado

    Resultado Esperado:
        A página de login com o heading "Login to your account" deve
        estar visível após o logout.
    """
    print("\n" + "="*80)
    print(teste_logout.__doc__)
    print("="*80)
    login = CadastroLogin(page)
    login.acessar_home()
    login.botao_logout.click()
    expect(page.get_by_role("heading", name="Login to your account")).to_be_visible()

def teste_usuario_nao_logado(page):
    """
    Valida que o botão de logout não é exibido para usuários não autenticados.

    Cenário:
        1. Acessar a página inicial (home) sem estar logado
        2. Verificar que o botão logout não está visível

    Resultado Esperado:
        O botão "Logout" não deve estar presente na página para
        usuários não autenticados.
    """
    print("\n" + "="*80)
    print(teste_usuario_nao_logado.__doc__)
    print("="*80)
    login = CadastroLogin(page)
    login.acessar_home()
    expect(page.get_by_role("link", name="Logout")).not_to_be_visible()