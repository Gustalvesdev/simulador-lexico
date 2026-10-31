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
const tokensSection = document.querySelector('#tokens-section');
const tokenCounts = document.querySelector('#token-counts');
const tokensBody = document.querySelector('#tokens-body');
const errorsSection = document.querySelector('#errors-section');
const errorsList = document.querySelector('#errors-list');

seletor.addEventListener('change', () => {
    if (exemplos[seletor.value]) {
        editor.value = exemplos[seletor.value];
        clearAnalysis();
        resultado.textContent = 'Exemplo carregado. Você pode editá-lo antes de analisar.';
        resultado.dataset.state = 'idle';
    }
});

function clearAnalysis() {
    tokensSection.hidden = true;
    errorsSection.hidden = true;
    tokenCounts.replaceChildren();
    tokensBody.replaceChildren();
    errorsList.replaceChildren();
}

editor.addEventListener('input', () => {
    if (!tokensSection.hidden || !errorsSection.hidden) {
        clearAnalysis();
        resultado.textContent = 'Código alterado. Solicite a análise novamente.';
        resultado.dataset.state = 'idle';
    }
});

function isValidToken(token) {
    return token !== null
        && typeof token === 'object'
        && typeof token.tipo === 'string'
        && typeof token.lexema === 'string'
        && Number.isInteger(token.linha)
        && Number.isInteger(token.coluna);
}

function isValidError(error) {
    return isValidToken(error) && typeof error.mensagem === 'string';
}

function addTableCell(row, value) {
    const cell = document.createElement('td');
    cell.textContent = String(value);
    row.append(cell);
}

function renderTokens(tokens) {
    const counts = new Map();
    tokens.forEach((token) => counts.set(token.tipo, (counts.get(token.tipo) || 0) + 1));

    counts.forEach((count, type) => {
        const item = document.createElement('li');
        item.textContent = `${type}: ${count}`;
        tokenCounts.append(item);
    });

    if (tokens.length === 0) {
        const row = document.createElement('tr');
        const cell = document.createElement('td');
        cell.colSpan = 4;
        cell.textContent = 'Nenhum token encontrado.';
        row.append(cell);
        tokensBody.append(row);
    } else {
        tokens.forEach((token) => {
            const row = document.createElement('tr');
            addTableCell(row, token.tipo);
            addTableCell(row, token.lexema);
            addTableCell(row, token.linha);
            addTableCell(row, token.coluna);
            tokensBody.append(row);
        });
    }

    tokensSection.hidden = false;
}

function renderErrors(errors) {
    errors.forEach((error) => {
        const item = document.createElement('li');
        item.textContent = `Linha ${error.linha}, coluna ${error.coluna}: ${error.mensagem}`;
        errorsList.append(item);
    });
    errorsSection.hidden = errors.length === 0;
}

formulario.addEventListener('submit', async (evento) => {
    evento.preventDefault();
    clearAnalysis();

    if (!editor.value.trim()) {
        resultado.textContent = 'Informe um código-fonte antes de solicitar a análise.';
        resultado.dataset.state = 'error';
        editor.focus();
        return;
    }

    botaoEnviar.disabled = true;
    resultado.textContent = 'Analisando código...';
    resultado.dataset.state = 'pending';

    try {
        let resposta;
        try {
            resposta = await fetch('/api/analisar', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ codigo: editor.value }),
            });
        } catch {
            resultado.textContent = 'Não foi possível se comunicar com o servidor. Verifique a conexão e tente novamente.';
            resultado.dataset.state = 'error';
            return;
        }

        let dados;
        try {
            dados = await resposta.json();
        } catch {
            resultado.textContent = 'O servidor retornou uma resposta inválida. Tente novamente.';
            resultado.dataset.state = 'error';
            return;
        }

        if (!resposta.ok) {
            resultado.textContent = dados !== null
                && typeof dados === 'object'
                && typeof dados.mensagem === 'string'
                ? dados.mensagem
                : 'Não foi possível processar a solicitação.';
            resultado.dataset.state = 'error';
            return;
        }

        if (
            dados === null
            || typeof dados !== 'object'
            || typeof dados.sucesso !== 'boolean'
            || !Array.isArray(dados.tokens)
            || !dados.tokens.every(isValidToken)
            || !Array.isArray(dados.erros)
            || !dados.erros.every(isValidError)
            || dados.sucesso !== (dados.erros.length === 0)
        ) {
            resultado.textContent = 'O servidor retornou dados de análise em formato inválido.';
            resultado.dataset.state = 'error';
            return;
        }

        renderTokens(dados.tokens);
        renderErrors(dados.erros);

        if (dados.erros.length > 0) {
            resultado.textContent = `Análise concluída com ${dados.tokens.length} token(s) e ${dados.erros.length} erro(s) léxico(s).`;
            resultado.dataset.state = 'error';
        } else {
            resultado.textContent = dados.tokens.length > 0
                ? `Análise concluída sem erros léxicos: ${dados.tokens.length} token(s) identificado(s).`
                : 'Análise concluída sem erros léxicos. Nenhum token foi encontrado.';
            resultado.dataset.state = 'success';
        }
    } finally {
        botaoEnviar.disabled = false;
    }
});
