const exemplos = {
    variavel: 'numero = 10\nprint(numero)',
    aritmetica: 'resultado = 10 + 5\nprint(resultado)',
    condicional: 'numero = 3\nif numero > 0:\n    print("positivo")',
};

const formulario = document.querySelector('#formulario');
const editor = document.querySelector('#codigo');
const seletor = document.querySelector('#exemplo');
const botaoEnviar = document.querySelector('#enviar');
const resultado = document.querySelector('#resultado');

seletor.addEventListener('change', () => {
    if (exemplos[seletor.value]) {
        editor.value = exemplos[seletor.value];
        resultado.textContent = 'Exemplo carregado. Você pode editá-lo antes de enviar.';
        resultado.dataset.state = 'idle';
    }
});

formulario.addEventListener('submit', async (evento) => {
    evento.preventDefault();
    resultado.textContent = '';
    resultado.dataset.state = 'idle';

    if (!editor.value.trim()) {
        resultado.textContent = 'Informe um código-fonte antes de solicitar o processamento.';
        resultado.dataset.state = 'error';
        editor.focus();
        return;
    }

    botaoEnviar.disabled = true;
    resultado.textContent = 'Enviando código...';
    resultado.dataset.state = 'pending';

    try {
        const resposta = await fetch('/api/analisar', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ codigo: editor.value }),
        });
        const dados = await resposta.json();

        if (!resposta.ok) {
            resultado.textContent = dados.mensagem || 'Não foi possível processar a solicitação.';
            resultado.dataset.state = 'error';
            return;
        }

        if (dados.recebido !== true || typeof dados.mensagem !== 'string') {
            throw new Error('Resposta inesperada do servidor.');
        }

        resultado.textContent = dados.mensagem;
        resultado.dataset.state = 'success';
    } catch {
        resultado.textContent = 'Não foi possível se comunicar com o servidor. Verifique a conexão e tente novamente.';
        resultado.dataset.state = 'error';
    } finally {
        botaoEnviar.disabled = false;
    }
});
