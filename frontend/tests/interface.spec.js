const { test, expect } = require('@playwright/test');

test.beforeEach(async ({ page }) => {
    await page.goto('/');
});

test('exibe a interface e permite carregar, substituir e editar exemplos', async ({ page }) => {
    const editor = page.getByLabel('Edite o código antes de enviar');
    const seletor = page.getByLabel('Carregar exemplo');

    await expect(page.getByRole('heading', { name: 'Simulador Léxico — Python' })).toBeVisible();
    await expect(seletor.locator('option')).toHaveCount(4);

    await seletor.selectOption('variavel');
    await expect(editor).toHaveValue('numero = 10\nprint(numero)');

    await seletor.selectOption('aritmetica');
    await expect(editor).toHaveValue('resultado = 10 + 5\nprint(resultado)');

    await seletor.selectOption('condicional');
    await expect(editor).toHaveValue('numero = 3\nif numero > 0:\n    print("positivo")');

    await editor.fill('numero = 20');
    await expect(editor).toHaveValue('numero = 20');
});

test('valida conteúdo vazio ou composto apenas por espaços sem chamar a API', async ({ page }) => {
    let chamadas = 0;
    await page.route('**/api/analisar', async (route) => {
        chamadas += 1;
        await route.continue();
    });

    const editor = page.getByLabel('Edite o código antes de enviar');
    const resultado = page.locator('#resultado');

    for (const codigo of ['', ' \n\t ']) {
        await editor.fill(codigo);
        await page.getByRole('button', { name: 'Solicitar processamento' }).click();
        await expect(resultado).toContainText('Informe um código-fonte');
    }

    expect(chamadas).toBe(0);
});

test('envia o texto editado e exibe a confirmação real do backend', async ({ page }) => {
    const editor = page.getByLabel('Edite o código antes de enviar');
    await page.getByLabel('Carregar exemplo').selectOption('variavel');
    await editor.fill('valor = 42');

    const responsePromise = page.waitForResponse((response) =>
        response.url().endsWith('/api/analisar') && response.request().method() === 'POST',
    );
    await page.getByRole('button', { name: 'Solicitar processamento' }).click();

    const response = await responsePromise;
    expect(response.status()).toBe(200);
    await expect(page.locator('#resultado')).toHaveText('Código recebido com sucesso.');
});

test('apresenta mensagem de validação devolvida pela API', async ({ page }) => {
    await page.route('**/api/analisar', (route) => route.fulfill({
        status: 400,
        contentType: 'application/json',
        body: JSON.stringify({ mensagem: 'O campo codigo é obrigatório.' }),
    }));
    await page.getByLabel('Edite o código antes de enviar').fill('entrada');
    await page.getByRole('button', { name: 'Solicitar processamento' }).click();

    await expect(page.locator('#resultado')).toHaveText('O campo codigo é obrigatório.');
});

test('trata falha de comunicação sem expor detalhes técnicos', async ({ page }) => {
    await page.route('**/api/analisar', (route) => route.abort());
    await page.getByLabel('Edite o código antes de enviar').fill('entrada');
    await page.getByRole('button', { name: 'Solicitar processamento' }).click();

    await expect(page.locator('#resultado')).toHaveText(
        'Não foi possível se comunicar com o servidor. Verifique a conexão e tente novamente.',
    );
    await expect(page.getByRole('button', { name: 'Solicitar processamento' })).toBeEnabled();
});

test('apresenta erro genérico para falha inesperada do servidor', async ({ page }) => {
    await page.route('**/api/analisar', (route) => route.fulfill({
        status: 500,
        contentType: 'application/json',
        body: JSON.stringify({ mensagem: 'Ocorreu um erro inesperado no servidor.' }),
    }));
    await page.getByLabel('Edite o código antes de enviar').fill('entrada');
    await page.getByRole('button', { name: 'Solicitar processamento' }).click();

    await expect(page.locator('#resultado')).toHaveText('Ocorreu um erro inesperado no servidor.');
    await expect(page.locator('#resultado')).not.toContainText('Traceback');
});
