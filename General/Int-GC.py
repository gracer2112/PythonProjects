from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException, NoSuchElementException, StaleElementReferenceException, WebDriverException, TimeoutException
import json
import time
import pandas as pd
import openpyxl

default_direct = r'C:\users\erica.araujo\onedrive - 200dev\documentos\pythonprojects\General'
columns_first_execution = ["Ordem", "Nro", "Prior.", "Área", "Estab.", "Módulo", "Motivo", "Abertura", "Situação", "Solicitante", "Analista", "Assunto", "Hrs", "Em Branco 1", "Em Branco 2"]
columns_second_execution = ["Ordem", "Nro", "Prior.", "Área", "Estab.", "Módulo", "Motivo", "Abertura", "Situação", "Solicitante", "Analista", "Assunto", "Hrs"]
df = pd.DataFrame(columns=columns_first_execution)

class EasySearch:
    def __init__(self, data):
        """Inicializa a classe com o conteúdo do arquivo de configuração"""
        self.email = data['email']
        self.password = data['password']
        self.startdate = data['startdate']
        self.enddate = data['enddate']
        self.issue_file = data['issue_file']
        self.issue_details = []
        self.first_execution = True  # Flag para controlar a primeira execução

        chrome_options = webdriver.ChromeOptions()
#        chrome_options.add_argument('--headless')
        chrome_options.add_experimental_option("detach", True)
        service = Service(ChromeDriverManager().install())
#        options = webdriver.ChromeOptions()

        self.driver = webdriver.Chrome(service=service, options=chrome_options)

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

    def servicedesk_filter(self):
        """Seleciona os chamados por filtros"""
        url = 'http://192.168.1.15:8085/GerenciadorChamados/modulos/chamados/consulta.xhtml'    
        self.driver.get(url)

        start_filter = self.driver.find_element(By.ID, "j_idt215_input")
        start_filter.clear()
        start_filter.send_keys(self.startdate)

        end_filter = self.driver.find_element(By.ID, "j_idt217_input")
        end_filter.clear()
        end_filter.send_keys(self.enddate)        

        if not self.first_execution:
            self.change_combo_value()

        find_button = self.driver.find_element(By.ID, "j_idt269")
        find_button.click()
        time.sleep(3)

    def change_combo_value(self):
        """Altera o valor do combo box para SAF-TI-INFRA"""
        combo_box = self.driver.find_element(By.ID, "j_idt224_label")
        combo_box.click()
        time.sleep(1)
        new_value = self.driver.find_element(By.XPATH, "//li[@data-label='SAF-TI-INFRA']")
        new_value.click()
        time.sleep(1)

    def extract_table_data(self, expected_columns):
        """Extrai dados da tabela"""
        data = []
        max_attempts = 3
        attempt = 0

        while attempt < max_attempts:
            try:
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_all_elements_located((By.XPATH, "//tbody[@id='DTConsulta_data']/tr")))
                   
                rows = self.driver.find_elements(By.XPATH, "//tbody[@id='DTConsulta_data']/tr")
                time.sleep(1)
                print("Extraindo dados", end="")
                for row in rows:
                    # Espera explícita para garantir que as colunas da linha estejam presentes
                    WebDriverWait(self.driver, 10).until(
                        EC.presence_of_all_elements_located((By.TAG_NAME, "td"))
                    )
                    cols = row.find_elements(By.TAG_NAME, "td")
                    time.sleep(2)
                    if len(cols) == len(expected_columns):  # Verifica se o número de colunas está correto
                        cols_data = [col.text for col in cols]
                        data.append(cols_data)
                        print(".", end="", flush=True)
                break  # Se a extração for bem-sucedida, sai do loop
            except (StaleElementReferenceException, NoSuchElementException, TimeoutException):
                attempt += 1
                print(f"\nTentativa {attempt} falhou. Tentando novamente...")
                if attempt == max_attempts:
                    print("Número máximo de tentativas atingido.")
                    time.sleep(1)
                    break  # Sai do loop após o número máximo de tentativas

        print()  # Nova linha após a extração
        return data

    def count_pages(self, expected_columns):
        """Conta o número de páginas e extrai dados de cada uma"""
        global df
        try:
#            select_filter = self.driver.find_element(By.ID, "DTConsulta:j_id33")
            select_filter = self.driver.find_element(By.NAME, "DTConsulta_rppDD")
            time.sleep(3)
            #select_filter = self.driver.find_element(By.ID, "DTConsulta")
        except NoSuchElementException:
            print("Elemento DTConsulta:j_id33 não encontrado. Tentando DTConsulta:j_id64.")
#            select_filter = self.driver.find_element(By.ID, "DTConsulta:j_id64")
            time.sleep(3)

        select = Select(select_filter)
        select.select_by_value('200')
        time.sleep(3)

        # Verifica se existe o botão da última página
        lastpage_button = self.driver.find_element(By.CSS_SELECTOR, 'a.ui-paginator-last')
        if 'ui-state-disabled' in lastpage_button.get_attribute('class'):
            print("Botão da última página desabilitado. Assumindo que há apenas uma página.")
            last_page_number = 1
        else:
            lastpage_button.click()
            time.sleep(3)

            paginator_elements = self.driver.find_elements(By.CLASS_NAME, 'ui-paginator-page')
            last_page_number = int(paginator_elements[-1].text)
        
        print(f"Última página: {last_page_number}")

        # Espera explícita para garantir que o botão de primeira pagina esteja presente
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'a.ui-paginator-first'))
                    )
        try:
            first_button = self.driver.find_element(By.CSS_SELECTOR, 'a.ui-paginator-first')
            first_button.click()
            time.sleep(3)
        except ElementClickInterceptedException:
            pass
        

        for page in range(1, last_page_number + 1):
            # Espera explícita para garantir que numero da pagina esteja presente
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located((By.XPATH, f'//a[@aria-label="Page {page}"]'))
                    )
            page_element = self.driver.find_element(By.XPATH, f'//a[@aria-label="Page {page}"]')
            page_element.click()
            time.sleep(3)

            table_data = self.extract_table_data(expected_columns)
            if table_data:  # Verifica se há dados extraídos
                temp_df = pd.DataFrame(table_data, columns=expected_columns)
                df = pd.concat([df, temp_df], ignore_index=True)

            # Salva os dados a cada 10 páginas
            if page % 10 == 0:
                df.to_excel(f'chamados_details_page_{page}.xlsx', index=False)
                print(f'Dados salvos em chamados_details_page_{page}.xlsx')

        # Salva os dados restantes após a última página
        df.to_excel(self.issue_file, index=False)
        print('Dados salvos em chamados_details.xlsx')

    def close_session(self):
        """Encerra o processamento"""
        global df
        if df.empty:
            print("Nenhum chamado encontrado. Encerrando aplicação")
        else:
            print("Processamento concluído. Dados salvos em arquivos Excel.")

        print('Encerrando a aplicação')
        self._safe_close_driver()

    def _safe_close_driver(self):
        """Fecha o driver de forma segura"""
        try:
            self.driver.quit()
        except WebDriverException as e:
            print(f"Erro ao fechar o driver: {e}")

    def easy_apply(self):
        """Executa o processo completo"""
        if self.first_execution:
            self.driver.maximize_window()
            self.login_servicedesk()

        self.servicedesk_filter()
        expected_columns = columns_first_execution if self.first_execution else columns_second_execution
        self.count_pages(expected_columns)

        if self.first_execution:
            self.first_execution = False
            self.servicedesk_filter()
            expected_columns = columns_second_execution
            self.count_pages(expected_columns)

        self.close_session()

if __name__ == "__main__":
    try:
        with open(default_direct+'\gercham.json','r') as config_file:
            data = json.load(config_file)
        bot = EasySearch(data)
        bot.easy_apply()
    except Exception as e:
        print(f"Erro: {e}")
        # Salvar os dados em caso de erro
        df.to_excel('chamados_details_error_backup.xlsx', index=False)
        print("Dados salvos em chamados_details_error_backup.xlsx")
        raise