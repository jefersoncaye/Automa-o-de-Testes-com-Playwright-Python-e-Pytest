import re
from openpyxl import load_workbook
import pandas as pd
import os
import tempfile
import PyPDF2
from typing import Optional


def comparar_arquivos(arquivo_base, arquivo_atual, linhas_ignorar=None, padrao_ignorar='', bytes_ignorar=0,
                      encoding='utf-8'):
    """
    Faz a comparação linha por linha de dois arquivos
    Caso algum arquivo tenha linhas a mais, será apresentado a mensagem "Os arquivos têm tamanhos diferentes, podem existir mais diferenças!"
    Caso seja necessario uma ou mais linhas especificas do arquivo, passar linhas em forma de lista no parametro "linhas_ignorar"
    Caso queira ignorar tag ou algum padrão, passar na variavel 'padrao_ignorar' (precisa ser um padrão ReGex)
    Caso queira ignorar uma quantidade de bytes especifica, passar o parametro bytes_ignorar, lembrar de alterar no arquivo base para sempre ser um caracter diferente
    """
    if linhas_ignorar is None:
        linhas_ignorar = []
    with open(arquivo_base, 'r', encoding=encoding) as f1, open(arquivo_atual, 'r', encoding=encoding) as f2:
        linhas_arquivo1 = f1.readlines()
        linhas_arquivo2 = f2.readlines()
    tem_diferenca = False
    bytes_diferenca = 0
    for i, (linha1, linha2) in enumerate(zip(linhas_arquivo1, linhas_arquivo2)):
        if (i + 1) in linhas_ignorar:
            continue
        if padrao_ignorar:
            linha1 = re.sub(padrao_ignorar, '', linha1, flags=re.DOTALL)
            linha2 = re.sub(padrao_ignorar, '', linha2, flags=re.DOTALL)
        if linha1 != linha2:
            print(f'Diferença na linha {i + 1}:')
            print(f'Arquivo Base:  {linha1.strip()}')
            print(f'Arquivo Atual: {linha2.strip()}')
            bytes_linha1 = linha1.encode()
            bytes_linha2 = linha2.encode()
            max_len = max(len(bytes_linha1), len(bytes_linha2))
            for j in range(max_len):
                try:
                    if bytes_linha1[j] != bytes_linha2[j]:
                        bytes_diferenca += 1
                except IndexError:
                    bytes_diferenca += 1
            if bytes_diferenca > bytes_ignorar or bytes_ignorar == 0:
                tem_diferenca = True

    assert len(linhas_arquivo2) > 0, 'Arquivo atual está em branco, Verifique!'

    assert len(linhas_arquivo1) == len(
        linhas_arquivo2), 'Os arquivos têm tamanhos diferentes, podem existir mais diferenças!'

    if not tem_diferenca:
        print(f'\nArquivos {arquivo_base} e {arquivo_atual} são iguais!, estão sendo ignorados {bytes_ignorar} Bytes')

    assert not tem_diferenca, f'\nArquivos com diferenças' \
                              f'\n{bytes_diferenca} Bytes de diferença!, foi configurado para ignorar {bytes_ignorar} Bytes' \
                              f'\nPara mais informações compare os arquivos Base: {arquivo_base} e Atual: {arquivo_atual} ' \
                              f'com algum utilitario de sua preferencia'
    assert bytes_ignorar == bytes_diferenca, (
        f'A quantidade de bytes a ingorar não é a mesma que a diferença de bytes entre os arquivos, verifique!\n'
        f'Bytes ignorar: {bytes_ignorar}\n'
        f'Bytes diferença: {bytes_diferenca}')


def comparar_arquivos_excel(
    arquivo_base: str,
    arquivo_atual: str,
    bytes_ignorar: int = 0,
    comparar_headers: bool = True,
) -> None:
    """
    Compara duas planilhas Excel célula a célula, incluindo os cabeçalhos.

    Suporta arquivos .xls (via xlrd) e .xlsx (via openpyxl). A comparação é feita
    sobre os valores das células convertidos para string, garantindo compatibilidade
    entre tipos mistos.

    Args:
        arquivo_base: Caminho para a planilha de referência (gabarito).
        arquivo_atual: Caminho para a planilha gerada pelo sistema sob teste.
        bytes_ignorar: Tolerância em bytes entre as planilhas. Se a diferença total
            for exatamente igual a este valor, os arquivos são considerados equivalentes.
            Use 0 para exigir igualdade total.
        comparar_headers: Se True (padrão), inclui a linha de cabeçalho na comparação.
            Passe False para ignorar diferenças nos nomes das colunas.

    Raises:
        AssertionError: Se as planilhas tiverem dimensões diferentes.
        AssertionError: Se houver diferenças de conteúdo além da tolerância configurada.
        AssertionError: Se `bytes_ignorar` for maior que zero mas a diferença real
            não for exatamente igual a ele.
    """
    engine_base = 'xlrd' if arquivo_base.endswith('.xls') else 'openpyxl'
    engine_atual = 'xlrd' if arquivo_atual.endswith('.xls') else 'openpyxl'

    df_base = pd.read_excel(arquivo_base, engine=engine_base).fillna('')
    df_atual = pd.read_excel(arquivo_atual, engine=engine_atual).fillna('')

    tem_diferenca = False
    bytes_diferenca = 0

    if df_base.shape != df_atual.shape:
        raise AssertionError("As planilhas não têm o mesmo tamanho, podem existir mais diferenças")

    if comparar_headers:
        headers_base = list(df_base.columns)
        headers_atual = list(df_atual.columns)
        if headers_base != headers_atual:
            print("Diferença nos cabeçalhos:")
            print(f"  Base:  {headers_base}")
            print(f"  Atual: {headers_atual}")

    for row_idx in range(df_base.shape[0]):
        for col_idx in range(df_base.shape[1]):
            cell1 = str(df_base.iat[row_idx, col_idx])
            cell2 = str(df_atual.iat[row_idx, col_idx])
            if cell1 != cell2:
                nome_coluna = df_base.columns[col_idx]
                print(f"Diferença na linha {row_idx + 1}, coluna '{nome_coluna}' (índice {col_idx + 1}):")
                print(f'Arquivo Base:  {cell1}')
                print(f'Arquivo Atual: {cell2}')
                max_len = max(len(cell1.encode()), len(cell2.encode()))
                for j in range(max_len):
                    try:
                        if cell1.encode()[j] != cell2.encode()[j]:
                            bytes_diferenca += 1
                    except IndexError:
                        bytes_diferenca += 1
                if bytes_diferenca > bytes_ignorar or bytes_ignorar == 0:
                    tem_diferenca = True

    if not tem_diferenca:
        print(f'\nArquivos {arquivo_base} e {arquivo_atual} são iguais!, estão sendo ignorados {bytes_ignorar} Bytes')

    assert not tem_diferenca, (
        f'\nArquivos com diferenças'
        f'\n{bytes_diferenca} Bytes de diferença!, foi configurado para ignorar {bytes_ignorar} Bytes'
        f'\nPara mais informações compare os arquivos Base: {arquivo_base} e Atual: {arquivo_atual} '
        f'com algum utilitário de sua preferência'
    )

    assert bytes_ignorar == bytes_diferenca, (
        f'A quantidade de bytes a ignorar não é a mesma que a diferença de bytes entre os arquivos, verifique!\n'
        f'Bytes ignorar: {bytes_ignorar}\n'
        f'Bytes diferença: {bytes_diferenca}'
    )


def converter_pdf_para_texto(arquivo_pdf: str) -> str:
    """
    Converte um arquivo PDF em texto simples para comparação em testes.

    O texto extraído é normalizado para facilitar comparações consistentes:
    - Quebras de linha múltiplas são colapsadas em uma única.
    - Espaços e tabulações consecutivos são reduzidos a um único espaço.
    - Espaços em branco no início e fim são removidos.

    Args:
        arquivo_pdf: Caminho para o arquivo PDF a ser convertido.

    Returns:
        String com o texto extraído e normalizado de todas as páginas.

    Raises:
        RuntimeError: Se ocorrer erro durante a leitura ou extração do PDF.
    """
    paginas_texto = []

    try:
        with open(arquivo_pdf, 'rb') as f:
            leitor_pdf = PyPDF2.PdfReader(f)

            for pagina in leitor_pdf.pages:
                texto_pagina = pagina.extract_text()
                if texto_pagina:
                    paginas_texto.append(texto_pagina)

    except Exception as e:
        raise RuntimeError(f"Erro ao ler o PDF '{arquivo_pdf}': {e}") from e

    texto = "\n".join(paginas_texto)

    texto = texto.replace('\r', '\n')
    texto = re.sub(r'\n+', '\n', texto)
    texto = re.sub(r'[ \t]+', ' ', texto)
    texto = texto.strip()

    return texto


def converter_e_comparar_pdf(
    arquivo_base: str,
    arquivo_atual: str,
    linhas_ignorar: Optional[list[int]] = None,
    padrao_ignorar: str = '',
    bytes_ignorar: int = 0,
    encoding: str = 'utf-8',
) -> None:
    """
    Extrai o texto de PDFs e os compara linha por linha.

    O texto extraído é salvo em arquivos temporários gerenciados automaticamente
    (removidos ao final, mesmo em caso de falha). Se `arquivo_base` não for um PDF,
    ele é usado diretamente como gabarito em texto puro — útil para manter arquivos
    de referência versionados sem precisar de PDFs.

    O encoding padrão desta função é UTF-8, mais adequado para texto extraído de PDF
    do que latin-1 (usado nos comparadores de arquivos de texto puro).

    Args:
        arquivo_base: Caminho para o PDF de referência (gabarito), ou arquivo de texto
            puro caso o gabarito já esteja em formato .txt.
        arquivo_atual: Caminho para o PDF gerado pelo sistema sob teste.
        linhas_ignorar: Lista de números de linha (1-based) a ignorar na comparação.
        padrao_ignorar: Padrão regex removido de cada linha antes da comparação.
        bytes_ignorar: Tolerância em bytes. Ver docstring de `comparar_arquivos`.
        encoding: Encoding para escrita dos arquivos temporários. Padrão: 'utf-8'.

    Raises:
        RuntimeError: Se falhar a extração de texto de algum PDF.
        AssertionError: Propagado de `comparar_arquivos` em caso de diferenças.
    """
    with tempfile.NamedTemporaryFile(
        mode='w', suffix='.txt', encoding=encoding, delete=False
    ) as f_atual:
        temp_atual = f_atual.name
        f_atual.write(converter_pdf_para_texto(arquivo_atual))

    temp_base = None

    try:
        if arquivo_base.lower().endswith('.pdf'):
            with tempfile.NamedTemporaryFile(
                mode='w', suffix='.txt', encoding=encoding, delete=False
            ) as f_base:
                temp_base = f_base.name
                f_base.write(converter_pdf_para_texto(arquivo_base))
            base_para_comparar = temp_base
        else:
            base_para_comparar = arquivo_base

        comparar_arquivos(base_para_comparar, temp_atual, linhas_ignorar, padrao_ignorar, bytes_ignorar,
                          encoding=encoding)
    finally:
        os.remove(temp_atual)
        if temp_base and os.path.exists(temp_base):
            os.remove(temp_base)

r"""
comparar_arquivos(arquivo_base=r'C:\Users\Pichau\Desktop\arquivos\relatorio_base.txt',
                  arquivo_atual=r'C:\Users\Pichau\Desktop\arquivos\relatorio_atual.txt',
                  padrao_ignorar=r"\d{2}/\d{2}/\d{4}")

comparar_arquivos_excel(r'C:\Users\Pichau\Desktop\arquivos\planilha_base.xlsx',
                        r'C:\Users\Pichau\Desktop\arquivos\planilha_atual.xlsx',
                        )

converter_e_comparar_pdf(r'C:\Users\Pichau\Desktop\arquivos\relatorio_base.pdf',
                        r'C:\Users\Pichau\Desktop\arquivos\relatorio_atual.pdf',
                        )
"""
