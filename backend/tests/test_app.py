import unittest

from werkzeug.exceptions import InternalServerError

from backend.app import app, erro_interno


class ApiTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_hello_route_remains_available(self):
        response = self.client.get("/api/hello")

        self.assertEqual(response.status_code, 200)
        self.assertIn("Hello, World!", response.get_json()["message"])

    def test_valid_code_is_acknowledged_without_analysis(self):
        response = self.client.post("/api/analisar", json={"codigo": "numero = 10"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.get_json(),
            {"mensagem": "Código recebido com sucesso.", "recebido": True},
        )

    def test_empty_code_is_rejected(self):
        for codigo in ("", " \t\n"):
            with self.subTest(codigo=codigo):
                response = self.client.post("/api/analisar", json={"codigo": codigo})

                self.assertEqual(response.status_code, 400)
                self.assertIn("Informe um código-fonte", response.get_json()["mensagem"])

    def test_missing_or_non_text_code_is_rejected(self):
        for body in ({}, {"codigo": 10}, {"codigo": None}):
            with self.subTest(body=body):
                response = self.client.post("/api/analisar", json=body)

                self.assertEqual(response.status_code, 400)
                self.assertIn("codigo", response.get_json()["mensagem"])

    def test_non_json_and_invalid_json_are_rejected(self):
        non_json = self.client.post("/api/analisar", data="codigo=numero")
        invalid_json = self.client.post(
            "/api/analisar",
            data="{",
            content_type="application/json",
        )

        self.assertEqual(non_json.status_code, 415)
        self.assertEqual(invalid_json.status_code, 400)
        self.assertIn("JSON", invalid_json.get_json()["mensagem"])

    def test_json_with_non_object_body_is_rejected(self):
        response = self.client.post("/api/analisar", json=["numero = 10"])

        self.assertEqual(response.status_code, 400)
        self.assertIn("JSON", response.get_json()["mensagem"])

    def test_internal_error_message_does_not_expose_details(self):
        with app.test_request_context():
            response, status = erro_interno(InternalServerError("internal detail"))

        self.assertEqual(status, 500)
        self.assertEqual(
            response.get_json(),
            {"mensagem": "Ocorreu um erro inesperado no servidor."},
        )


if __name__ == "__main__":
    unittest.main()
