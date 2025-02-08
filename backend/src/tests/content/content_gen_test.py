import os
import json
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Frame, Image, PageTemplate
from reportlab.lib.units import cm

def criar_flyer_responsivo(caminho_json, nome_arquivo="flyer_responsivo.pdf"):
    if not os.path.exists(caminho_json):
        print(f"Arquivo JSON não encontrado: {caminho_json}")
        return

    # Carregar o JSON
    with open(caminho_json, "r", encoding="utf-8") as arquivo:
        dados = json.load(arquivo)

    # Configurações de estilo
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
        leading=14,  # Espaçamento entre linhas
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

    # Criar o documento
    doc = SimpleDocTemplate(
        nome_arquivo,
        pagesize=A4,
        rightMargin=2 * cm,
        leftMargin=2 * cm,
        topMargin=2 * cm,
        bottomMargin=3 * cm,
    )

    elementos = []

    # Nome do Produto
    if "nome_do_produto" in dados:
        elementos.append(Paragraph(dados["nome_do_produto"], estilo_titulo))
        elementos.append(Spacer(1, 0.5 * cm))

    # Tipo do Produto
    if "tipo_do_produto" in dados:
        elementos.append(Paragraph(f"Tipo do Produto: {dados['tipo_do_produto']}", estilo_subtitulo))
        elementos.append(Spacer(1, 0.5 * cm))

    # Descrição
    if "descricao_do_produto" in dados:
        elementos.append(Paragraph(f"<b>Descrição:</b> {dados['descricao_do_produto']}", estilo_texto))
        elementos.append(Spacer(1, 0.5 * cm))

    # Vantagens do Produto
    if "vantagens_do_produto" in dados:
        vantagens = dados["vantagens_do_produto"]
        elementos.append(Paragraph("<b>Vantagens do Produto:</b>", estilo_subtitulo))
        if isinstance(vantagens, list):
            for vantagem in vantagens:
                elementos.append(Paragraph(f"- {vantagem}", estilo_texto))
        else:
            elementos.append(Paragraph(f"- {vantagens}", estilo_texto))
        elementos.append(Spacer(1, 0.5 * cm))

    # Número da Patente
    if "numero_da_patente" in dados:
        elementos.append(Paragraph(f"<b>Número da Patente:</b> {dados['numero_da_patente']}", estilo_texto))
        elementos.append(Spacer(1, 0.5 * cm))

    # Rodapé (Supervisores e Tags)
    rodape_content = []
    if "supervisores_contato" in dados:
        supervisores = dados["supervisores_contato"]
        rodape_content.append("<b>Contato dos Supervisores:</b>")
        if "email" in supervisores:
            rodape_content.append(f"Email: {supervisores['email']}")
        if "telefone" in supervisores:
            rodape_content.append(f"Telefone: {supervisores['telefone']}")
    if "tags_relacionadas_ao_produto" in dados:
        tags = dados["tags_relacionadas_ao_produto"]
        if isinstance(tags, list):
            tags_texto = ", ".join(tags[:5])  # Limitar a 5 tags
        else:
            tags_texto = tags
        rodape_content.append(f"<b>Tags Relacionadas:</b> {tags_texto}")

    if rodape_content:
        rodape_texto = "<br/>".join(rodape_content)
        elementos.append(Spacer(1, 1 * cm))
        elementos.append(Paragraph(rodape_texto, estilo_rodape))

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
    print(f"Flyer responsivo gerado com sucesso: {nome_arquivo}")


# Caminho para o JSON de entrada
caminho_json = "backend/src/generator/output_json/summary.json"

# Gerar o flyer responsivo
criar_flyer_responsivo(caminho_json, "flyer_responsivo.pdf")
