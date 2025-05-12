# # Definir o caminho absoluto para a pasta de templates
# template_dir = os.path.abspath(r'C:\Users\erica.araujo\OneDrive - 200DEV\Documentos\PythonProjects\SR\templates')
# app.template_folder=template_dir

# routes.py
from flask import Blueprint, render_template, request, redirect, url_for, flash, make_response, send_file
from extensions import db
from models import db, Projeto, Tarefa, EntregaTarefa, Problema, ProjetoSuperintendencia, ProjetoKeyUser, Superintendentes, Funcionarios, ProjetoFuncTI
from datetime import datetime
from utils import calcular_dias_uteis, format_date, get_headers, generate_excel, generate_pdf_report, upload_pdf_to_jira, check_jira_issue

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    projetos = Projeto.query.order_by(Projeto.created_at.asc()).all()
    return render_template('index.html', projetos=projetos)

@bp.route('/create', methods=['GET'])
def create():
    superintendencias = Superintendentes.query.all()
    funcionarios = Funcionarios.query.filter(Funcionarios.tipo_funcionario=='GEN').order_by(Funcionarios.nome).all()
    funcionarios_ti = Funcionarios.query.filter(Funcionarios.tipo_funcionario=='TEC').order_by(Funcionarios.nome).all()
    return render_template('create.html', superintendencias=superintendencias, funcionarios=funcionarios, funcionarios_ti=funcionarios_ti)

@bp.route('/submit', methods=['POST'])
def submit():
    # Capturar os dados do formulário
    nome_projeto = request.form['nome_projeto']
    data_relatorio = datetime.strptime(request.form['data_relatorio'], '%Y-%m-%d')
    gerente_projeto = request.form['gerente_projeto']
    equipe_envolvida = request.form['equipe_envolvida']
    status_geral = request.form['status_geral']
    resumo_status = request.form['resumo_status']
    principais_conquistas = request.form['principais_conquistas']
    proximos_passos = request.form['proximos_passos']
    solicitacoes = request.form['solicitacoes']
    dependencias = request.form['dependencias']
    notas_adicionais = request.form['notas_adicionais']
    numero_chamado = request.form['order_number']
    status_projeto = request.form['project_status']

    # Capturar IDs das superintendências e key users
    superintendencias_ids = request.form.getlist('superintendencias[]')
    key_users_ids = request.form.getlist('key_users[]')

    # Capturar IDs dos funcionários de TI
    funcionarios_ti_ids = request.form.getlist('funcionarios_ti[]')

#    import pdb; pdb.set_trace()  # Ponto de interrupção
    # Progresso das Tarefas
    tarefas = request.form.getlist('tarefas[]')
    responsaveis = request.form.getlist('responsaveis[]')
    status_tarefas = request.form.getlist('status_tarefas[]')
    datas_inicio = [datetime.strptime(date, '%Y-%m-%d') for date in request.form.getlist('datas_inicio[]')]
    datas_termino = [datetime.strptime(date, '%Y-%m-%d') for date in request.form.getlist('datas_termino[]')]
    datas_entrega_inicio = [datetime.strptime(date, '%Y-%m-%d') for date in request.form.getlist('datas_entrega_inicio[]')]
    datas_entrega_fim = [datetime.strptime(date, '%Y-%m-%d') for date in request.form.getlist('datas_entrega_fim[]')]
    observacoes = request.form.getlist('observacoes[]')


    # Verificar se pelo menos uma tarefa foi informada
    if not tarefas:
        flash("Por favor, adicione pelo menos uma tarefa.")
        return redirect(url_for('main.create'))

    # Problemas e Riscos
    tipos = request.form.getlist('tipos[]')
    problemas = request.form.getlist('problemas[]')
    impactos = request.form.getlist('impactos[]')
    acoes_corretivas = request.form.getlist('acoes_corretivas[]')
    agentes_solucao = request.form.getlist('agentes_solucao[]')
    datas_alvo_solucao = [datetime.strptime(date, '%Y-%m-%d') for date in request.form.getlist('datas_alvo_solucao[]')]
    coordenadores_agente_solucao = request.form.getlist('coordenadores_agente_solucao[]')
    status_problemas = request.form.getlist('status_problemas[]')

    # Criar um novo projeto
    novo_projeto = Projeto(
        nome_projeto=nome_projeto,
        data_relatorio=data_relatorio,
        gerente_projeto=gerente_projeto,
        equipe_envolvida=equipe_envolvida,
        status_geral=status_geral,
        resumo_status=resumo_status,
        principais_conquistas=principais_conquistas,
        proximos_passos=proximos_passos,
        solicitacoes=solicitacoes,
        dependencias=dependencias,
        notas_adicionais=notas_adicionais,
        order_number=numero_chamado,
        project_status=status_projeto
    )
    db.session.add(novo_projeto)
    db.session.commit()

    # Associar funcionários de TI ao projeto, se houver
    if funcionarios_ti_ids:
        for funcionario_ti_id in funcionarios_ti_ids:
            projeto_func_ti = ProjetoFuncTI(
                projeto_id=novo_projeto.id,
                funcionario_id=funcionario_ti_id
            )
            db.session.add(projeto_func_ti)

    # Adicionar superintendências ao projeto, se houver
    if superintendencias_ids:
        for superintendencia_id in superintendencias_ids:
            projeto_superintendencia = ProjetoSuperintendencia(
                projeto_id=novo_projeto.id,
                superintendencia_id=superintendencia_id
            )
            db.session.add(projeto_superintendencia)

    # Adicionar key users ao projeto, se houver
    if key_users_ids:
        for key_user_id in key_users_ids:
            projeto_key_user = ProjetoKeyUser(
                projeto_id=novo_projeto.id,
                funcionario_id=key_user_id
            )
            db.session.add(projeto_key_user)

    # Adicionar tarefas e entregas ao projeto
    for i in range(len(tarefas)):
        nova_tarefa = Tarefa(
            projeto_id=novo_projeto.id,
            tarefa=tarefas[i],
            responsavel=responsaveis[i],
            status=status_tarefas[i],
            data_inicio=datas_inicio[i],
            data_termino=datas_termino[i],
            observacoes=observacoes[i]
        )
        db.session.add(nova_tarefa)
        db.session.flush()  # Necessário para obter o id da tarefa

        # Tratar as datas de entrega
        #data_entrega_inicio = datetime.strptime(datas_entrega_inicio[i], '%Y-%m-%d') if datas_entrega_inicio[i] else None
        #data_entrega_fim = datetime.strptime(datas_entrega_fim[i], '%Y-%m-%d') if datas_entrega_fim[i] else None

        if datas_entrega_inicio[i] or datas_entrega_fim[i]:
            nova_entrega = EntregaTarefa(
                tarefa_id=nova_tarefa.id,
                data_entrega_inicio=datas_entrega_inicio[i],
                data_entrega_fim=datas_entrega_fim[i]
            )
            db.session.add(nova_entrega)

    # Adicionar problemas ao projeto
    for i in range(len(tipos)):
        novo_problema = Problema(
            projeto_id=novo_projeto.id,
            tipo=tipos[i],
            problema_risco=problemas[i],
            impacto=impactos[i],
            acao_corretiva=acoes_corretivas[i],
            agente_solucao=agentes_solucao[i],
            data_alvo_solucao=datas_alvo_solucao[i],
            coordenador_agente_solucao=coordenadores_agente_solucao[i],
            status=status_problemas[i]
        )
        if novo_problema.tipo == 'Problema':
            novo_problema.data_abertura = datetime.now().date()

        db.session.add(novo_problema)

    db.session.commit()

    flash("Projeto adicionado com sucesso!")
    return redirect(url_for('main.index'))

@bp.route('/report/<int:projeto_id>')
def view_report(projeto_id):
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
                    'data_entrega_inicio': data_entrega_inicio if entrega else None,
                    'data_entrega_fim': data_entrega_fim if entrega else None
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
                'data_entrega_inicio': data_entrega_inicio,
                'data_entrega_fim': data_entrega_fim
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

    return render_template('report.html', 
                           projeto=projeto, 
                           tarefas=tarefas_filtradas, 
                           problemas=problemas_ordenados, 
                           problemas_reportados=problemas_reportados, 
                           superintendencias=superintendencias, 
                           key_users=key_users,
                           funcionarios_ti=funcionarios_ti)

@bp.route('/generate_pdf/<int:projeto_id>')
def generate_pdf(projeto_id):
    return generate_pdf_report(projeto_id)

   
@bp.route('/download_pdf/<path:pdf_path>')
def download_pdf(pdf_path):
    return send_file(pdf_path, as_attachment=True)

@bp.route('/update/<int:projeto_id>', methods=['GET', 'POST'])
def update(projeto_id):
    projeto = Projeto.query.get_or_404(projeto_id)

    if request.method == 'POST':
        projeto.nome_projeto = request.form['nome_projeto']
        projeto.data_relatorio = datetime.strptime(request.form['data_relatorio'], '%Y-%m-%d')
        projeto.gerente_projeto = request.form['gerente_projeto']
        projeto.equipe_envolvida = request.form['equipe_envolvida']
        projeto.status_geral = request.form['status_geral']
        projeto.resumo_status = request.form['resumo_status']
        projeto.principais_conquistas = request.form['principais_conquistas']
        projeto.proximos_passos = request.form['proximos_passos']
        projeto.solicitacoes = request.form['solicitacoes']
        projeto.dependencias = request.form['dependencias']
        projeto.notas_adicionais = request.form['notas_adicionais']
        projeto.order_number = request.form['order_number']
        projeto.project_status = request.form['estado_projeto']

        # Atualizar tarefas
        Tarefa.query.filter_by(projeto_id=projeto.id).delete()
        tarefas = request.form.getlist('tarefas[]')
        responsaveis = request.form.getlist('responsaveis[]')
        status_tarefas = request.form.getlist('status_tarefas[]')
        datas_inicio = [datetime.strptime(date, '%Y-%m-%d') for date in request.form.getlist('datas_inicio[]')]
        datas_termino = [datetime.strptime(date, '%Y-%m-%d') for date in request.form.getlist('datas_termino[]')]
        datas_entrega_inicio = [datetime.strptime(date, '%Y-%m-%d') for date in request.form.getlist('datas_entrega_inicio[]')]
        datas_entrega_fim = [datetime.strptime(date, '%Y-%m-%d') for date in request.form.getlist('datas_entrega_fim[]')]
        observacoes = request.form.getlist('observacoes[]')

        # Verificar se pelo menos uma tarefa foi informada
        if not tarefas:
            flash("Por favor, adicione pelo menos uma tarefa.")
            return redirect(url_for('main.update'))
        
        for i in range(len(tarefas)):
            nova_tarefa = Tarefa(
                projeto_id=projeto.id,
                tarefa=tarefas[i],
                responsavel=responsaveis[i],
                status=status_tarefas[i],
                data_inicio=datas_inicio[i],
                data_termino=datas_termino[i],
                observacoes=observacoes[i]
            )
            db.session.add(nova_tarefa)
            db.session.flush()  # Necessário para obter o id da tarefa novamente

            nova_entrega = EntregaTarefa(
                tarefa_id=nova_tarefa.id,
                data_entrega_inicio=datas_entrega_inicio[i],
                data_entrega_fim=datas_entrega_fim[i]
            )
            db.session.add(nova_entrega)
                
        # Atualizar problemas
        Problema.query.filter_by(projeto_id=projeto.id).delete()
        tipos = request.form.getlist('tipos[]')
        problemas = request.form.getlist('problemas[]')
        impactos = request.form.getlist('impactos[]')
        acoes_corretivas = request.form.getlist('acoes_corretivas[]')
        agentes_solucao = request.form.getlist('agentes_solucao[]')
        datas_alvo_solucao = [datetime.strptime(date, '%Y-%m-%d') for date in request.form.getlist('datas_alvo_solucao[]')]
        coordenadores_agente_solucao = request.form.getlist('coordenadores_agente_solucao[]')
        status_problemas = request.form.getlist('status_problemas[]')

        for i in range(len(tipos)):
            problema_existente = Problema.query.filter_by(projeto_id=projeto.id, problema_risco=problemas[i]).first()
            if problema_existente:
                if problema_existente.status != status_problemas[i]:
                    if problema_existente.tipo == 'Problema' and 'resolvida' not in status_problemas[i].lower():
                        dias_uteis = calcular_dias_uteis(problema_existente.data_abertura, datetime.now().date())
                        problema_existente.dias_abertos += dias_uteis
                    elif 'resolvida' in status_problemas[i].lower():
                        problema_existente.data_resolucao = datas_alvo_solucao[i]  # Atualiza a data de resolução com a data alvo
                        problema_existente.dias_abertos = calcular_dias_uteis(problema_existente.data_abertura, problema_existente.data_resolucao)
                        problema_existente.dias_abertos = abs(dias_uteis)  # Usa o valor absoluto para evitar negativos
                else:
                    # Enviar mensagem informando que o status não foi alterado
                    flash(f"O status do problema '{problemas[i]}' não foi alterado.")
            else:
                novo_problema = Problema(
                    projeto_id=projeto.id,
                    tipo=tipos[i],
                    problema_risco=problemas[i],
                    impacto=impactos[i],
                    acao_corretiva=acoes_corretivas[i],
                    agente_solucao=agentes_solucao[i],
                    data_alvo_solucao=datas_alvo_solucao[i],
                    coordenador_agente_solucao=coordenadores_agente_solucao[i],
                    status=status_problemas[i],
                    data_abertura=datetime.now().date()
                )
                
                db.session.add(novo_problema)

        # Atualizar superintendências, se houver
        ProjetoSuperintendencia.query.filter_by(projeto_id=projeto.id).delete()
        superintendencias_ids = request.form.getlist('superintendencias[]')
        if superintendencias_ids:
            for superintendencia_id in superintendencias_ids:
                projeto_superintendencia = ProjetoSuperintendencia(
                    projeto_id=projeto.id,
                    superintendencia_id=superintendencia_id
                )
                db.session.add(projeto_superintendencia)

        # Atualizar key users, se houver
        ProjetoKeyUser.query.filter_by(projeto_id=projeto.id).delete()
        key_users_ids = request.form.getlist('key_users[]')
        if key_users_ids:
            for key_user_id in key_users_ids:
                projeto_key_user = ProjetoKeyUser(
                    projeto_id=projeto.id,
                    funcionario_id=key_user_id
                )
                db.session.add(projeto_key_user)

        # Atualizar funcionários de TI
        ProjetoFuncTI.query.filter_by(projeto_id=projeto.id).delete()
        funcionarios_ti_ids = request.form.getlist('funcionarios_ti[]')
        if funcionarios_ti_ids:
            for funcionario_ti_id in funcionarios_ti_ids:
                projeto_func_ti = ProjetoFuncTI(
                    projeto_id=projeto.id,
                    funcionario_id=funcionario_ti_id
                )
                db.session.add(projeto_func_ti)

        db.session.commit()
        flash("Projeto atualizado com sucesso!")
        # Redirecionar para a index mantendo o estado do checkbox
        show_completed = 'on' if request.form.get('show_completed') else 'off'
        return redirect(url_for('main.view_report', projeto_id=projeto.id))
    
    # Verificar se o checkbox para mostrar tarefas concluídas foi marcado
    show_completed = request.args.get('show_completed', 'off') == 'on'

    if show_completed:
        tarefas = Tarefa.query.filter_by(projeto_id=projeto.id).order_by(Tarefa.data_inicio).all()
    else:
        tarefas = Tarefa.query.filter_by(projeto_id=projeto.id).filter(Tarefa.status != 'Concluída').order_by(Tarefa.data_inicio).all()

    # Preparar tarefas e entregas
    tarefas_e_entregas = []
    for tarefa in tarefas:
        entrega = EntregaTarefa.query.filter_by(tarefa_id=tarefa.id).order_by(EntregaTarefa.id.desc()).first()
        tarefas_e_entregas.append({
            'tarefa': tarefa,
            'entrega_tarefa': entrega
        })

    problemas = Problema.query.filter_by(projeto_id=projeto.id).all()
    superintendencias = Superintendentes.query.all()
    funcionarios = Funcionarios.query.filter(Funcionarios.tipo_funcionario=='GEN').order_by(Funcionarios.nome).all()
    funcionarios_ti = Funcionarios.query.filter(Funcionarios.tipo_funcionario=='TEC').order_by(Funcionarios.nome).all()


    # Obter superintendências e key users associados ao projeto
    projeto_superintendencias = ProjetoSuperintendencia.query.filter_by(projeto_id=projeto.id).all()
    projeto_key_users = ProjetoKeyUser.query.filter_by(projeto_id=projeto.id).all()
    projeto_funcionarios_ti = ProjetoFuncTI.query.filter_by(projeto_id=projeto.id).all()

    
    superintendencias_ids = [ps.superintendencia_id for ps in projeto_superintendencias]
    key_users_ids = [ku.funcionario_id for ku in projeto_key_users]
    funcionarios_ti_ids = [pfti.funcionario_id for pfti in projeto_funcionarios_ti]


    # Obter funcionários de TI associados ao projeto
    projeto_funcionarios_ti = ProjetoFuncTI.query.filter_by(projeto_id=projeto.id).all()
    funcionarios_ti_ids = [pfti.funcionario_id for pfti in projeto_funcionarios_ti]

    funcionarios_ti = Funcionarios.query.filter(Funcionarios.tipo_funcionario=='TEC').order_by(Funcionarios.nome).all()

    return render_template('update.html', 
                           projeto=projeto, 
                           tarefas_e_entregas=tarefas_e_entregas, 
                           problemas=problemas, 
                           superintendencias=superintendencias, 
                           funcionarios=funcionarios, 
                           funcionarios_ti=funcionarios_ti,
                           superintendencias_ids=superintendencias_ids, 
                           key_users_ids=key_users_ids,
                           funcionarios_ti_ids=funcionarios_ti_ids,
                           show_completed=show_completed)

@bp.route('/check_jira/<int:projeto_id>')
def check_jira(projeto_id):
    return check_jira_issue(projeto_id)

@bp.route('/upload_pdf_to_jira/<int:projeto_id>')
def upload_pdf_to_jira_route(projeto_id):
    return upload_pdf_to_jira(projeto_id)
