from playwright.sync_api import expect


def test_importar_arquivo_unico(page):
    page.goto('https://www.transfernow.net/pt')
    page.get_by_role("button", name="Aceitar e Continuar").click()
    with page.expect_file_chooser() as fc_info:
        page.get_by_role("button", name="Começar").click()
    file_chooser = fc_info.value
    file_chooser.set_files(r"C:\playwright_com_python_do_zero_automacao_profissional\stores\teste_importar_arquivo\teste123.txt")
    page.get_by_role("button", name="Criar um link").click()
    page.get_by_role("textbox", name="Seu e-mail").fill("teste@teste123124.com")
    page.get_by_role("button", name="Obter um link").click()
    expect(page.get_by_text("Seu link está pronto!")).to_be_visible(timeout=30000)

def test_importar_arquivo_multiplos(page):
    page.goto('https://www.transfernow.net/pt')
    page.get_by_role("button", name="Aceitar e Continuar").click()
    with page.expect_file_chooser() as fc_info:
        page.get_by_role("button", name="Começar").click()
    file_chooser = fc_info.value
    file_chooser.set_files([r"C:\playwright_com_python_do_zero_automacao_profissional\stores\teste_importar_arquivo\teste123.txt",
                            r'C:\playwright_com_python_do_zero_automacao_profissional\stores\teste_importar_arquivo\teste321.txt'])
    page.get_by_role("button", name="Criar um link").click()
    page.get_by_role("textbox", name="Seu e-mail").fill("teste@teste123124.com")
    page.get_by_role("button", name="Obter um link").click()
    expect(page.get_by_text("Seu link está pronto!")).to_be_visible(timeout=30000)
