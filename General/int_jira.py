import base64
import requests
from requests.auth import HTTPBasicAuth
from urllib.parse import quote
import csv
import json
from collections import defaultdict
from datetime import datetime

import requests

JIRA_INSTALLATION = "timetiintegrada.atlassian.net"
E_MAIL = "erica.araujo@integrada.coop.br"
API_TOKEN = "ATATT3xFfGF0YdbDeAD5bm_Bh8zT2PgZbah-PPxVLRnS0Tp5ZKel0ZJ7S_vwIvJaoU7vAPcoLNjQFvsbp1ZK_0TCo_xzYYvpb87YhHItcseeZzxskelgk-8RfKgL_JVfOgw2y3ZUW55hEjTheU1dVqgM7MCtjV6l4X3sRYZuCX7XfxEGWujrfLA=E4C56923"

HEADER = ['Report Date', 'Issue ID', 'Issue Type', 'Story Points', 'Sprint', 'Reliability Engineer Type', 'Executors Teams',
          'PagSeguro Teams', 'Insight Business Unit', 'Operational Categorization', 'Labels', 'Assignee',
          'Epic Link', 'Issue Links', 'Sub Tasks', 'Backlog', 'Análise', 'Desenvolvimento', 'Aguardando Teste',
          'Code Review', 'Done','Pending', 'Summary', 'Impediment', 'Teste','Resolved','Homologação','Aguardando Deploy', 'Liberado', 'Cancelado']
ISSUE_TYPES = ['Backlog', 'Análise', 'Desenvolvimento', 'Code Review', 'Aguardando Teste', 'Done','Teste',
               'Impediment','Homologação','Aguardando Deploy','Liberado', 'Cancelado']
def main():
    # with open('jira.json', encoding='utf-8') as json_file:
    # issues_json = json.load(json_file)
    issues_json = call_jira_api('10111', '1000', '0')

    issues_total = issues_json['total']
    issues_retornados = issues_json['maxResults']
    pages = issues_total // issues_retornados
    page_num = 0
    writer = create_csv_with_header(page_num)

    if (issues_total % issues_retornados) != 0 :
        pages = pages + 1
    while page_num < pages :
        page_num = page_num + 1
        if page_num > 1 :
            startat = str(issues_retornados * (page_num-1))
            issues_json = call_jira_api('10111', '1000', startat)
        issues = issues_json['issues']
        for issue in issues:
            row_dict = defaultdict(dict)
            data_atual = datetime.today()
            row_dict['Report Date'] = data_atual.strftime('%d/%m/%Y')
            row_dict['Issue ID'] = issue['key']
            row_dict['Issue Type'] = issue['fields']['issuetype']['name']
            row_dict['Summary'] = issue['fields']['summary']

            try:
                issue['fields']['assignee']['displayName']
            except TypeError:
                row_dict['Assignee'] = ''
            else:
                row_dict['Assignee'] = issue['fields']['assignee']['displayName']

            try:
                issue['fields']['customfield_10014']
            except TypeError:
                row_dict['Epic Link'] = ''
            else:
                row_dict['Epic Link'] = issue['fields']['customfield_10014']

            if issue['fields']['customfield_10054']:
                for pagseguroteams in issue['fields']['customfield_10054']:
                    try:
                        pagseguroteams['value']
                    except TypeError:
                        row_dict['PagSeguro Teams'] = ''
                    else:
                        row_dict['PagSeguro Teams'] = pagseguroteams['value']
            else:
                row_dict['PagSeguro Teams'] = ''

            if issue['fields']['customfield_10020']:
                for sprint in issue['fields']['customfield_10020']:
                    try:
                        not sprint['name']
                    except TypeError:
                        row_dict['Sprint'] = ''
                    else:
                        row_dict['Sprint'] = sprint['name']


            apoio = ''

            if issue['fields']['issuetype']['name'] == 'Sub-task':
                try:
                    issue['fields']['parent']['key']
                except TypeError:
                    apoio = apoio + '' + ";"
                else:
                    apoio = apoio + issue['fields']['parent']['key'] + ";"

            for issuelink in issue['fields']['issuelinks']:
                if issuelink['type']['name'] == "Issue split" \
                        and not 'inwardIssue' in issuelink and not 'outwardIssue' in issuelink :
                    try:
                         not issuelink['inwardIssue']['key'] and not issuelink['outwardIssue']['key']
                    except TypeError:
                        apoio  = apoio + '' + ";"
                    else:
                        apoio = apoio + issuelink['inwardIssue']['key'] + ";"
                        apoio = apoio + issuelink['outwardIssue']['key'] + ";"

            row_dict['Issue Links'] = apoio

            apoio = ''
            for subtask in issue['fields']['subtasks']:
                try:
                    subtask['key']
                except TypeError:
                    apoio  = apoio + '' + ";"
                else:
                    apoio = apoio + subtask['key'] + ";"

            row_dict['Sub Tasks'] = apoio

            apoio = ''
            for label in issue['fields']['labels']:
                    apoio = apoio + label + ";"

            row_dict['Labels'] = apoio

            row_dict['Backlog'] = to_date(issue['fields']['created'])
            print("Key:%s Created: %s" % (issue['key'], issue['fields']['created']))
            for history in issue['changelog']['histories']:
                for item in history['items']:
                    if item['field'] == 'status' and item['toString'] in ISSUE_TYPES:
                        row_dict[item['toString']] = to_date(history['created'])
                    if item['field'] == 'Flagged' and item['toString'] in ISSUE_TYPES:
                        row_dict[item['toString']] = to_date(history['created'])
            writer.writerow(row_dict)

def to_date(str_date):
    date = datetime.strptime(str_date, "%Y-%m-%dT%H:%M:%S.%f%z")
    return datetime.strftime(date, "%Y-%m-%d")
def create_csv_with_header(page_qtd):
    nome_csv = 'jira-pags_' + str(page_qtd) + '.csv'
    csv_file = open(nome_csv, 'w')
    csv_writer = csv.DictWriter(csv_file, delimiter=';', fieldnames=HEADER, lineterminator='\n')
    csv_writer.writeheader()
    return csv_writer

def call_jira_api(filter_id, maxresults, startat):
    """
    Função para fazer chamadas à API do Jira.

    :param filter_id: ID do filtro Jira.
    :param maxresults: Número máximo de resultados a serem retornados.
    :param startat: Ponto de início para a paginação.
    :param email: Email do usuário.
    :param api_token: Token de API do Jira.
    :return: Resposta da API em formato JSON.
    """
    headers = get_headers(E_MAIL, API_TOKEN)

    url = f"https://{JIRA_INSTALLATION}/rest/api/2/search?jql=filter={filter_id}&startAt={startat}&maxResults={maxresults}&expand=changelog&"

    response = requests.get(url, headers=headers, verify=False)  # Desabilitar verificação SSL para testes

    # Verifique se a chamada foi bem-sucedida
    if response.status_code not in [200, 201, 204]:
        raise Exception(f"Falha ao acessar a API: {response.status_code} - {response.text}")

    print(f"URL: {url}")  # Adicione esta linha para verificar a URL gerada

    return response.json()

def get_headers(username, api_token):
    """
    Função para gerar cabeçalhos de autenticação básica.

    :param username: Nome de usuário (email).
    :param api_token: Token de API do Jira.
    :return: Dicionário de cabeçalhos.
    """
    # Combine username e token de API no formato 'username:api_token'
    credentials = f"{username}:{api_token}"

    # Codifique as credenciais em Base64
    encoded_credentials = base64.b64encode(credentials.encode('utf-8')).decode('utf-8')

    headers = {
        'Authorization': 'Basic %s' % encoded_credentials,
        'Content-Type': 'application/json'
    }
    return headers


if __name__ == '__main__':
    main()

# "https://timetiintegrada.atlassian.net/rest/api/2/search?jql=filter=10111&startAt=0&maxResults=1000&expand=changelog&",