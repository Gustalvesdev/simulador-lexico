import unittest

from backend.lexer import tokenize


class TokenizeTestCase(unittest.TestCase):
    def test_keywords_builtin_and_identifiers(self):
        tokens, errors = tokenize("if else while def print _x nome2 A_1")

        self.assertEqual(errors, [])
        self.assertEqual(
            [(token["tipo"], token["lexema"]) for token in tokens],
            [
                ("PALAVRA_RESERVADA", "if"),
                ("PALAVRA_RESERVADA", "else"),
                ("PALAVRA_RESERVADA", "while"),
                ("PALAVRA_RESERVADA", "def"),
                ("FUNCAO_BUILTIN", "print"),
                ("IDENTIFICADOR", "_x"),
                ("IDENTIFICADOR", "nome2"),
                ("IDENTIFICADOR", "A_1"),
            ],
        )

    def test_operators_are_matched_with_longest_lexeme_first(self):
        tokens, errors = tokenize("= + - * / == < >")

        self.assertEqual(errors, [])
        self.assertEqual(
            [(token["tipo"], token["lexema"]) for token in tokens],
            [
                ("OPERADOR_ATRIBUICAO", "="),
                ("OPERADOR_ARITMETICO", "+"),
                ("OPERADOR_ARITMETICO", "-"),
                ("OPERADOR_ARITMETICO", "*"),
                ("OPERADOR_ARITMETICO", "/"),
                ("OPERADOR_COMPARACAO", "=="),
                ("OPERADOR_COMPARACAO", "<"),
                ("OPERADOR_COMPARACAO", ">"),
            ],
        )

    def test_delimiters_integers_and_escaped_strings(self):
        tokens, errors = tokenize('funcao(10, "a\\"b\\\\c"):')

        self.assertEqual(errors, [])
        self.assertEqual(
            [(token["tipo"], token["lexema"]) for token in tokens],
            [
                ("IDENTIFICADOR", "funcao"),
                ("DELIMITADOR", "("),
                ("LITERAL_INTEIRO", "10"),
                ("DELIMITADOR", ","),
                ("LITERAL_STRING", '"a\\"b\\\\c"'),
                ("DELIMITADOR", ")"),
                ("DELIMITADOR", ":"),
            ],
        )

    def test_comments_are_ignored_and_positions_are_one_based(self):
        tokens, errors = tokenize("x = 1 # comentário\r\n    print(x)")

        self.assertEqual(errors, [])
        self.assertEqual(
            [(token["lexema"], token["linha"], token["coluna"]) for token in tokens],
            [
                ("x", 1, 1),
                ("=", 1, 3),
                ("1", 1, 5),
                ("print", 2, 5),
                ("(", 2, 10),
                ("x", 2, 11),
                (")", 2, 12),
            ],
        )
        tab_tokens, tab_errors = tokenize("\tprint")
        self.assertEqual(tab_errors, [])
        self.assertEqual((tab_tokens[0]["linha"], tab_tokens[0]["coluna"]), (1, 2))

    def test_unknown_characters_report_positions_and_scanning_continues(self):
        tokens, errors = tokenize("x @ y $\nprint(x)")

        self.assertEqual(
            [(token["lexema"], token["linha"], token["coluna"]) for token in tokens],
            [
                ("x", 1, 1),
                ("y", 1, 5),
                ("print", 2, 1),
                ("(", 2, 6),
                ("x", 2, 7),
                (")", 2, 8),
            ],
        )
        self.assertEqual(
            [(error["lexema"], error["linha"], error["coluna"]) for error in errors],
            [("@", 1, 3), ("$", 1, 7)],
        )

    def test_unclosed_string_reports_error_and_scans_following_line(self):
        tokens, errors = tokenize('"sem fechamento\nvalor = 3')

        self.assertEqual(
            [(token["lexema"], token["linha"], token["coluna"]) for token in tokens],
            [("valor", 2, 1), ("=", 2, 7), ("3", 2, 9)],
        )
        self.assertEqual(len(errors), 1)
        self.assertEqual(errors[0]["lexema"], '"sem fechamento')
        self.assertEqual((errors[0]["linha"], errors[0]["coluna"]), (1, 1))

    def test_unsupported_escape_is_reported_but_string_is_kept(self):
        tokens, errors = tokenize('"linha\\nseguinte"')

        self.assertEqual([token["tipo"] for token in tokens], ["LITERAL_STRING"])
        self.assertEqual(len(errors), 1)
        self.assertEqual(errors[0]["lexema"], "\\n")
        self.assertEqual((errors[0]["linha"], errors[0]["coluna"]), (1, 7))
        self.assertIn("Escape não suportado", errors[0]["mensagem"])

    def test_unicode_identifier_character_is_reported_as_out_of_scope(self):
        tokens, errors = tokenize("café = 1")

        self.assertEqual([token["lexema"] for token in tokens], ["caf", "=", "1"])
        self.assertEqual(
            [(error["lexema"], error["linha"], error["coluna"]) for error in errors],
            [("é", 1, 4)],
        )

    def test_syntactic_structure_is_not_validated(self):
        tokens, errors = tokenize("valor = if +")

        self.assertEqual(errors, [])
        self.assertEqual(
            [token["tipo"] for token in tokens],
            [
                "IDENTIFICADOR",
                "OPERADOR_ATRIBUICAO",
                "PALAVRA_RESERVADA",
                "OPERADOR_ARITMETICO",
            ],
        )

    def test_empty_whitespace_comment_and_eof_without_newline(self):
        self.assertEqual(tokenize(""), ([], []))
        self.assertEqual(tokenize(" \t\n"), ([], []))
        self.assertEqual(tokenize("# somente comentário"), ([], []))

        tokens, errors = tokenize("final=42")
        self.assertEqual(errors, [])
        self.assertEqual([token["lexema"] for token in tokens], ["final", "=", "42"])


if __name__ == "__main__":
    unittest.main()
