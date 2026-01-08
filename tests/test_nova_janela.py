
def test_nova_janela(page):
    page.goto("https://demoqa.com/browser-windows")

    with page.expect_popup() as window_info:
        page.locator('#windowButton').click()

    nova_janela = window_info.value
    nova_janela.wait_for_load_state()
    context = page.context
    print(f"\nTotal de janelas abertas: {len(context.pages)}")
    print(context.pages)

    nova_janela.screenshot(path="nova_janela.png")

    nova_janela.close()
