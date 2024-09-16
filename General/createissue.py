# This code sample uses the 'requests' library:
# http://docs.python-requests.org
import requests
from requests.auth import HTTPBasicAuth
import json
import base64
import logging


API_JIRA="ATATT3xFfGF0g64Kr3HtllYyFFl7MDtNwGG1Gg2UNZK9NMrKS91Cu8X7E6Cb93hEd51e_JCSmMz0rR_FY4IxFR3VpeY5wFWKAjFKo44yzAWXPQtPJev-dSB6QhYURrr4SMcNVqlrri-XScsKAf8TlhiQIqNVgUuBAqiOPLRdJF65nTcNyOJtQmE=EB0B24F8"
E_MAIL = 'ericaaraujo2112@gmail.com'
JIRA_INSTALLATION="jtbtrekkingtur.atlassian.net"

def get_headers(username, api_token):
    credentials = f"{username}:{api_token}"
    encoded_credentials = base64.b64encode(credentials.encode('utf-8')).decode('utf-8')

    headers = {
        'Authorization': 'Basic %s' % encoded_credentials,
        'Content-Type': 'application/json'
    }
    return headers


def create_epic(summary, description):
  url = f"https://{JIRA_INSTALLATION}/rest/api/2/issue"
  headers = get_headers(E_MAIL, API_JIRA)

  payload = json.dumps(
    {
      "fields": {
        "project": {
          "key": "TE1"
        },
        "summary": summary,
        "issuetype": {
          "name": "Epic"
        },
        "description": description
      }
    }
  )
  response = requests.request(
    "POST",
    url,
    data=payload,
    headers=headers
    # auth=auth
  )
  
  if response.status_code not in [200, 201]:
        raise Exception(f"Falha ao criar épico: {response.status_code} - {response.text}")

  return response.json()

def update_epic(issue_id, summary=None, description=None, status=None, impediment_int=None):
    url = f"https://{JIRA_INSTALLATION}/rest/api/2/issue/{issue_id}"
    headers = get_headers(E_MAIL, API_JIRA)

    response = requests.request(
        "GET",
        url,
        headers=headers
  )    
    if response.status_code == 200:
        issue_data = response.json()
        print(f"Issue encontrada: {issue_data['key']} - {issue_data['fields']['summary']}")    

    # if response.status_code == 200:
    #     fields = response.json()
    #     # Adicionar log para inspecionar a estrutura dos campos
    #     print (f"Campos disponíveis: {fields}")

    #     # Verificar se 'customfield_10021' está presente e é um dicionário
    #     customfield_10021_exists = any(isinstance(field, dict) and field.get('id') == 'customfield_10021' for field in fields)

    #     if not customfield_10021_exists:
    #         print("O campo customfield_10021 não está disponível na issue.")

            # Verificar o status do projeto e definir o valor de customfield_10021

    if impediment_int == 0:
        customfield_10021_value = [{
            "value": "Impediment",
            "id": "10019"
                            }]
    else:
        customfield_10021_value = None

    payload = json.dumps(
    {
      "fields": {
        "summary": summary,
        "description": description,
        # "status": {
        #   "name": status
        # },
         "customfield_10021": customfield_10021_value
    }
    }  
  )
    response = requests.request(
      "PUT",
      url,
      data=payload,
      headers=headers
      # auth=auth
    )

    if response.status_code not in [200, 204]:
        raise Exception(f"Falha ao atualizar épico: {response.status_code} - {response.text}")

    # Tentar decodificar a resposta como JSON
    try:
        return response.json()
    except ValueError:
        return {"message": "Update successful, but no JSON response received"}

def get_transitions(issue_key):
    url = f"https://{JIRA_INSTALLATION}/rest/api/2/issue/{issue_key}/transitions"
    headers = get_headers(E_MAIL, API_JIRA)

    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"Falha ao obter transições: {response.status_code} - {response.text}")
    
    return response.json()

def transition_issue(issue_key, transition_id):
    url = f"https://{JIRA_INSTALLATION}/rest/api/2/issue/{issue_key}/transitions"
    headers = get_headers(E_MAIL, API_JIRA)

    payload = json.dumps({
        "transition": {
            "id": transition_id
        }
    })

    response = requests.post(url, data=payload, headers=headers)
    
    if response.status_code not in [200, 204]:
        raise Exception(f"Falha ao atualizar status: {response.status_code} - {response.text}")

    return response.json()

if __name__ == '__main__':
    # # Exemplo de criação de um épico
    # new_epic = create_epic("Novo Épico", "Descrição do novo épico")
    # print(new_epic)

    #identificação das transitions
    # try:
    #   issue_key = "TE1-3"  # Substitua pela chave do item no Jira
    #   transitions = get_transitions(issue_key)
    #   print("Transições disponíveis:")
    #   for transition in transitions['transitions']:
    #       print(f"ID: {transition['id']}, Nome: {transition['name']}")

    #   # Escolha a transição desejada (substitua pelo ID da transição desejada)
    #   transition_id = "11"  # Substitua pelo ID da transição desejada
    #   transition_response = transition_issue(issue_key, transition_id)
    #   print("Resposta da transição:", transition_response)
    # except Exception as e:
    #   print(e)
      html_content=0
    # Exemplo de atualização de um épico existente
      try:
        updated_epic = update_epic("TE1-3", summary="Resumo Atualizado 1", description=html_content, impediment_int=0)
        print(updated_epic)
      except Exception as e:
          print(e)
