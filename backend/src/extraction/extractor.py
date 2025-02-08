from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
import os
import subprocess

def fetch_rendered_html(url: str, driver_path: str):
    """
    Usa o Selenium para carregar e renderizar a página completamente e salva o HTML localmente.
    Em seguida, chama o parser para processar os dados extraídos.
    
    :param url: URL da página a ser carregada.
    :param driver_path: Caminho para o driver do Chrome (ex.: chromedriver.exe).
    """
    # Configurar opções do navegador
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Executa o Chrome sem interface gráfica
    chrome_options.add_argument("--disable-gpu")  # Desabilita GPU (opcional)
    chrome_options.add_argument("--no-sandbox")  # Necessário para alguns sistemas Linux

    # Iniciar o driver
    service = Service(driver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        print(f"🔹 Carregando página: {url}")
        driver.get(url)
        time.sleep(3)  # Aguarda o carregamento do conteúdo dinâmico (ajuste se necessário)
        
        # Captura o HTML renderizado
        html = driver.page_source
        print("✅ Página carregada com sucesso.")

        # Definir caminho para salvar o HTML
        output_dir = os.path.join("backend", "src", "extraction", "output")
        os.makedirs(output_dir, exist_ok=True)
        output_file_path = os.path.join(output_dir, "rendered_page.html")

        # Salvar o HTML no arquivo
        with open(output_file_path, "w", encoding="utf-8") as file:
            file.write(html)

        print(f"✅ Página salva em: {output_file_path}")

        # Pequeno delay para garantir que o arquivo seja salvo corretamente
        time.sleep(2)

        # Chamar o parser automaticamente
        print("🔄 Chamando o parser para processar os dados...")
        parser_script = os.path.join("backend", "src", "generator", "groq_parser.py")
        subprocess.run(["python", parser_script], check=True)

    except Exception as e:
        print(f"❌ Erro ao carregar a página: {e}")
    finally:
        driver.quit()
