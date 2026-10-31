# Registro de testes — Etapa 3

## Scanner e API

- **Tipo:** testes unitários e de endpoint (`unittest`).
- **Comando executado:** `.\.venv\Scripts\python.exe -m unittest discover -s backend\tests -v`
- **Resultado:** 18 testes aprovados.
- **Cobertura relevante:** categorias, identificadores, operadores (incluindo `==`), delimitadores, inteiros, strings e escapes definidos, comentários, espaços e posições, erros lexicais com recuperação, entradas de borda, contrato HTTP e regressão de `/api/hello`.

## Interface e integração

- **Tipo:** testes de navegador com Playwright contra os serviços Docker.
- **Comando executado:** `npm test --prefix frontend`
- **Resultado final:** 9 testes aprovados.
- **Cobertura relevante:** exemplos e edição, validação de entrada, envio ao backend, tabela/contagem de tokens, erros lexicais, resposta malformada, falha de comunicação e resposta inesperada do servidor.

## Docker Compose e verificações adicionais

- **Comando:** `docker compose up --build -d --wait`
- **Resultado:** imagens construídas; backend iniciou saudável e frontend ficou acessível em `http://localhost:8080`.
- **Verificações:** `GET /api/hello`, análise com tokens e requisição com caractere inválido verificados pela rota publicada via Nginx; `docker compose config --quiet`, `python -m py_compile`, `node --check` e `git diff --check` concluídos sem erros.

## Ocorrências durante a validação

- O Docker Desktop estava parado na primeira tentativa. O serviço foi iniciado e o build completo foi repetido com sucesso.
- Uma execução inicial dos testes E2E ocorreu simultaneamente à reconstrução do frontend e atingiu o contêiner anterior; dois testes falharam nessa corrida. Após a reconstrução terminar, todos os 9 testes foram executados novamente contra os serviços atualizados e passaram.
- Não houve falhas pendentes na validação final.

## Limitações não cobertas

Não foram testadas análise sintática/semântica, execução do código, indentação como `INDENT`/`DEDENT`, floats, strings de aspas simples, escapes fora do recorte, identificadores Unicode ou integração com parser. Esses recursos estão fora do escopo atual.
