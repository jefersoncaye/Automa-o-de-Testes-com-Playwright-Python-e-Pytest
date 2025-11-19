import os


def test_baixar_arquivos(page):
    page.goto('https://www.transfernow.net/pt/cld?utm_source=202508103hxk0f6q')
    page.pause()
    with page.expect_download() as download_info:
        page.get_by_role("link", name="Baixar tudo").click()
    download = download_info.value
    caminho_final = fr"C:\playwright_com_python_do_zero_automacao_profissional\stores\teste_importar_arquivo\{download.suggested_filename}"
    download.save_as(caminho_final)

    assert os.path.exists(caminho_final), 'Não encontrei o arquivo baixado'
