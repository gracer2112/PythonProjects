from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from datetime import datetime
from models import db, Activity, Project
from collections import defaultdict

activity_bp = Blueprint('activity_bp', __name__)

# Função para mapear os valores das fases e equipes
def map_values(activity):
    phase_mapping = {
        'pre_go_live': 'Pré Go Live',
        'go_live': 'Go Live',
        'post_go_live': 'Pós Go Live'
    }
    
    team_mapping = {
        'negocio': 'Negócio',
        'ti': 'TI'
    }
    
    activity.phase = phase_mapping.get(activity.phase, activity.phase)
    activity.equipe = team_mapping.get(activity.equipe, activity.equipe)
    return activity


@activity_bp.route('/add', methods=['GET', 'POST'])
def add_activity():
    if request.method == 'POST':
        try:
            phase = request.form['phase']
            activity = request.form['activity']
            responsible = request.form['responsible']
            description = request.form['description']
            start_date = datetime.strptime(request.form['start_date'], '%Y-%m-%d').date()
            end_date = datetime.strptime(request.form['end_date'], '%Y-%m-%d').date()
            start_hour = datetime.strptime(request.form['start_hour'], '%H:%M').time() if request.form['start_hour'] else None
            end_hour = datetime.strptime(request.form['end_hour'], '%H:%M').time() if request.form['end_hour'] else None
            equipe = request.form['equipe']
            observations = request.form['observations']
            project_id = request.form['hidden_project_id']
            seq = request.form['seq']
            
            if not project_id:
                return "Project ID is required", 400
            
            new_activity = Activity(
                phase=phase, activity=activity, responsible=responsible, description=description,
                start_date=start_date, end_date=end_date, start_hour=start_hour, end_hour=end_hour,
                equipe=equipe, observations=observations, project_id=project_id, seq=seq
            )
            db.session.add(new_activity)
            db.session.commit()
            
            return redirect(url_for('activity_bp.listar_atividades'))
        except KeyError as e:
            return f"Missing form field: {e}", 400
    
    projects = Project.query.all()
    next_id = db.session.query(db.func.max(Activity.id)).scalar()
    next_id = next_id + 1 if next_id else 1
    
    return render_template('activity_form.html', action='add', next_id=next_id, projects=projects)

@activity_bp.route('/listar_atividades', methods=['GET', 'POST'])
def listar_atividades():
    project_id = request.args.get('project_id')
    projects = Project.query.all()

    if project_id and project_id != "":
        activities = Activity.query.filter_by(project_id=project_id).order_by(Activity.start_date, Activity.start_hour).all()
    else:
        activities = Activity.query.order_by(Activity.start_date, Activity.start_hour).all()

    # Aplique o mapeamento às atividades
    activities = [map_values(activity) for activity in activities]

    # Organize atividades por projeto
    activities_by_project_phase_and_team = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))
    for activity in activities:
        activities_by_project_phase_and_team[activity.project_id][activity.phase][activity.equipe].append(activity)

    # Atualize o campo seq incrementalmente dentro de cada agrupamento
    for project_id, phases in activities_by_project_phase_and_team.items():
        for phase, teams in phases.items():
            for team, activities in teams.items():
                activities.sort(key=lambda x: (x.start_date, x.start_hour))
                for i, activity in enumerate(activities, start=1):
                    activity.seq = i
                    db.session.add(activity)  # Adicione a atividade à sessão para atualizar no banco de dados

    db.session.commit()  # Commit as alterações no banco de dados
                    
    # Filtre apenas projetos que têm atividades
    projects_with_activities = Project.query.filter(Project.id.in_(activities_by_project_phase_and_team.keys())).all()

    return render_template('activity_form.html', action='list', activities_by_project_phase_and_team=activities_by_project_phase_and_team, projects=projects_with_activities)

@activity_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_activity(id):
    activity = Activity.query.get_or_404(id)
    projects = Project.query.all()  

    if request.method == 'POST':
        activity.phase = request.form['phase']
        activity.activity = request.form['activity']
        activity.responsible = request.form['responsible']
        activity.description = request.form['description']
        activity.start_date = datetime.strptime(request.form['start_date'], '%Y-%m-%d').date()
        activity.end_date = datetime.strptime(request.form['end_date'], '%Y-%m-%d').date()
        
        start_hour = request.form['start_hour']
        end_hour = request.form['end_hour']

        # if not project_id:
        #  return "Project ID is required", 400
                
        if start_hour:
            activity.start_hour = datetime.strptime(start_hour, '%H:%M').time()
        else:
            activity.start_hour = None
        
        if end_hour:
            activity.end_hour = datetime.strptime(end_hour, '%H:%M').time()
        else:
            activity.end_hour = None
        
        activity.equipe = request.form['equipe']
        activity.observations = request.form['observations']
        activity.project_id = request.form['project_id']
        activity.seq = request.form['seq']
        
        db.session.commit()
        return redirect(url_for('activity_bp.listar_atividades'))
    
    return render_template('activity_form.html', action='edit', activity=activity, projects=projects)

@activity_bp.route('/delete/<int:id>', methods=['POST'])
def delete_activity(id):
    activity = Activity.query.get_or_404(id)
    db.session.delete(activity)
    db.session.commit()
    return redirect(url_for('activity_bp.list_activities'))

@activity_bp.route('/search_projects')
def search_projects():
    query = request.args.get('query', '')
    projects = Project.query.filter(
        (Project.nome_projeto.ilike(f'%{query}%')) | 
        (Project.id.ilike(f'%{query}%'))
    ).all()
    projects_list = [{'id': project.id, 'name': project.nome_projeto} for project in projects]
    return jsonify(projects_list)