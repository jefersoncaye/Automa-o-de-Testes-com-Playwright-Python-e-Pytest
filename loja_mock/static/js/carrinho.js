const mensagemErro = document.getElementById('mensagem-erro');
const carrinhoVazio = document.getElementById('carrinho-vazio');
const tabelaCarrinho = document.getElementById('tabela-carrinho');
const corpoTabela = document.getElementById('corpo-tabela-carrinho');
const totalCarrinho = document.getElementById('total-carrinho');
const botaoSair = document.getElementById('botao-sair');

function exibirErro(texto) {
    mensagemErro.textContent = texto;
    mensagemErro.hidden = false;
}

function ocultarErro() {
    mensagemErro.hidden = true;
    mensagemErro.textContent = '';
}

function renderizarCarrinho(dados) {
    if (dados.itens.length === 0) {
        carrinhoVazio.hidden = false;
        tabelaCarrinho.hidden = true;
        totalCarrinho.textContent = '';
        return;
    }

    carrinhoVazio.hidden = true;
    tabelaCarrinho.hidden = false;
    corpoTabela.innerHTML = '';

    dados.itens.forEach((item) => {
        const linha = document.createElement('tr');
        linha.setAttribute('data-testid', `item-carrinho-${item.produto_id}`);
        linha.innerHTML = `
            <td>${item.nome}</td>
            <td>R$ ${item.preco.toFixed(2)}</td>
            <td>${item.quantidade}</td>
            <td>R$ ${item.subtotal.toFixed(2)}</td>
            <td><button data-testid="botao-remover-${item.produto_id}">Remover</button></td>
        `;

        const botaoRemover = linha.querySelector(`[data-testid="botao-remover-${item.produto_id}"]`);
        botaoRemover.addEventListener('click', () => removerItem(item.produto_id));

        corpoTabela.appendChild(linha);
    });

    totalCarrinho.textContent = `Total: R$ ${dados.subtotal.toFixed(2)}`;
}

async function carregarCarrinho() {
    ocultarErro();

    try {
        const resposta = await fetch('/api/carrinho');

        if (!resposta.ok) {
            if (resposta.status === 401) {
                window.location.href = '/login';
                return;
            }
            exibirErro('Erro ao carregar carrinho');
            return;
        }

        const dados = await resposta.json();
        renderizarCarrinho(dados);
    } catch (erro) {
        exibirErro('Erro de conexao com o servidor');
    }
}

async function removerItem(produtoId) {
    ocultarErro();

    try {
        const resposta = await fetch(`/api/carrinho/${produtoId}`, { method: 'DELETE' });

        if (!resposta.ok) {
            const dados = await resposta.json();
            exibirErro(dados.erro || 'Erro ao remover item');
            return;
        }

        await carregarCarrinho();
    } catch (erro) {
        exibirErro('Erro de conexao com o servidor');
    }
}

botaoSair.addEventListener('click', async () => {
    await fetch('/api/logout', { method: 'POST' });
    window.location.href = '/login';
});

carregarCarrinho();
