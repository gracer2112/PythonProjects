import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException, StaleElementReferenceException
from selenium.webdriver.common.keys import Keys
import re
import time

# Configurações
config = {
    "driver_path": "C:/Users/erica.araujo/OneDrive - 200DEV/Documentos/PythonProjects/chromedriver_win32",  # Ajuste o caminho para o seu ChromeDriver
    "email": "erica.araujo",  # Substitua pelo seu email
    "password":"x5hL8D9q",  # Substitua pela sua senha
    "headless": False  # Altere para True se desejar usar o modo headless
}

class Chamado:
    def __init__(self, id_chamado, situacao):
        self.id_chamado = id_chamado
        self.situacao = situacao
        self.data_categorizacao = None
        self.data_aceite = None
        self.tempo_categorizacao = None
        self.tempo_atendimento = None
        self.ocorrencias = []

    def adicionar_ocorrencia(self, nome: str, data_hora: str, texto_atuacao: str, minutos: str = None, title: str = None):
        ocorrencia = {
            "Nome": nome,
            "Data e Hora": data_hora,
            "Texto Atuação": texto_atuacao
        }
        if minutos:
            ocorrencia["Minutos"] = minutos
        if title:
            ocorrencia["Title"] = title
        self.ocorrencias.append(ocorrencia)

# Função para iniciar o driver
def iniciar_driver(headless=False):
    options = webdriver.ChromeOptions()
    if headless:
        options.add_argument('--headless')
    options.add_experimental_option("detach", True)
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    return driver

# Função para realizar o login
def login_servicedesk(driver, email, password):
    url = "http://192.168.1.15:8085/GerenciadorChamados/login.xhtml"
    driver.get(url)

    login_email = driver.find_element(By.NAME, 'j_idt6:username')
    login_email.clear()
    login_email.send_keys(email)

    login_password = driver.find_element(By.NAME, 'j_idt6:password')
    login_password.clear()
    login_password.send_keys(password)

    login_password.send_keys(Keys.RETURN)

# Função para extrair dados de um chamado específico
def extrair_dados_chamado(driver, id_chamado):
    url_base = "http://192.168.1.15:8085/GerenciadorChamados/modulos/chamados/movimentacao-chamado.xhtml?pa=cc&id="
    url_chamado = f"{url_base}{id_chamado}"
    driver.get(url_chamado)

    wait = WebDriverWait(driver, 20)  # Aumentar o tempo de espera para 20 segundos

    def encontrar_elemento_por_ids(possiveis_ids):
        for id in possiveis_ids:
            try:
                return driver.find_element(By.ID, id).text
            except NoSuchElementException:
                time.sleep(1)
        return None

    # Tentar encontrar o elemento com os IDs especificados
    data_categorizacao = encontrar_elemento_por_ids(["j_idt286", "j_idt287"])
    if data_categorizacao is None:
        print(f"Tempo limite excedido ao carregar a página do chamado {id_chamado}")
        return

    data_aceite = encontrar_elemento_por_ids(["j_idt294", "j_idt298", "j_idt299"])
    tempo_categorizacao = encontrar_elemento_por_ids(["j_idt305", "j_idt306"])
    tempo_atendimento = encontrar_elemento_por_ids(["j_idt311", "j_idt312"])

    print(f"Dados do Chamado {id_chamado}:")
    print(f"Data de Categorização: {data_categorizacao}")
    print(f"Data de Aceite: {data_aceite}")
    print(f"Tempo de Categorização: {tempo_categorizacao}")
    print(f"Tempo de Atendimento: {tempo_atendimento}")

    try:
        atuacoes = driver.find_elements(By.CSS_SELECTOR, "div.ui-accordion-header.ui-helper-reset.ui-state-default.ui-corner-all")
    except StaleElementReferenceException:
        print("Elemento não encontrado na referência atual. Tentando novamente.")
        time.sleep(1)
        atuacoes = driver.find_elements(By.CSS_SELECTOR, "div.ui-accordion-header.ui-helper-reset.ui-state-default.ui-corner-all")

    chamado = Chamado(id_chamado, "Fechado")
    for atuacao in atuacoes:
        try:
            # Capturar o texto da atuação
            tabela = atuacao.find_element(By.XPATH, ".//table")
            primeira_coluna = tabela.find_element(By.XPATH, ".//td[1]/label").text
            match = re.search(r"Por:\s*(.+?)\s*em:\s*(\d{2}/\d{2}/\d{4}\s*\d{2}:\d{2})", primeira_coluna)
            if match:
                nome = match.group(1)
                data_hora = match.group(2)
                minutos = None
                title = None

                # Verificar se há uma div dentro da tabela
                try:
                    div_adicional = tabela.find_element(By.XPATH, ".//div")
                    minutos_element = div_adicional.find_element(By.XPATH, ".//label[contains(@class, 'FontBold')]")
                    minutos = minutos_element.text

                    img_element = div_adicional.find_element(By.XPATH, ".//img[@title]")
                    title = img_element.get_attribute("title")
                except NoSuchElementException:
                    print("Div adicional ou elementos adicionais não encontrados nesta atuação.")

                chamado.adicionar_ocorrencia(nome, data_hora, primeira_coluna, minutos, title)
        except NoSuchElementException:
            print("Elemento de atuação não encontrado nesta ocorrência.")
            
    for ocorrencia in chamado.ocorrencias:
        print(f"Ocorrência: {ocorrencia}")

# Execução
driver = iniciar_driver(headless=config['headless'])
login_servicedesk(driver, config['email'], config['password'])
extrair_dados_chamado(driver, 371069)
driver.quit()