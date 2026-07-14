const listaProdutos = document.getElementById('lista-produtos');
const mensagemErro = document.getElementById('mensagem-erro');
const selectCategoria = document.getElementById('select-categoria');
const contadorCarrinho = document.getElementById('contador-carrinho');
const botaoSair = document.getElementById('botao-sair');

function exibirErro(texto) {
    mensagemErro.textContent = texto;
    mensagemErro.hidden = false;
}

function ocultarErro() {
    mensagemErro.hidden = true;
    mensagemErro.textContent = '';
}

function renderizarProdutos(produtos) {
    listaProdutos.innerHTML = '';

    produtos.forEach((produto) => {
        const card = document.createElement('div');
        card.className = 'produto-card';
        card.setAttribute('data-testid', `produto-${produto.id}`);

        const semEstoque = produto.estoque <= 0;

        card.innerHTML = `
            <img src="${produto.imagem}" alt="${produto.nome}" onerror="this.style.display='none'">
            <h3>${produto.nome}</h3>
            <div class="produto-preco">R$ ${produto.preco.toFixed(2)}</div>
            <div class="produto-estoque ${semEstoque ? 'produto-sem-estoque' : ''}">
                ${semEstoque ? 'Sem estoque' : `Estoque: ${produto.estoque}`}
            </div>
            <button data-testid="botao-adicionar-${produto.id}" ${semEstoque ? 'disabled' : ''}>
                Adicionar ao carrinho
            </button>
        `;

        const botaoAdicionar = card.querySelector(`[data-testid="botao-adicionar-${produto.id}"]`);
        botaoAdicionar.addEventListener('click', () => adicionarAoCarrinho(produto.id));

        listaProdutos.appendChild(card);
    });
}

async function carregarProdutos(categoria) {
    ocultarErro();

    try {
        const url = categoria ? `/api/produtos?categoria=${encodeURIComponent(categoria)}` : '/api/produtos';
        const resposta = await fetch(url);

        if (!resposta.ok) {
            if (resposta.status === 401) {
                window.location.href = '/login';
                return;
            }
            exibirErro('Erro ao carregar produtos');
            return;
        }

        const produtos = await resposta.json();
        renderizarProdutos(produtos);
    } catch (erro) {
        exibirErro('Erro de conexao com o servidor');
    }
}

async function adicionarAoCarrinho(produtoId) {
    ocultarErro();

    try {
        const resposta = await fetch('/api/carrinho', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ produto_id: produtoId, quantidade: 1 }),
        });

        const dados = await resposta.json();

        if (!resposta.ok) {
            exibirErro(dados.erro || 'Erro ao adicionar ao carrinho');
            return;
        }

        await atualizarContadorCarrinho();
    } catch (erro) {
        exibirErro('Erro de conexao com o servidor');
    }
}

async function atualizarContadorCarrinho() {
    try {
        const resposta = await fetch('/api/carrinho');
        if (!resposta.ok) return;
        const dados = await resposta.json();
        contadorCarrinho.textContent = dados.quantidade_total;
    } catch (erro) {
        // Falha silenciosa no contador nao bloqueia a pagina
    }
}

selectCategoria.addEventListener('change', () => {
    carregarProdutos(selectCategoria.value);
});

botaoSair.addEventListener('click', async () => {
    await fetch('/api/logout', { method: 'POST' });
    window.location.href = '/login';
});

carregarProdutos('');
atualizarContadorCarrinho();
