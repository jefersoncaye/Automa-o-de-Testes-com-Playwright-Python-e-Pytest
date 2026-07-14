const formLogin = document.getElementById('form-login');
const mensagemErro = document.getElementById('mensagem-erro');

function exibirErro(texto) {
    mensagemErro.textContent = texto;
    mensagemErro.hidden = false;
}

function ocultarErro() {
    mensagemErro.hidden = true;
    mensagemErro.textContent = '';
}

formLogin.addEventListener('submit', async (evento) => {
    evento.preventDefault();
    ocultarErro();

    const email = document.getElementById('input-email').value;
    const senha = document.getElementById('input-senha').value;

    try {
        const resposta = await fetch('/api/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, senha }),
        });

        const dados = await resposta.json();

        if (!resposta.ok || !dados.sucesso) {
            exibirErro(dados.erro || 'Falha ao autenticar');
            return;
        }

        window.location.href = '/produtos';
    } catch (erro) {
        exibirErro('Erro de conexao com o servidor');
    }
});
