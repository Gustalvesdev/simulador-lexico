from flask import Flask, jsonify, request
from flask_cors import CORS
from werkzeug.exceptions import InternalServerError

app = Flask(__name__)
CORS(app) # Permite que o frontend se comunique com o backend


@app.route('/api/hello', methods=['GET'])
def hello():
    return jsonify({"message": "Hello, World! O Backend em Python está rodando e conectado!"})


@app.route('/api/analisar', methods=['POST'])
def analisar():
    if not request.is_json:
        return jsonify({"mensagem": "Envie os dados no formato JSON."}), 415

    dados = request.get_json(silent=True)
    if not isinstance(dados, dict):
        return jsonify({"mensagem": "O corpo da requisição JSON é inválido."}), 400

    codigo = dados.get("codigo")
    if not isinstance(codigo, str):
        return jsonify({"mensagem": "O campo 'codigo' é obrigatório e deve ser texto."}), 400
    if not codigo.strip():
        return jsonify({"mensagem": "Informe um código-fonte antes de solicitar o processamento."}), 400

    return jsonify({
        "mensagem": "Código recebido com sucesso.",
        "recebido": True,
    })


@app.errorhandler(InternalServerError)
def erro_interno(_error):
    return jsonify({"mensagem": "Ocorreu um erro inesperado no servidor."}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
