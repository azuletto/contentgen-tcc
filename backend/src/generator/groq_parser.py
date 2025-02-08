import os
import json
import re
from dotenv import load_dotenv
from groq import Groq

# Carregar variáveis de ambiente a partir do arquivo .env
load_dotenv()

# Caminhos dos arquivos
html_file_path = os.path.join(os.getcwd(), "backend", "src", "extraction", "output", "rendered_page.html")
output_json_path = os.path.join(os.getcwd(), "backend", "src", "generator", "output_json", "summary.json")

# Garantir que a pasta de saída existe
os.makedirs(os.path.dirname(output_json_path), exist_ok=True)

def process_html_with_ai():
    """
    Lê o HTML extraído, envia para a IA e salva o JSON gerado.
    """
    try:
        # Lê o conteúdo do arquivo HTML
        with open(html_file_path, "r", encoding="utf-8") as file:
            html_content = file.read()
    except FileNotFoundError:
        print(f"❌ Erro: O arquivo HTML não foi encontrado em {html_file_path}.")
        return
    except Exception as e:
        print(f"❌ Erro inesperado ao ler o arquivo HTML: {e}")
        return

    # Criar cliente da API Groq
    try:
        api_key = os.getenv("API_KEY")
        if not api_key:
            print("❌ Erro: A chave de API não foi encontrada no arquivo .env.")
            return
        
        client = Groq(api_key=api_key)
    except Exception as e:
        print(f"❌ Erro ao configurar o cliente da API: {e}")
        return

    # Prompt para a IA
    INPUT_CONTENT = "patente"
    TYPE_OUTPUT = "flyer"

    prompt = (
    f"Resuma esse HTML:\n{html_content}\n"
    f"Isto é uma(um) {INPUT_CONTENT}. "
    f", mais um resumo principal. "
    f"Esse resumo deve ser adequado para um {TYPE_OUTPUT} comercial, então seja atrativo e detalhado. "
    f"Retorne um JSON bem formatado e **APENAS o JSON puro**, sem explicações adicionais e sem markdown.\n"
    f"Os campos que devem ser extraídos SEMPRE do texto são:\n"
    f"- nome_do_produto\n"
    f"- tipo_do_produto\n"
    f"- descricao_do_produto\n"
    f"- vantagens_do_produto\n"
    f"- numero_da_patente [caso haja]\n"
    f"- supervisores_contato\n"
    f"- tags_relacionadas_ao_produto"
)

    # Chamada à API
    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-specdec",
            messages=[{"role": "user", "content": prompt}],
            temperature=1,
            max_completion_tokens=1024,
            top_p=1,
            stream=False,
            stop=None,
        )

        # Capturar a resposta gerada pela IA
        response_text = completion.choices[0].message.content.strip()

    except Exception as e:
        print(f"❌ Erro ao chamar a API: {e}")
        return

    # Limpar formatação extra do JSON
    response_text = re.sub(r"```json\s*", "", response_text)  # Remove ```json do início
    response_text = re.sub(r"```$", "", response_text)  # Remove ``` do final
    response_text = response_text.strip()  # Remove espaços extras

    # Verificar se a resposta é um JSON válido antes de salvar
    try:
        summary_data = json.loads(response_text)  # Converte a string para JSON
        with open(output_json_path, "w", encoding="utf-8") as json_file:
            json.dump(summary_data, json_file, indent=4, ensure_ascii=False)
        print(f"✅ Resumo salvo com sucesso em: {output_json_path}")
    except json.JSONDecodeError:
        print("❌ Erro: A resposta da IA não está em formato JSON válido.")
        print("🔍 Resposta recebida:")
        print(response_text)

if __name__ == "__main__":
    process_html_with_ai()
