from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app) # Permite que o frontend se comunique com o backend

@app.route('/api/hello', methods=['GET'])
def hello():
    # Esta mensagem será enviada ao frontend para provar a comunicação
    return jsonify({"message": "Hello, World! O Backend em Python está rodando e conectado!"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)