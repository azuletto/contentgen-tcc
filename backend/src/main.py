from flask import Flask, request, jsonify
from flask_cors import CORS
import threading
import os
import json
from extraction.extractor import fetch_rendered_html  # Função de extração importada
from content.classic_content import criar_flyer_responsivo
from flask import Flask, request, send_file, jsonify

from dotenv import load_dotenv, set_key


env_path = os.path.join(os.getcwd(), "backend/.env")
load_dotenv(env_path)

app = Flask(__name__)
CORS(
    app, resources={r"/*": {"origins": "http://localhost:3000"}}
)  # Permite chamadas do frontend

CHROMEDRIVER_PATH = "chromedriver-win64\chromedriver.exe"
JSON_OUTPUT_DIR = os.path.join("backend", "src", "generator", "output_json")


@app.route("/process", methods=["POST"])
def process():
    data = request.json
    url = data.get("url")
    output_type = data.get("output_type")

    if not url:
        return jsonify({"error": "Parâmetro 'url' inválido"}), 400

    threading.Thread(target=process_data, args=(url, output_type)).start()
    return jsonify({"message": "Processamento iniciado, aguarde a conclusão."}), 200


def process_data(url, output_type):
    print(f"🔹 Extraindo HTML de {url}")
    html_content = fetch_rendered_html(url, CHROMEDRIVER_PATH)

    if html_content:
        output_dir = os.path.join("backend", "src", "extraction", "output")
        os.makedirs(output_dir, exist_ok=True)

        output_file_path = os.path.join(output_dir, "rendered_page.html")
        with open(output_file_path, "w", encoding="utf-8") as file:
            file.write(html_content)
        print("✅ HTML extraído e salvo com sucesso!")

        json_data = {
            "url": url,
            "output_type": output_type,
            "data": "Aqui você adicionaria a estrutura extraída do HTML",
        }

        os.makedirs(JSON_OUTPUT_DIR, exist_ok=True)
        json_file_path = os.path.join(JSON_OUTPUT_DIR, "summary.json")

        with open(json_file_path, "w", encoding="utf-8") as json_file:
            json.dump(json_data, json_file, indent=4)
        print("✅ JSON gerado e salvo como summary.json!")

        notify_frontend()


def notify_frontend():
    print("✅ Processamento concluído!")


@app.route("/get-json", methods=["GET"])
def get_json():
    """
    Retorna o conteúdo do arquivo JSON mais recente gerado.
    """
    json_output_dir = os.path.join(
        os.path.dirname(__file__), "generator", "output_json"
    )
    json_file_path = os.path.join(
        json_output_dir, "summary.json"
    )  # Caminho fixo para o arquivo esperado

    try:
        if os.path.exists(json_file_path):  # Verifica se o arquivo existe
            with open(json_file_path, "r", encoding="utf-8") as json_file:
                json_data = json.load(json_file)
            return jsonify(json_data), 200
        else:
            print(f"❌ Arquivo não encontrado: {json_file_path}")  # Debug no console
            return jsonify({"error": "Arquivo JSON não encontrado"}), 404
    except Exception as e:
        print(f"❌ Erro ao abrir o arquivo: {str(e)}")  # Debug no console
        return jsonify({"error": f"Erro ao acessar o JSON: {str(e)}"}), 500


@app.route("/get-api-key", methods=["GET"])
def get_api_key():
    api_key = os.getenv("API_KEY", "Chave não definida")  # Busca a chave no .env
    return jsonify({"api_key": api_key})  # Retorna a chave para o frontend


@app.route("/set-api-key", methods=["POST"])
def set_api_key():
    data = request.json
    api_key = data.get("api_key")

    if not api_key:
        return jsonify({"error": "API Key não fornecida"}), 400

    # Salvar a API Key no arquivo .env
    set_key(env_path, "API_KEY", api_key)

    return jsonify({"message": "API Key salva com sucesso!"})


@app.route("/gerar-pdf", methods=["POST"])
def gerar_pdf():
    try:
        # Obter JSON da requisição
        dados = request.json.get("dados")
        if not dados:
            return jsonify({"error": "Nenhum dado recebido para gerar o PDF!"}), 400

        # Caminho onde o PDF será salvo
        caminho_pdf = "output_file/classic_layout_flyer.pdf"

        # Chama a função para gerar o PDF
        criar_flyer_responsivo(dados_json=dados, nome_arquivo=caminho_pdf)

        # Responde com sucesso
        return (
            jsonify({"message": "PDF gerado com sucesso!", "caminho_pdf": caminho_pdf}),
            200,
        )

    except Exception as e:
        print(f"🚨 Erro ao gerar PDF: {str(e)}")
        return jsonify({"error": "Erro ao gerar o PDF!", "details": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
