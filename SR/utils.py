# utils.py
import base64
import json
import os
import re
from datetime import datetime, timedelta
import requests
from flask import flash, render_template, request, url_for, make_response, send_file, redirect
from weasyprint import HTML, CSS
import pandas as pd
from models import db, Projeto, Tarefa, EntregaTarefa, Problema, ProjetoSuperintendencia, ProjetoKeyUser, Superintendentes, Funcionarios, ProjetoFuncTI

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
JIRA_INSTALLATION = "timetiintegrada.atlassian.net"
E_MAIL = "erica.araujo@integrada.coop.br"
API_JIRA = "chave-api-do-jira"
KEY="TSI"

from datetime import datetime

def format_date(date_value, output_format="%d-%m-%Y"): 
    if date_value is None: return None 
    if isinstance(date_value, str): 
        try: 
        # Ajuste o formato se a string estiver em outro padrão, por exemplo: '%Y-%m-%d' 
            dt = datetime.strptime(date_value, "%Y-%m-%d") 
        except ValueError: 
        # Se a conversão falhar, retorne a própria string ou trate o erro como desejar. 
            return date_value 
        else: 
            return dt.strftime(output_format) 
        
    elif isinstance(date_value, datetime): 
        return date_value.strftime(output_format) 
    
    else: 
        return date_value
    
def calcular_dias_uteis(data_inicio, data_fim):
     dias_uteis = 0
     while data_inicio <= data_fim:
         if data_inicio.weekday() < 5:  # 0-4 correspondem a segunda a sexta-feira
             dias_uteis += 1
         data_inicio += timedelta(days=1)
     return dias_uteis

def get_headers(username, api_token):
    credentials = f"{username}:{api_token}"
    encoded_credentials = base64.b64encode(credentials.encode('utf-8')).decode('utf-8')

    headers = {
        'Authorization': 'Basic %s' % encoded_credentials,
        'Content-Type': 'application/json'
    }
    return headers

def generate_excel(projeto, tarefas, problemas):
    # Limpar o nome do projeto para ser usado no nome do arquivo
    nome_projeto_limpo = re.sub(r'[^\w\s-]', '', projeto.nome_projeto).strip().replace(' ', '_')

    # Construir o DataFrame para Informações Gerais
    data = {
        'Nome do Projeto': [projeto.nome_projeto],
        'Data do Relatório': [projeto.data_relatorio],
        'Gerente do Projeto': [projeto.gerente_projeto],
        'Equipe Envolvida': [projeto.equipe_envolvida],
        'Status Geral': [projeto.status_geral],
        'Resumo do Status': [projeto.resumo_status],
        'Principais Conquistas': [projeto.principais_conquistas],
        'Próximos Passos': [projeto.proximos_passos],
        'Solicitações': [projeto.solicitacoes],
        'Dependências': [projeto.dependencias],
        'Notas Adicionais': [projeto.notas_adicionais],
        'Numero do Chamado' : [projeto.order_number],
        'Status do Projeto' : [projeto.project_status]
    }
    df = pd.DataFrame(data)

    # Construir o DataFrame para Progresso das Tarefas
    tarefas_data = {
        'Tarefa': [tarefa.tarefa for tarefa in tarefas],
        'Responsável': [tarefa.responsavel for tarefa in tarefas],
        'Status': [tarefa.status for tarefa in tarefas],
        'Data de Início': [tarefa.data_inicio.strftime("%d-%m-%Y") for tarefa in tarefas],
        'Data de Término': [tarefa.data_termino.strftime("%d-%m-%Y") for tarefa in tarefas],
        'Observações': [tarefa.observacoes for tarefa in tarefas]
    }
    df_tarefas = pd.DataFrame(tarefas_data)

    # Construir o DataFrame para Problemas e Riscos
    if not problemas:
        problemas_data = {
            'Tipo': ['Não foram reportados problemas ou riscos até o momento desse report.'],
            'Problema/Risco': [''],
            'Impacto': [''],
            'Ação Corretiva': [''],
            'Agente de Solução': [''],
            'Data Alvo de Solução': [''],
            'Coordenador do Agente de Solução': [''],
            'Status': ['']
        }
    else:
        problemas_data = {
            'Tipo': [problema.tipo for problema in problemas],
            'Problema/Risco': [problema.problema_risco for problema in problemas],
            'Impacto': [problema.impacto for problema in problemas],
            'Ação Corretiva': [problema.acao_corretiva for problema in problemas],
            'Agente de Solução': [problema.agente_solucao for problema in problemas],
            'Data Alvo de Solução': [problema.data_alvo_solucao.strftime("%d-%m-%Y") for problema in problemas],
            'Coordenador do Agente de Solução': [problema.coordenador_agente_solucao for problema in problemas],
            'Status': [problema.status for problema in problemas]
        }
        
    df_problemas = pd.DataFrame(problemas_data)

    # Obter superintendências associadas ao projeto
    projeto_superintendencias = ProjetoSuperintendencia.query.filter_by(projeto_id=projeto.id).all()
    superintendencias = [Superintendentes.query.get(ps.superintendencia_id) for ps in projeto_superintendencias]

    # Obter key users associados ao projeto
    projeto_key_users = ProjetoKeyUser.query.filter_by(projeto_id=projeto.id).all()
    key_users = [Funcionarios.query.get(ku.funcionario_id) for ku in projeto_key_users]

    # Construir o DataFrame para Superintendências
    superintendencias_data = {
        'Superintendência': [superintendencia.superintendencia for superintendencia in superintendencias],
        'Nome do Superintendente': [superintendencia.nomesuperintendente for superintendencia in superintendencias],
        'Email do Superintendente': [superintendencia.emailsuperintendente for superintendencia in superintendencias]
    }
    df_superintendencias = pd.DataFrame(superintendencias_data)

    # Construir o DataFrame para Key Users
    key_users_data = {
        'Nome': [key_user.nome for key_user in key_users],
        'Cargo': [key_user.cargo for key_user in key_users],
        'Email': [key_user.email for key_user in key_users]
    }
    df_key_users = pd.DataFrame(key_users_data)

    # Salvar em Excel
    file_name = f"diario_de_bordo_{nome_projeto_limpo}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    with pd.ExcelWriter(file_name) as writer:
        df.to_excel(writer, sheet_name='Informacoes_Gerais', index=False)
        df_tarefas.to_excel(writer, sheet_name='Progresso_Tarefas', index=False)
        df_problemas.to_excel(writer, sheet_name='Problemas_Riscos', index=False)

    return file_name

def generate_pdf_report(projeto_id):
    projeto = Projeto.query.get_or_404(projeto_id)

    # Filtrar tarefas concluídas no mês corrente
    tarefas = Tarefa.query.filter_by(projeto_id=projeto.id).order_by(Tarefa.data_inicio).all()
    tarefas_filtradas = []
    for tarefa in tarefas:
        entrega = EntregaTarefa.query.filter_by(tarefa_id=tarefa.id).order_by(EntregaTarefa.id.desc()).first()
        
        data_entrega_inicio = entrega.data_entrega_inicio if entrega else None
        data_entrega_fim = entrega.data_entrega_fim if entrega else None

        if tarefa.status.lower() == 'concluída':
            if tarefa.data_termino.month == datetime.now().month and tarefa.data_termino.year == datetime.now().year:
                tarefas_filtradas.append({
                    'tarefa': tarefa,
                    'data_entrega_inicio': format_date(data_entrega_inicio, "%d-%m-%Y") if entrega else None,
                    'data_entrega_fim': format_date(data_entrega_fim, "%d-%m-%Y") if entrega else None
                    })
        else:
            # Outras condições para tarefas não concluídas
            if tarefa.status.lower() in ['planejada', 'replanejada', 'prazo vencido']:
                data_entrega_inicio = None
                data_entrega_fim = None
            elif tarefa.status == 'Em Andamento':
                current_start_date = data_entrega_inicio
                if entrega:
                    if entrega.data_entrega_inicio and current_start_date != entrega.data_entrega_inicio:
                        data_entrega_inicio = entrega.data_entrega_inicio
                    else:
                        data_entrega_inicio = None
                data_entrega_fim = None

            tarefas_filtradas.append({
                'tarefa': tarefa,
                'data_entrega_inicio': format_date(data_entrega_inicio, "%d-%m-%Y") if data_entrega_inicio is not None else None,
                'data_entrega_fim': format_date(data_entrega_fim, "%d-%m-%Y") if data_entrega_fim is not None else None
            })


    # Filtrar e ordenar problemas
    problemas = Problema.query.filter_by(projeto_id=projeto.id).all()
    problemas_resolvidos = [problema for problema in problemas if 'resolvida' in problema.status.lower()]
    problemas_nao_resolvidos = [problema for problema in problemas if 'resolvida' not in problema.status.lower()]
    
    # Ordenar problemas resolvidos por data de solução (do mais antigo para o mais novo)
    problemas_resolvidos_ordenados = sorted(problemas_resolvidos, key=lambda x: x.data_alvo_solucao)
    
    # Combinar listas
    problemas_ordenados = problemas_nao_resolvidos + problemas_resolvidos_ordenados
    
    problemas_reportados = len(problemas_ordenados) > 0

    # Obter superintendências e key users associados ao projeto
    projeto_superintendencias = ProjetoSuperintendencia.query.filter_by(projeto_id=projeto.id).all()
    projeto_key_users = ProjetoKeyUser.query.filter_by(projeto_id=projeto.id).all()
    projeto_funcionarios_ti = ProjetoFuncTI.query.filter_by(projeto_id=projeto.id).all()

    superintendencias = [Superintendentes.query.get(ps.superintendencia_id) for ps in projeto_superintendencias]
    key_users = [Funcionarios.query.get(ku.funcionario_id) for ku in projeto_key_users]
    funcionarios_ti = [Funcionarios.query.get(pfti.funcionario_id) for pfti in projeto_funcionarios_ti]

    # Renderizar o conteúdo HTML do relatório
    html_content = render_template(
        'report.html',
        projeto=projeto,
        tarefas=tarefas_filtradas,
        problemas=problemas_ordenados,
        problemas_reportados=problemas_reportados,
        superintendencias=superintendencias,
        key_users=key_users,
        funcionarios_ti=funcionarios_ti  )
    
    # Gerar PDF em modo paisagem
    pdf = HTML(string=html_content, base_url=request.url_root).write_pdf(stylesheets=[CSS(string='@page { size: A4 landscape; }')])

    # Formatar a data do relatório
    data_relatorio_str = projeto.data_relatorio.strftime('%Y-%m-%d')

    # Definir o nome do arquivo PDF
    filename = f"report_{projeto_id}_{data_relatorio_str}.pdf"

    # Salvar o PDF em um diretório específico
    pdf_path = os.path.join(BASE_DIR,'static', 'reports', filename)
    with open(pdf_path, 'wb') as f:
        f.write(pdf)

    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = f'inline; filename={filename}'

    return response

def get_transition_id(project_status):
    """Mapeia o status do projeto para o transition_id do Jira."""
    status_map = {
        "Aguardando inicio": 11,  # Backlog
        "Cancelado": 111,       # Cancelado
        "Em Estudo": 21,          # Análise
        "Concluido": 91,       # Concluído
        "Em Andamento": 31,       # Em Desenvolvimento
        "Implantado": 81          # Liberado
    }
    return status_map.get(project_status)

def transition_issue(issue_key, transition_id):
    """Realiza a transição da issue no Jira para o transition_id especificado."""
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

def check_jira_issue(projeto_id):
    projeto = Projeto.query.get_or_404(projeto_id)
    id_jira = projeto.id_jira
    
    # Configurações da API do Jira
    jira_url = f"https://{JIRA_INSTALLATION}/rest/api/2"
    jira_auth = get_headers(E_MAIL, API_JIRA)

    # Obter superintendências e key users associados ao projeto
    projeto_superintendencias = ProjetoSuperintendencia.query.filter_by(projeto_id=projeto.id).all()
    projeto_key_users = ProjetoKeyUser.query.filter_by(projeto_id=projeto.id).all()
    
    superintendencias = [Superintendentes.query.get(ps.superintendencia_id) for ps in projeto_superintendencias]
    key_users = [Funcionarios.query.get(ku.funcionario_id) for ku in projeto_key_users]

    # Formatando a descrição do Jira com superintendências e key users
    superintendencias_str = "\n".join([f"* {s.superintendencia} - {s.nomesuperintendente} ({s.emailsuperintendente})" for s in superintendencias])
    key_users_str = "\n".join([f"* {k.nome} - {k.cargo} ({k.email})" for k in key_users])
    
    description = f"""
    h2. Informações do Projeto

    * *Gerente do Projeto*: {projeto.gerente_projeto}
    * *Equipe Envolvida*: {projeto.equipe_envolvida}
    * *Status Geral*: {projeto.status_geral}
    * *Estado do Projeto*: {projeto.project_status}

    h2. Resumo do Status

    {projeto.resumo_status}

    h2. Principais Conquistas

    {projeto.principais_conquistas}

    h2. Próximos Passos

    {projeto.proximos_passos}

    h2. Solicitações e Dependências

    * *Solicitações*: {projeto.solicitacoes}
    * *Dependências*: {projeto.dependencias}

    h2. Notas Adicionais

    {projeto.notas_adicionais}

    h2. Superintendências

    {superintendencias_str}

    h2. Key Users

    {key_users_str}
    """

    if not id_jira:
        # Criar novo issue no Jira
        summary = f"{projeto.nome_projeto} - [ID: {projeto.id}]"
        if projeto.order_number:
            summary += f" [Chamado: {projeto.order_number}]"
        
        issue_data = json.dumps({
            "fields": {
                "project": {
                    "key": KEY
                },
                "summary": summary,
                "description": description,
                "issuetype": {
                    "name": "Story"
                }
            }
        })

        response = requests.request(
            "POST",
            f"{jira_url}/issue",
            data=issue_data,
            headers=jira_auth)
        
        if response.status_code in [200, 201]:
            issue = response.json()
            projeto.id_jira = issue['key']
            db.session.commit()
            flash(f"Issue criada no Jira: {issue['key']}")
            # Upload do PDF para o Jira
        else:
            flash("Falha ao criar o issue no Jira.")
            raise Exception(f"Falha ao criar issue: {response.status_code} - {response.text}")
    else:
        # Verificar se o issue existe no Jira e atualizar a descrição
        response = requests.request(
            "GET",
            f"{jira_url}/issue/{id_jira}",
            headers=jira_auth
        )            

        if response.status_code in [200, 201]:
            issue_data = response.json()
            flash(f"Issue encontrada: {issue_data['key']} - {issue_data['fields']['summary']}")

            # Verificar o status do projeto e definir o valor de customfield_10021
            if projeto.project_status.lower() == "bloqueado":
                customfield_10021_value = [{
                    "value": "Impediment",
                    "id": "10019"
                }]
            else:
                """Atualiza o status da issue no Jira com base no project_status."""
                transition_id = get_transition_id(projeto.project_status)
                if transition_id is None:
                    raise ValueError(f"Status do projeto '{projeto.project_status}' não mapeado para um transition_id.")

                try:
                    transition_issue(id_jira, transition_id)
                    print(f"Status da issue {id_jira} atualizado para '{projeto.project_status}'.")
                except Exception as e:
                    print(f"Erro ao atualizar o status da issue {id_jira}: {str(e)}")

                customfield_10021_value = None

            # Atualizar a descrição da issue
            update_data = json.dumps({
                "fields": {
                    "description": description,
                    "customfield_10021": customfield_10021_value
                }
            })

            update_response = requests.request(
                "PUT",
                f"{jira_url}/issue/{id_jira}",
                data=update_data,
                headers=jira_auth
            )

            if update_response.status_code == 204:
                flash(f"Descrição da issue {id_jira} atualizada com sucesso.")
            else:
                error_message = update_response.json().get('errors', {})
                flash(f"Falha ao atualizar a descrição da issue {id_jira}.Erro: {error_message}")
        else:
            flash("Não foi possível encontrar um issue no Jira com o ID fornecido.")
            return redirect(url_for('main.view_report', projeto_id=projeto.id)) 
        
    return redirect(url_for('main.upload_pdf_to_jira_route', projeto_id=projeto.id))

def upload_pdf_to_jira(projeto_id):

    projeto = Projeto.query.get_or_404(projeto_id)
    id_jira = projeto.id_jira

    if not id_jira:
        flash("Este projeto não possui um ID do Jira associado.")
        return redirect(url_for('main.view_report', projeto_id=projeto.id))

    jira_url = f"https://{JIRA_INSTALLATION}/rest/api/2"
    headers = get_headers(E_MAIL, API_JIRA)

    pdf_path = os.path.join(BASE_DIR,'static', 'reports', f"report_{projeto_id}_{projeto.data_relatorio.strftime('%Y-%m-%d')}.pdf")
    try:
        with open(pdf_path, 'rb') as pdf_file:
            files = {
            'file': (os.path.basename(pdf_path), pdf_file, 'application/pdf')
        }
            upload_headers = {
            "Authorization": headers['Authorization'],
            "X-Atlassian-Token": "no-check"
        }

            upload_response = requests.request(
                "POST",
                f"{jira_url}/issue/{id_jira}/attachments",
                headers=upload_headers,
                files=files)    
                                
            if upload_response.status_code in [200, 201]:
                flash(f"Relatório PDF carregado para o Jira: {id_jira}")
            else:
                flash("Falha ao carregar o relatório PDF para o Jira.")
    except FileNotFoundError:
        flash("Arquivo PDF não encontrado. Certifique-se de que o relatório foi gerado corretamente.")
        return redirect(url_for('main.view_report', projeto_id=projeto.id))
    except Exception as e:
        flash(f"Ocorreu um erro ao tentar carregar o PDF para o Jira: {str(e)}")
        return redirect(url_for('main.view_report', projeto_id=projeto.id))            

    return redirect(url_for('main.view_report', projeto_id=projeto.id))


