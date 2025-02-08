import os
import json
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.units import cm

def criar_flyer_responsivo(dados_json=None, nome_arquivo="classic_layout_flyer.pdf", caminho_json="backend/src/generator/output_json/summary.json"):
    """
    Gera um PDF baseado nos dados fornecidos.
    - Pode receber um JSON diretamente (via API).
    - Se nenhum JSON for passado, carrega os dados do arquivo local.

    :param dados_json: Dicionário com os dados para o flyer (opcional).
    :param nome_arquivo: Nome do arquivo PDF a ser gerado.
    :param caminho_json: Caminho opcional para um arquivo JSON local.
    :return: Caminho do arquivo PDF gerado ou None se falhar.
    """

    # 1️⃣ Se os dados não forem passados, tentar carregar do arquivo JSON
    if dados_json is None:
        if os.path.exists(caminho_json):
            with open(caminho_json, "r", encoding="utf-8") as arquivo:
                dados_json = json.load(arquivo)
        else:
            print(f"🚨 Erro: Nenhum dado foi passado e o arquivo JSON não existe: {caminho_json}")
            return None

    # 2️⃣ Verificar se os dados JSON recebidos estão no formato correto
    if not isinstance(dados_json, dict):
        print("🚨 Erro: JSON inválido ou vazio!")
        return None

    # 3️⃣ Se os dados estiverem aninhados dentro de uma chave "dados", desaninhá-los
    if "dados" in dados_json and isinstance(dados_json["dados"], dict):
        dados_json = dados_json["dados"]  # Agora contém apenas os dados necessários

    # 📌 Exibir os dados carregados para depuração
    print("📌 JSON processado para gerar o PDF:", json.dumps(dados_json, indent=4, ensure_ascii=False))

    # Configurações de estilo do PDF
    estilos = getSampleStyleSheet()
    estilo_titulo = estilos["Heading1"]
    estilo_titulo.textColor = colors.HexColor("#3b82f6")  # Azul vibrante
    estilo_titulo.alignment = 1  # Centralizado

    estilo_subtitulo = estilos["Heading2"]
    estilo_subtitulo.textColor = colors.white
    estilo_subtitulo.backColor = colors.HexColor("#374151")  # Fundo cinza
    estilo_subtitulo.alignment = 0  # Alinhado à esquerda

    estilo_texto = ParagraphStyle(
        "TextoNormal",
        parent=estilos["Normal"],
        fontName="Helvetica",
        fontSize=10,
        textColor=colors.white,
        leading=14,
        spaceAfter=6,
    )

    estilo_rodape = ParagraphStyle(
        "Rodape",
        parent=estilos["Normal"],
        fontName="Helvetica",
        fontSize=9,
        textColor=colors.white,
        leading=12,
    )

    # Criar o documento PDF
    doc = SimpleDocTemplate(
        nome_arquivo,
        pagesize=A4,
        rightMargin=2 * cm,
        leftMargin=2 * cm,
        topMargin=2 * cm,
        bottomMargin=3 * cm,
    )

    elementos = []

    # Verificar e adicionar Nome do Produto
    nome_produto = dados_json.get("nome_do_produto", "").strip()
    if nome_produto:
        elementos.append(Paragraph(nome_produto, estilo_titulo))
        elementos.append(Spacer(1, 0.5 * cm))
    else:
        print("⚠️ Aviso: Nome do produto ausente!")

    # Verificar e adicionar Tipo do Produto
    tipo_produto = dados_json.get("tipo_do_produto", "").strip()
    if tipo_produto:
        elementos.append(Paragraph(f"Tipo do Produto: {tipo_produto}", estilo_subtitulo))
        elementos.append(Spacer(1, 0.5 * cm))

    # Verificar e adicionar Descrição
    descricao = dados_json.get("descricao_do_produto", "").strip()
    if descricao:
        elementos.append(Paragraph(f"<b>Descrição:</b> {descricao}", estilo_texto))
        elementos.append(Spacer(1, 0.5 * cm))

    # Verificar e adicionar Vantagens do Produto
    vantagens = dados_json.get("vantagens_do_produto", [])
    if isinstance(vantagens, list) and vantagens:
        elementos.append(Paragraph("<b>Vantagens do Produto:</b>", estilo_subtitulo))
        for vantagem in vantagens:
            elementos.append(Paragraph(f"- {vantagem}", estilo_texto))
        elementos.append(Spacer(1, 0.5 * cm))

    # Verificar e adicionar Número da Patente
    numero_patente = dados_json.get("numero_da_patente", "").strip()
    if numero_patente:
        elementos.append(Paragraph(f"<b>Número da Patente:</b> {numero_patente}", estilo_texto))
        elementos.append(Spacer(1, 0.5 * cm))

    # Verificar e adicionar Supervisores e Contato
    supervisores = dados_json.get("supervisores_contato", {})
    rodape_content = []
    if isinstance(supervisores, dict):
        rodape_content.append("<b>Contato dos Supervisores:</b>")
        if "email" in supervisores:
            rodape_content.append(f"Email: {supervisores['email']}")
        if "telefone" in supervisores:
            rodape_content.append(f"Telefone: {supervisores['telefone']}")

    # Verificar e adicionar Tags Relacionadas
    tags = dados_json.get("tags_relacionadas_ao_produto", [])
    if isinstance(tags, list) and tags:
        rodape_content.append(f"<b>Tags Relacionadas:</b> {', '.join(tags[:5])}")  # Limita a 5 tags

    if rodape_content:
        elementos.append(Spacer(1, 1 * cm))
        elementos.append(Paragraph("<br/>".join(rodape_content), estilo_rodape))

    # Se não houver elementos, retorna erro
    if not elementos:
        print("🚨 Erro: Nenhum conteúdo válido para adicionar ao PDF!")
        return None

    # Adicionar plano de fundo e renderizar
    def fundo(canvas, doc):
        canvas.saveState()
        canvas.setFillColor(colors.HexColor("#1e293b"))  # Fundo azul-escuro
        canvas.rect(0, 0, A4[0], A4[1], fill=True, stroke=False)
        canvas.restoreState()

    doc.build(
        elementos,
        onFirstPage=fundo,
        onLaterPages=fundo,
    )

    print(f"✅ Flyer gerado com sucesso: {nome_arquivo}")
    return nome_arquivo
