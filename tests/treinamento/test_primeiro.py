

def test_abrir_google(page):
    page.goto('https://www.google.com/')
    page.get_by_role("button", name="Pesquisa Google").click()
    assert "Google" in page.title()

def test_abrir_google2(page):
    page.goto('https://www.google.com/')
    page.get_by_role("button", name="Pesquisa Google").click()
    assert "Google" in page.title()