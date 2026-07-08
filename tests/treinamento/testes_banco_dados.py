"""
Exemplos da aula: Utilitario para Validacao de Banco de Dados.

Demonstra todas as funcoes de utilitarios/banco_dados.py contra o banco
de exemplo loja.db (SQLite), na raiz do projeto.

Pre-requisito:
    Rodar o script de criacao do banco para gerar o arquivo loja.db.

Execucao:
    python tests/treinamento/testes_banco_dados.py
"""

from pathlib import Path

from utilitarios.banco_dados import (
    atualizar,
    contar_registros,
    criar_engine,
    executar_comando,
    executar_query,
    imprimir_resultado,
    inserir,
    montar_connection_string,
    registro_existe,
    registro_nao_existe,
    salvar_resultado_em_arquivo,
    validar_resultado_esperado,
    validar_valor_coluna,
)

# Raiz do projeto: duas pastas acima de tests/treinamento/.
RAIZ_PROJETO = Path(__file__).resolve().parents[2]

EMAIL_TESTE = 'ana@teste.com'


def titulo(texto):
    """Imprime um cabecalho para separar os blocos de exemplo no console."""
    print(f'\n{"=" * 60}\n{texto}\n{"=" * 60}')


# ---------------------------------------------------------------------------
# 1. Conexao
# ---------------------------------------------------------------------------
def exemplo_conexao():
    """Monta a connection string e cria a engine do SQLAlchemy."""
    titulo('1. CONEXAO')

    connection_string = montar_connection_string('sqlite', database='loja.db')
    print(f'Connection string: {connection_string}')

    return criar_engine(connection_string)


# ---------------------------------------------------------------------------
# 2. Consultando dados
# ---------------------------------------------------------------------------
def exemplo_consulta(engine):
    """Le dados do banco e exibe o resultado formatado."""
    titulo('2. CONSULTANDO DADOS')

    print('Tabela usuarios:')
    imprimir_resultado(engine, 'SELECT id, nome, email, ativo FROM usuarios')

    print('\nTabela produtos:')
    imprimir_resultado(engine, 'SELECT id, nome, preco, estoque FROM produtos')

    # executar_query devolve (colunas, linhas) para uso direto no codigo.
    colunas, linhas = executar_query(engine, 'SELECT nome, preco FROM produtos')
    print(f'\nColunas: {colunas}')
    print(f'Primeira linha: {linhas[0]}')


# ---------------------------------------------------------------------------
# 3. Validadores
# ---------------------------------------------------------------------------
def exemplo_validadores(engine):
    """Os quatro tipos de validacao do utilitario."""
    titulo('3. VALIDADORES')

    # Existe ao menos um registro?
    registro_existe(
        engine,
        'SELECT * FROM usuarios WHERE email = :email',
        {'email': 'joao@teste.com'},
    )

    # Nao existe nenhum registro? (util apos exclusoes)
    registro_nao_existe(
        engine,
        'SELECT * FROM usuarios WHERE email = :email',
        {'email': 'naoexiste@teste.com'},
    )

    # Quantidade exata de registros.
    contar_registros(engine, 'SELECT * FROM usuarios WHERE ativo = 1', 2)

    # Valor de uma coluna especifica.
    validar_valor_coluna(
        engine,
        'SELECT nome, preco FROM produtos WHERE nome = :nome',
        'preco',
        199.90,
        {'nome': 'Calca Jeans'},
    )

    # Resultado completo comparado com um gabarito.
    validar_resultado_esperado(
        engine,
        'SELECT nome, estoque FROM produtos ORDER BY id',
        [
            ['Camiseta Preta', 50],
            ['Calca Jeans', 20],
            ['Tenis Esportivo', 10],
        ],
    )


# ---------------------------------------------------------------------------
# 4. Quando a validacao falha
# ---------------------------------------------------------------------------
def exemplo_validacao_falha(engine):
    """Mostra a mensagem de erro quando um validador nao passa."""
    titulo('4. QUANDO A VALIDACAO FALHA')

    try:
        contar_registros(engine, 'SELECT * FROM usuarios WHERE ativo = 1', 5)
    except AssertionError as erro:
        print(f'AssertionError: {erro}')


# ---------------------------------------------------------------------------
# 5. Escrita: massa de dados e limpeza
# ---------------------------------------------------------------------------
def exemplo_escrita(engine):
    """INSERT para criar massa, UPDATE para forcar cenario, DELETE para limpar."""
    titulo('5. ESCRITA (INSERT / UPDATE / DELETE)')

    # INSERT - cria a massa de dados.
    linhas = inserir(engine, 'usuarios', {
        'nome': 'Ana Prova',
        'email': EMAIL_TESTE,
        'ativo': 1,
        'data_cadastro': '2026-02-01',
    })
    print(f'Registros inseridos: {linhas}')
    registro_existe(
        engine,
        'SELECT * FROM usuarios WHERE email = :email',
        {'email': EMAIL_TESTE},
    )

    # UPDATE - forca um cenario dificil de alcancar pela interface.
    linhas = atualizar(
        engine,
        'usuarios',
        {'ativo': 0},
        'email = :email',
        {'email': EMAIL_TESTE},
    )
    print(f'\nRegistros atualizados: {linhas}')
    validar_valor_coluna(
        engine,
        'SELECT ativo FROM usuarios WHERE email = :email',
        'ativo',
        0,
        {'email': EMAIL_TESTE},
    )

    # DELETE - limpeza, para o teste nao contaminar os proximos.
    linhas = executar_comando(
        engine,
        'DELETE FROM usuarios WHERE email = :email',
        {'email': EMAIL_TESTE},
    )
    print(f'\nRegistros removidos: {linhas}')
    registro_nao_existe(
        engine,
        'SELECT * FROM usuarios WHERE email = :email',
        {'email': EMAIL_TESTE},
    )


# ---------------------------------------------------------------------------
# 6. Rollback automatico
# ---------------------------------------------------------------------------
def exemplo_rollback(engine):
    """Se o comando falha, engine.begin() desfaz a transacao automaticamente."""
    titulo('6. ROLLBACK AUTOMATICO')

    _, linhas = executar_query(engine, 'SELECT * FROM usuarios')
    total_antes = len(linhas)
    print(f'Usuarios antes do comando invalido: {total_antes}')

    try:
        executar_comando(engine, 'INSERT INTO usuarios (coluna_inexistente) VALUES (1)')
    except Exception as erro:
        print(f'Erro capturado: {type(erro).__name__}')

    # O banco continua intacto: nada foi gravado pela metade.
    contar_registros(engine, 'SELECT * FROM usuarios', total_antes)


# ---------------------------------------------------------------------------
# 7. Exportando o resultado para arquivo
# ---------------------------------------------------------------------------
def exemplo_exportar_arquivo(engine):
    """Salva o resultado da query num .txt formatado.

    O arquivo gerado pode ser comparado com um gabarito usando o utilitario
    comparar_arquivos, da aula de comparacao de arquivos.
    """
    titulo('7. EXPORTANDO RESULTADO PARA ARQUIVO')

    destino = RAIZ_PROJETO / 'stores' / 'produtos_atual.txt'
    destino.parent.mkdir(parents=True, exist_ok=True)

    salvar_resultado_em_arquivo(
        engine,
        'SELECT id, nome, preco FROM produtos ORDER BY id',
        str(destino),
    )

    print(f'Arquivo gerado: {destino}\n')
    print(destino.read_text(encoding='utf-8'))


def limpar_massa_residual(engine):
    """Remove a massa de testes deixada por execucoes anteriores.

    Garante que o script possa ser executado varias vezes seguidas.
    """
    executar_comando(
        engine,
        'DELETE FROM usuarios WHERE email = :email',
        {'email': EMAIL_TESTE},
    )


def main():
    """Executa todos os exemplos da aula em sequencia."""
    engine = exemplo_conexao()
    limpar_massa_residual(engine)

    exemplo_consulta(engine)
    exemplo_validadores(engine)
    exemplo_validacao_falha(engine)
    exemplo_escrita(engine)
    exemplo_rollback(engine)
    exemplo_exportar_arquivo(engine)

    titulo('FIM - todos os exemplos executados com sucesso')


if __name__ == '__main__':
    main()
