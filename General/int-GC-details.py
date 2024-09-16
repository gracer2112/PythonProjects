import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException, NoSuchElementException
from selenium.webdriver.common.keys import Keys
import re
import json
import time

default_direct = r'C:\users\erica.araujo\onedrive - 200dev\documentos\pythonprojects\General'

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


class GerenciadorChamados:
    def __init__(self, config):
        self.arquivo_chamados = config['issue_file']
        self.url_base = "http://192.168.1.15:8085/GerenciadorChamados/modulos/chamados/movimentacao-chamado.xhtml?pa=cc&id="
        self.email = config.get('email')
        self.password = config.get('password')
        self.driver = None
        self.chamados = []

    def iniciar_driver(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        service = Service(ChromeDriverManager().install())
        options = webdriver.ChromeOptions()
        options.add_experimental_option("detach", True)
        self.driver = webdriver.Chrome(service=service, options=options)

    def ler_arquivo_chamados(self):
        df_chamados = pd.read_excel(self.arquivo_chamados)
        df_chamados_fechados = df_chamados[df_chamados['Situação'] == 'Fechado']
        self.chamados = [Chamado(row['Nro'], row['Situação']) for _, row in df_chamados_fechados.iterrows()]

    def login_servicedesk(self):
        """Faz o login no sistema de chamados"""
        url = "http://192.168.1.15:8085/GerenciadorChamados/login.xhtml"
        self.driver.get(url)

        login_email = self.driver.find_element(By.XPATH, '//input[@placeholder="Informe seu login"]')
        login_email.clear()
        login_email.send_keys(self.email)

        login_password = self.driver.find_element(By.XPATH, '//input[@placeholder="Informe sua senha"]')
        login_password.clear()
        login_password.send_keys(self.password)
        
        login_password.send_keys(Keys.RETURN)

        time.sleep(3)  # Aguarda 3 segundos para garantir que o login seja processado

    def extrair_dados_chamado(self, chamado: Chamado):
        url_chamado = f"{self.url_base}{chamado.id_chamado}"
        self.driver.get(url_chamado)

        wait = WebDriverWait(self.driver, 20)  # Aumentando o tempo de espera para 20 segundos
        try:
            wait.until(EC.presence_of_element_located((By.CLASS_NAME, "ui-fieldset-content")))
        except TimeoutException:
            print(f"Tempo limite excedido ao carregar a página do chamado {chamado.id_chamado}")
            return

        time.sleep(2)  # Aguarda 2 segundos para garantir que a página esteja completamente carregada

        self._extrair_dados_elemento(chamado, "data_categorizacao", ["j_idt286", "j_idt287"])
        self._extrair_dados_elemento(chamado, "data_aceite", ["j_idt294", "j_idt298", "j_idt299"])
        self._extrair_dados_elemento(chamado, "tempo_categorizacao", ["j_idt305", "j_idt306"])
        self._extrair_dados_elemento(chamado, "tempo_atendimento", ["j_idt311", "j_idt312"])

        atuacoes = self._tentar_encontrar_elementos(By.CSS_SELECTOR, "div.ui-accordion-header.ui-helper-reset.ui-state-default.ui-corner-all")
        for atuacao in atuacoes:
            self._processar_atuacao(chamado, atuacao)

        for ocorrencia in chamado.ocorrencias:
            print(f"Ocorrência: {ocorrencia}")

    def _extrair_dados_elemento(self, chamado, atributo, ids):
        for id_elemento in ids:
            try:
                setattr(chamado, atributo, self.driver.find_element(By.ID, id_elemento).text)
                break
            except NoSuchElementException:
                time.sleep(1)

    def _tentar_encontrar_elementos(self, by, value):
        try:
            return self.driver.find_elements(by, value)
        except StaleElementReferenceException:
            time.sleep(1)
            return self.driver.find_elements(by, value)

    def _processar_atuacao(self, chamado, atuacao):
        try:
            tabela = atuacao.find_element(By.XPATH, ".//table")
            primeira_coluna = tabela.find_element(By.XPATH, ".//td[1]/label").text
            match = re.search(r"Por:\s*(.+?)\s*em:\s*(\d{2}/\d{2}/\d{4}\s*\d{2}:\d{2})", primeira_coluna)
            if match:
                nome = match.group(1)
                data_hora = match.group(2)
                minutos, title = self._extrair_dados_adicionais(tabela)
                chamado.adicionar_ocorrencia(nome, data_hora, primeira_coluna, minutos, title)
        except NoSuchElementException:
            print(f"Elemento de atuação não encontrado nesta ocorrência. Chamado: {chamado.id_chamado}")

    def _extrair_dados_adicionais(self, tabela):
        try:
            div_adicional = tabela.find_element(By.XPATH, ".//div")
            minutos = div_adicional.find_element(By.XPATH, ".//label[contains(@class, 'FontBold')]").text
            title = div_adicional.find_element(By.XPATH, ".//img[@title]").get_attribute("title")
            return minutos, title
        except NoSuchElementException:
            return None, None

    def processar_chamados(self):
        self.iniciar_driver()
        self.login_servicedesk()
        self.ler_arquivo_chamados()
        for chamado in self.chamados:
            self.extrair_dados_chamado(chamado)
            time.sleep(2)  # Aguarda 2 segundos entre a extração de dados de cada chamado
        self.driver.quit()

    def salvar_ocorrencias(self, arquivo_saida):
        self._salvar_ocorrencias(arquivo_saida)

    def salvar_ocorrencias_backup(self, arquivo_saida: str):
        """Salva as ocorrências em um arquivo de backup em caso de erro"""
        self._salvar_ocorrencias(arquivo_saida)

    def _salvar_ocorrencias(self, arquivo_saida):
        ocorrencias_lista = [
            [
                chamado.id_chamado,
                chamado.data_categorizacao,
                chamado.data_aceite,
                chamado.tempo_categorizacao,
                chamado.tempo_atendimento,
                ocorrencia["Nome"],
                ocorrencia["Data e Hora"],
                ocorrencia["Texto Atuação"],
                ocorrencia.get("Minutos", ""),
                ocorrencia.get("Title", "")
            ]
            for chamado in self.chamados
            for ocorrencia in chamado.ocorrencias
        ]

        df_ocorrencias = pd.DataFrame(ocorrencias_lista, columns=[
            "ID Chamado", "Data Categorização", "Data Aceite",
            "Tempo Categorização", "Tempo Atendimento",
            "Nome", "Data e Hora", "Texto Atuação", "Minutos", "Title"
        ])
        df_ocorrencias.to_excel(arquivo_saida, index=False)

# Carrega as configurações do arquivo JSON
with open(default_direct+'\gercham.json','r') as file:
    config = json.load(file)

# Execução
gerenciador = GerenciadorChamados(config)
try:
    gerenciador.processar_chamados()
    gerenciador.salvar_ocorrencias("ocorrencias_chamados.xlsx")
except Exception as e:
    print(f"Erro: {e}")
    # Salvar os dados em caso de erro
    gerenciador.salvar_ocorrencias_backup("chamados_details_error_backup.xlsx")
    print("Dados salvos em chamados_details_error_backup.xlsx")
    raise