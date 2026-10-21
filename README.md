# Simulador Léxico - Python

Este repositório contém a infraestrutura e o código fonte de um software educacional interativo focado no ensino da fase de **Análise Léxica** de compiladores.

## 1. Escopo e Fronteira Tecnológica

* **Linguagem Foco:** Python.
* **Justificativa:** A linguagem Python foi escolhida por possuir uma sintaxe limpa, popularidade acadêmica e proximidade com a linguagem natural. Isso permite focar puramente no conceito de geração de tokens, reduzindo a carga cognitiva do aluno com estruturas verbosas de outras linguagens.
* **Subconjunto Inicial da Linguagem:** Para manter o projeto viável e focado na didática, o analisador léxico cobrirá inicialmente o seguinte subconjunto de Python:
  * **Identificadores:** Nomes de variáveis.
  * **Palavras Reservadas:** `if`, `else`, `while`, `print`, `def`.
  * **Operadores:** Atribuição (`=`), Matemáticos básicos (`+`, `-`, `*`, `/`) e Relacionais (`==`, `<`, `>`).
  * **Delimitadores:** Parênteses `()`, dois-pontos `:` e vírgula `,`.
  * **Literais:** Números inteiros e Strings simples (aspas duplas).

## 2. Estrutura do Projeto

* `frontend/`: Interface de usuário servida via Nginx (HTML/JS puro).
* `backend/`: API em Python utilizando Flask para o processamento léxico.
* `docker-compose.yml`: Arquivo de orquestração dos contêineres.

## 3. Pré-requisitos

Para executar este projeto em qualquer máquina (instalação limpa), você precisará apenas de:
* [Docker](https://docs.docker.com/get-docker/) instalado.
* [Docker Compose](https://docs.docker.com/compose/install/) instalado.

## 4. Como Executar (Inicialização)

1. Clone este repositório para sua máquina local.
2. Abra o terminal na pasta raiz do projeto (onde está o arquivo `docker-compose.yml`).
3. Execute o comando para construir e iniciar os contêineres em segundo plano:
   ```bash
   docker-compose up --build -d