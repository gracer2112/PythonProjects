from flask import abort, Flask, render_template, jsonify, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

import json
import os
from io import BytesIO

# Importar os modelos
from models import db, Project, Activity, Superintendente, Funcionario

# Definir o caminho absoluto para a pasta de templates
template_dir = os.path.abspath(r'C:\Users\erica.araujo\OneDrive - 200DEV\Documentos\PythonProjects\PI\templates')
app = Flask(__name__, template_folder=template_dir)

# Definindo uma chave secreta segura
app.secret_key = os.urandom(24)

# Configuração do banco de dados
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:/Users/erica.araujo/OneDrive - 200DEV/Documentos/PythonProjects/database/projetos.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicialização do banco de dados com o aplicativo Flask
db.init_app(app)

# Importar as rotas de projetos
from project_routes import project_bp
from activity_routes import activity_bp
from superintendentes_routes import superintendentes_bp
from funcionarios_routes import funcionarios_bp
from funcionarios_TI_routes import funcionarios_TI_bp


# Registrar o blueprint das rotas de projetos
app.register_blueprint(project_bp, url_prefix='/projects')
app.register_blueprint(activity_bp, url_prefix='/activities')
app.register_blueprint(superintendentes_bp, url_prefix='/superintendentes')
app.register_blueprint(funcionarios_bp, url_prefix='/funcionarios')
app.register_blueprint(funcionarios_TI_bp, url_prefix='/funcionarios_TI')


# Criação das tabelas
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search_projects', methods=['GET'])
def search_projects():
    query = request.args.get('query')
    if query:
        projects = Project.query.filter((Project.nome_projeto.contains(query)) | (Project.id.contains(query))).all()
    else:
        projects = Project.query.all()
    return jsonify([{'id': project.id, 'name': project.nome_projeto} for project in projects]) 


if __name__ == '__main__':
    app.run(debug=True, port=5001)