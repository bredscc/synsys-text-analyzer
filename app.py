from flask_cors import CORS
from flask import Flask, request, jsonify
from analise import analisar_texto

app = Flask(__name__)

# Configuração de CORS (Cross-Origin Resource Sharing)
# Isto é CRUCIAL para que meu site (brecketline.me) possa se comunicar com esta API.
CORS(app)


@app.route('/analisar', methods=['POST'])
def api_analisar():
    """
    Endpoint principal da API. Recebe um texto via POST e retorna a análise de PLN.
    """
    data = request.get_json()

    if not data or 'texto' not in data:
        return jsonify({"erro": "Requisição inválida. O campo 'texto' é obrigatório."}), 400

    texto_entrada = data.get('texto', '')

    try:
        resultados = analisar_texto(texto_entrada)

        return jsonify({
            "status": "sucesso",
            "resultados": resultados,
            "total_palavras_repetidas": len(resultados)
        }), 200

    except Exception as e:

        return jsonify({"erro": f"Erro interno durante a análise: {str(e)}"}), 500


if __name__ == '__main__':
    print("--- 🌐 Iniciando Servidor SYNSYS API em http://127.0.0.1:5000/ ---")
    app.run(debug=True)
