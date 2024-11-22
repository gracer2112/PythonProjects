from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import ElementClickInterceptedException,NoSuchElementException,StaleElementReferenceException, WebDriverException
from webdriver_manager.chrome import ChromeDriverManager
import json
import time
import math
import pandas as pd

chrome_dir=r"C:/Users/erica.araujo/OneDrive - 200DEV/Documentos/PythonProjects/chromedriver_win32"
class EasyApplyLinkedin:
    def __init__(self,data):
        """Inicializa a classe com o conteudo do arquivo de configuração"""
        self.email = data['email']
        self.password = data['password']
        self.keywords = data['keyword']
        self.location = data['location']
        self.job_details = []

        chrome_options = webdriver.ChromeOptions()
#        chrome_options.add_argument('--headless')
#        options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option("detach", True)
#        service = Service(chrome_dir)
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)


    def login_linkedin(self):
        """Faz o login no linkedin"""
        url = "https://www.linkedin.com/home"
        self.driver.get(url)

        WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((By.NAME, 'session_key')
                                           ))
        login_email = self.driver.find_element(By.NAME,'session_key')
        login_email.clear()
        login_email.send_keys(self.email)

        login_password = self.driver.find_element(By.NAME,'session_password')
        login_password.clear()
        login_password.send_keys(self.password)

        login_password.send_keys(Keys.RETURN)
        time.sleep(30)


    def job_search(self):
        """Altera o link ir direto para a pagina de search do LinkedIn"""
        url = (
        "https://www.linkedin.com/jobs/search/?geoId=106057199&keywords="
        "%22COORDENADOR%20DE%20PROJETOS%22%20OR%20%22LIDER%20DE%20PROJETOS%22%20OR%20%22SUPERVISOR%20DE%20PROJETOS%22"
        "%20OR%20%22ANALISTA%20DE%20%20PROJETOS%22%20OR%20%20%22Project%20Manager%22%20OR%20%22Gerente%20de%20Projetos%22"
        "%20OR%20%22CONSULTOR%20DE%20PROJETO%22%20OR%20%22DIRETOR%20DE%20PROJETO%22%20OR%20%22GESTOR%20DE%20PROJETO%22"
        "%20OR%20%22Scrum%20Master%22%20OR%20%22Agile%20Coach%22%20OR%20%22Agile%20Facilitator%22%20OR%20%22Agile%20Project%20Manager%22"
        "%20OR%20%22Agile%20Delivery%20Manager%22%20OR%20%22Agile%20Program%20Manager%22%20OR%20%22Agile%20Transformation%20Lead%22"
        "%20OR%20%22Lean%20Agile%20Coach%22%20OR%20%22Agile%20Consultant%22%20OR%20%22Agile%20Product%20Owner%22%20OR%20%22Agile%20Team%20Lead%22"
        "%20OR%20%22Agile%20Release%20Train%20Engineer%22%20OR%20%22Agile%20Portfolio%20Manager%22%20OR%20%22Agile%20Development%20Manager%22"
        "%20OR%20%22Agile%20Process%20Manager%22%20OR%20%22Agile%20Master%22&origin=JOB_SEARCH_PAGE_SEARCH_BUTTON&refresh=true"
            )

        #     url = (
    # "https://www.linkedin.com/jobs/search/?geoId=106057199&keywords="
    # "%22COORDENADOR%20DE%20PROJETOS%22%20OR%20%22LIDER%20DE%20PROJETOS%22%20OR%20%22SUPERVISOR%20DE%20PROJETOS%22"
    # "%20OR%20%22ANALISTA%20DE%20%20PROJETOS%22%20OR%20%20%22Project%20Manager%22%20OR%20%22Gerente%20de%20Projetos%22"
    # "%20OR%20%22CONSULTOR%20DE%20PROJETO%22%20OR%20%22DIRETOR%20DE%20PROJETO%22%20OR%20%22GESTOR%20DE%20PROJETO%22"
    # "%20OR%20%22Scrum%20Master%22%20OR%20%22Agile%20Coach%22%20OR%20%22Agile%20Facilitator%22%20OR%20%22Agile%20Project%20Manager%22"
    # "%20OR%20%22Agile%20Delivery%20Manager%22%20OR%20%22Agile%20Program%20Manager%22%20OR%20%22Agile%20Transformation%20Lead%22"
    # "%20OR%20%22Lean%20Agile%20Coach%22%20OR%20%22Agile%20Consultant%22%20OR%20%22Agile%20Product%20Owner%22%20OR%20%22Agile%20Team%20Lead%22"
    # "%20OR%20%22Agile%20Release%20Train%20Engineer%22%20OR%20%22Agile%20Portfolio%20Manager%22%20OR%20%22Agile%20Development%20Manager%22"
    # "%20OR%20%22Agile%20Process%20Manager%22%20OR%20%22Agile%20Master%22%20AND%20%22Ingl%C3%AAs%20Avan%C3%A7ado%22&origin=JOB_SEARCH_PAGE_SEARCH_BUTTON&refresh=true"
    #     )
        #url = "https://www.linkedin.com/jobs/search/?currentJobId=3921020217&geoId=106057199&keywords=%22Coordenador%20de%20Projetos%22%20or%20%22AGILISTA%22%20OR%20%22ANALISTA%20DE%20%20PROJETOS%22%20OR%20%20%22Project%20Manager%22%20OR%20%22Gerente%20de%20Projetos%22%20OR%20%22Scrum%20Master%22%20OR%20%22Agile%20Master%22%20NOT%20%22Ingl%C3%AAs%20Avan%C3%A7ado%22&location=Brasil&origin=JOB_SEARCH_PAGE_SEARCH_BUTTON&refresh=true"
        #url = "https://www.linkedin.com/jobs/search/?keywords=%22AGILISTA%22%20OR%20%22ANALISTA%20DE%20%20PROJETOS%22%20OR%20%20%22Project%20Manager%22%20OR%20%22Gerente%20de%20Projetos%22%20OR%20%22Scrum%20Master%22%20OR%20%22Agile%20Master%22%20NOT%20%22Ingl%C3%AAs%20Avan%C3%A7ado%22&location=Brasil&origin=JOB_SEARCH_PAGE_SEARCH_BUTTON&refresh=true"
        self.driver.get(url)
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'occludable-update'))
        )
#        time.sleep(3)

    def filter_easy_apply(self):
        """"filtra as vagas para somente candidatura simplificada"""
        all_filters_button = self.driver.find_element(By.XPATH, "//button[contains(@aria-label,'Exibir todos os filtros')]")
        all_filters_button.click()
        time.sleep(1)
        easy_apply_button = self.driver.find_element(By.CLASS_NAME,"artdeco-toggle__button ")
        easy_apply_button.send_keys(Keys.SPACE)
        time.sleep(3)
        apply_filter_button = self.driver.find_element(By.XPATH,"//button[contains(@aria-label,'Aplicar filtros atuais')]")
        apply_filter_button.click()
        time.sleep(1)

    def filter_remote(self):
        """"filtra as vagas para somente candidatura remota"""
        remote_button = self.driver.find_element(By.XPATH, "//button[contains(@aria-label,'Exibir todos os filtros')]")
        remote_button.click()
        time.sleep(1)

        # Localiza o label que contém a palavra "Remoto"
        label_remoto = self.driver.find_element(By.XPATH, "//label[contains(., 'Remoto')]")

        hover_checkbox = ActionChains(self.driver).move_to_element(label_remoto)
        time.sleep(2)
        hover_checkbox.perform()
        time.sleep(1)

        # Encontra o input associado ao label
        checkbox_remoto = label_remoto.find_element(By.XPATH, "./preceding-sibling::input")

        # Tenta clicar no label em vez do input
        try:
            label_remoto.click()
        except:
            # Se clicar no label falhar, tenta clicar no input usando JavaScript
            self.driver.execute_script("arguments[0].click();", checkbox_remoto)

        # Verifica se o checkbox foi marcado
        assert checkbox_remoto.is_selected()
        time.sleep(3)

        # Localiza o label que contém a palavra "Hibrido"
        # label_hibrido = self.driver.find_element(By.XPATH, "//label[contains(., 'Híbrido')]")
        #
        # hover_checkbox = ActionChains(self.driver).move_to_element(label_hibrido)
        # time.sleep(2)
        # hover_checkbox.perform()
        # time.sleep(1)
        #
        # # Encontra o input associado ao label
        # checkbox_hibrido = label_hibrido.find_element(By.XPATH, "./preceding-sibling::input")

        # Tenta clicar no label em vez do input
        # try:
        #     label_hibrido.click()
        # except:
        #     # Se clicar no label falhar, tenta clicar no input usando JavaScript
        #     self.driver.execute_script("arguments[0].click();", checkbox_remoto)

        # Verifica se o checkbox foi marcado
        # assert checkbox_hibrido.is_selected()
        # time.sleep(3)

        apply_filter_button = self.driver.find_element(By.XPATH,"//button[contains(@aria-label,'Aplicar filtros atuais')]")
        apply_filter_button.click()
        time.sleep(1)

    def find_offers(self):
        """Navega pelas oportunidades e submete o cv"""
        try:
            total_results = self.driver.find_element(By.CLASS_NAME,'jobs-search-results-list__subtitle')
            total_results_txt = total_results.text.split(' ',1)[0].replace('.'," ")
            total_results_int = int((''.join(filter(str.isdigit, total_results_txt))))
        except NoSuchElementException:
            total_results_int =0

        print("Quantidade de jobs: ", total_results_int)

        if total_results_int == 0:
            self.close_session()
            return

        current_url = self.driver.current_url
        items_per_page = 24
        total_pages_int = math.ceil(total_results_int / items_per_page)
        print("Quantidade de páginas de resultados:", total_pages_int)

        # Variáveis para rastrear a navegação real
        current_page = 1

        while current_page <= total_pages_int:
            print(f"Processando página {current_page} de {total_pages_int}")

            try:        
                results = self.driver.find_elements(By.CLASS_NAME, 'occludable-update.p0.relative.scaffold-layout__list-item')

                i = 1
                for result in results:
                    hover = ActionChains(self.driver).move_to_element(result).perform()
                    titles = result.find_elements(By.CLASS_NAME, 'ember-view.job-card-container__link.job-card-list__title.job-card-list__title--link')
                    for title in titles:
                        print("Job no.:", i)
                        self.submmit_application(title)
                        i += 1

                try:
                    # Tente ir para a próxima página
                    next_button = WebDriverWait(self.driver, 10).until(
                        EC.element_to_be_clickable((By.CLASS_NAME, "jobs-search-pagination__button--next"))
                    )
                    next_button.click()
                    current_page += 1
                                   
                    # Aguarda até que a nova página esteja carregada
                    WebDriverWait(self.driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, f"//button[@aria-label='Página {current_page}']"))
                    )

                except (NoSuchElementException,ElementClickInterceptedException):
                    print("Não é possível avançar para a próxima página. Parando a navegação.")
                    break

            except StaleElementReferenceException:
                print("Elemento não está mais anexado ao DOM, tentando novamente...")
                continue
        
        print("Número final de páginas processadas:", current_page)    


    def submmit_application(self, job_ad):
        """submete o cv para vagas com candidatura simplificada e gera dataframe"""
        job_details = {}

        print('Vc está enviando cv para ', job_ad.text.split("\n")[0])
        job_link = job_ad.get_attribute("href") 
        time.sleep(1)

        job_ad.click()
        time.sleep(2)

        try:
# jun/24    job_company = self.driver.find_element(By.CLASS_NAME,"job-details-jobs-unified-top-card__primary-description-without-tagline.mb2")
            job_company = self.driver.find_element(By.CLASS_NAME,"job-details-jobs-unified-top-card__company-name")
            job_details['Company'] = job_company.text
        except NoSuchElementException:
            pass

        time.sleep(2)        

        try:
            job_info_loc = self.driver.find_element(By.CLASS_NAME,"job-details-jobs-unified-top-card__job-insight.job-details-jobs-unified-top-card__job-insight--highlight")
            job_info_tempo = self.driver.find_element(By.CLASS_NAME,"job-details-jobs-unified-top-card__primary-description-container")
            job_details['Job Info'] = job_info_tempo.text+"/"+job_info_loc.text
        except NoSuchElementException:
            pass

        time.sleep(1)

        job_details['Title'] = job_ad.text.split("\n")[0]
        job_details['Link'] = job_link
        
        job_code = job_link.split("view/")[1].split("/")[0]
        print ("Job Code: ", job_code)
        job_details['Code']=job_code

        try:
            in_apply = self.driver.find_element(By.XPATH,"//button[contains(@aria-label,'Candidatar-se')]")
            job_details['Easy Apply'] = "Employer"
            job_details['Sent Resume'] ="No"
            self.job_details.append(job_details)
            print('Direto no site do empregador')
            time.sleep(2)
            return
        except NoSuchElementException:
            pass

        try:
            in_apply = self.driver.find_element(By.CLASS_NAME,"jobs-apply-button.artdeco-button.artdeco-button--3.artdeco-button--primary.ember-view")
            in_apply.click()
        except NoSuchElementException:
            print('vc já enviou CV')
            job_details['Easy Apply'] = "Yes"
            job_details['Sent Resume'] ="Yes"
            self.job_details.append(job_details)
            time.sleep(2)
            return

        time.sleep(1)    

        try:
            submit=self.driver.find_element(By.XPATH,"//button[contains(@aria-label,'Enviar candidatura')]")
            submit.send_keys(Keys.RETURN)
            time.sleep(2)
            discard_submit = self.driver.find_element(By.CLASS_NAME,"artdeco-button.artdeco-button--circle.artdeco-button--muted.artdeco-button--2.artdeco-button--tertiary.ember-view.artdeco-modal__dismiss")
            discard_submit.send_keys(Keys.RETURN)
            print("CV enviado!")
            job_details['Easy Apply'] = "Yes"
            job_details['Sent Resume'] = "Yes"
            time.sleep(2)

        except NoSuchElementException:
            print('não é aplicação direta')
            try:
                discard=self.driver.find_element(By.XPATH,"//button[contains(@aria-label,'Fechar')]")
                discard.send_keys(Keys.RETURN)
                time.sleep(2)
                discard_confirm=self.driver.find_element(By.CLASS_NAME,"artdeco-button.artdeco-button--2.artdeco-button--secondary.ember-view.artdeco-modal__confirm-dialog-btn")
                discard_confirm.send_keys(Keys.RETURN)
                time.sleep(2)
                job_details['Easy Apply'] = "No"
                job_details['Sent Resume'] ="No"
            except NoSuchElementException:
                job_details['Easy Apply'] = "No"
                job_details['Sent Resume'] ="No"
                pass
        self.job_details.append(job_details)
        time.sleep(2)
        return



    def close_session(self):
        """encerra processamento"""
        if not self.job_details:
            print("Nenhuma vaga encontrada. Encerrando aplicação")
            self._safe_close_driver()
            return

        df = pd.DataFrame(self.job_details)
        if df.empty:
            print("Nenhuma vaga encontrada. Encerrando aplicação")
            self._safe_close_driver()
            return

        # Verifica se todas as colunas esperadas estão presentes
        expected_columns = ['Title', 'Company', 'Link', 'Job Info', 'Easy Apply', 'Sent Resume', 'Code']
        for col in expected_columns:
            if col not in df.columns:
                df[col] = None

        df = df.drop_duplicates("Code")
        df = df[['Title', 'Company', 'Link', 'Job Info', 'Easy Apply', 'Sent Resume', 'Code']]
        df.to_excel('job_details.xlsx',index=False)

        print('Encerrando a aplicação')
        self._safe_close_driver()

    def _safe_close_driver(self):
        """Fecha o driver de forma segura"""
        try:
            self.driver.quit()
        except WebDriverException as e:
            print(f"Erro ao fechar o driver: {e}")

    def easy_apply(self):
        """Executa o processo de candidatura simplificada"""
        self.driver.maximize_window()
        self.login_linkedin()
        time.sleep(30)
        self.job_search()
        time.sleep(2)
        self.filter_remote()
        time.sleep(2)
        self.find_offers()
        time.sleep(2)
        self.close_session()

if __name__ == "__main__":
    bot = None
    try:
        with open('linkedin.json') as config_file:
            data = json.load(config_file)
        bot = EasyApplyLinkedin(data)
        bot.easy_apply()
    except Exception as e:
        print(f"Erro: {e}")
        if bot and bot.job_details:
            df = pd.DataFrame(bot.job_details)
            df.to_excel('job_details_error_backup.xlsx', index=False)
            print("Dados salvos em job_details_error_backup.xlsx")
        raise