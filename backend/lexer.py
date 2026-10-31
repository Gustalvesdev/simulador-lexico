OPERATORS = {
    "=": "OPERADOR_ATRIBUICAO",
    "+": "OPERADOR_ARITMETICO",
    "-": "OPERADOR_ARITMETICO",
    "*": "OPERADOR_ARITMETICO",
    "/": "OPERADOR_ARITMETICO",
    "==": "OPERADOR_COMPARACAO",
    "<": "OPERADOR_COMPARACAO",
    ">": "OPERADOR_COMPARACAO",
}

DELIMITERS = {"(", ")", ":", ","}

KEYWORDS = {
    "if",
    "else",
    "while",
    "def",
}

BUILTINS = {"print"}


def _is_identifier_start(character: str) -> bool:
    return character == "_" or "a" <= character <= "z" or "A" <= character <= "Z"


def _is_identifier_part(character: str) -> bool:
    return _is_identifier_start(character) or "0" <= character <= "9"


def tokenize(source: str) -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    tokens: list[dict[str, object]] = []
    errors: list[dict[str, object]] = []
    source = source.replace("\r\n", "\n").replace("\r", "\n")
    index = 0
    line = 1
    column = 1

    def advance() -> str:
        nonlocal index, line, column
        character = source[index]
        index += 1
        if character == "\n":
            line += 1
            column = 1
        else:
            column += 1
        return character

    def add_token(token_type: str, lexeme: str, token_line: int, token_column: int) -> None:
        tokens.append({
            "tipo": token_type,
            "lexema": lexeme,
            "linha": token_line,
            "coluna": token_column,
        })

    def add_error(
        lexeme: str,
        message: str,
        error_line: int,
        error_column: int,
    ) -> None:
        errors.append({
            "tipo": "ERRO_LEXICO",
            "lexema": lexeme,
            "linha": error_line,
            "coluna": error_column,
            "mensagem": message,
        })

    while index < len(source):
        character = source[index]

        if character.isspace():
            advance()
            continue

        if character == "#":
            while index < len(source) and source[index] != "\n":
                advance()
            continue

        token_line = line
        token_column = column

        if _is_identifier_start(character):
            start = index
            while index < len(source) and _is_identifier_part(source[index]):
                advance()
            lexeme = source[start:index]
            if lexeme in KEYWORDS:
                token_type = "PALAVRA_RESERVADA"
            elif lexeme in BUILTINS:
                token_type = "FUNCAO_BUILTIN"
            else:
                token_type = "IDENTIFICADOR"
            add_token(token_type, lexeme, token_line, token_column)
            continue

        if "0" <= character <= "9":
            start = index
            while index < len(source) and "0" <= source[index] <= "9":
                advance()
            add_token("LITERAL_INTEIRO", source[start:index], token_line, token_column)
            continue

        if character == '"':
            start = index
            advance()
            string_closed = False

            while index < len(source):
                current = source[index]

                if current == "\n":
                    break

                if current == '"':
                    advance()
                    string_closed = True
                    break

                if current == "\\":
                    escape_line = line
                    escape_column = column
                    escape_start = index
                    advance()
                    if index < len(source) and source[index] in {'"', "\\"}:
                        advance()
                    else:
                        if index < len(source) and source[index] != "\n":
                            advance()
                        escape = source[escape_start:index]
                        add_error(
                            escape,
                            f"Escape não suportado: {escape!r}. São aceitos apenas \\\\\" e \\\\\\\\.",
                            escape_line,
                            escape_column,
                        )
                    continue

                advance()

            lexeme = source[start:index]
            if string_closed:
                add_token("LITERAL_STRING", lexeme, token_line, token_column)
            else:
                add_error(
                    lexeme,
                    "String sem fechamento antes do fim da linha ou do arquivo.",
                    token_line,
                    token_column,
                )
            continue

        operator = None
        if source.startswith("==", index):
            operator = "=="
        elif character in OPERATORS:
            operator = character

        if operator is not None:
            for _ in operator:
                advance()
            add_token(OPERATORS[operator], operator, token_line, token_column)
            continue

        if character in DELIMITERS:
            advance()
            add_token("DELIMITADOR", character, token_line, token_column)
            continue

        advance()
        add_error(
            character,
            f"Caractere não reconhecido: {character!r}.",
            token_line,
            token_column,
        )

    return tokens, errors
