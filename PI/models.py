from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Project(db.Model):
    __tablename__ = 'projeto'
    id = db.Column(db.Integer, primary_key=True)
    nome_projeto = db.Column(db.String(100), nullable=False)
    data_relatorio = db.Column(db.Date, nullable=False)
    gerente_projeto = db.Column(db.String(100), nullable=False)
    equipe_envolvida = db.Column(db.String(100), nullable=False)
    status_geral = db.Column(db.String(10), nullable=False)
    resumo_status = db.Column(db.Text, nullable=False)
    principais_conquistas = db.Column(db.Text, nullable=False)
    proximos_passos = db.Column(db.Text, nullable=False)
    solicitacoes = db.Column(db.Text, nullable=False)
    dependencias = db.Column(db.Text, nullable=False)
    notas_adicionais = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    order_number = db.Column(db.Integer, nullable=False)
    project_status = db.Column(db.String(100), nullable=False)
    meeting_date = db.Column(db.Date, nullable=False)
    document_version=db.Column(db.String(50), nullable=False)
    id_jira = db.Column(db.String(10), nullable=False)

    activities = db.relationship('Activity', backref='projects', lazy='dynamic')

    def __repr__(self):
        return f'<Projeto {self.id}>'

class Activity(db.Model):
    __tablename__ = 'atividades'
    id = db.Column(db.Integer, primary_key=True)
    phase = db.Column(db.String, nullable=False)
    activity = db.Column(db.String, nullable=False)
    responsible = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    start_hour = db.Column(db.Time)
    end_hour = db.Column(db.Time)
    equipe = db.Column(db.String, nullable=False)
    observations = db.Column(db.String)
    project_id = db.Column(db.Integer, db.ForeignKey('projeto.id'), nullable=False)
    seq = db.Column(db.Integer, nullable=False, default=0)

    def __repr__(self):
        return f'<Activity {self.activity}>'
    
class Superintendente(db.Model):
    __tablename__ = 'superintendentes'
    ID = db.Column(db.Integer, primary_key=True)
    Superintendencia = db.Column(db.String(100), nullable=False)
    NomeSuperintendente = db.Column(db.String(100), nullable=False)
    EmailSuperintendente = db.Column(db.String(100), nullable=False)
    def __repr__(self):
        return f'<Superintendente {self.ID} - {self.NomeSuperintendente}>'

class Funcionario(db.Model):
    __tablename__ = 'funcionarios'
    ID = db.Column(db.Integer, primary_key=True)
    IDSuperintendente = db.Column(db.Integer, db.ForeignKey('superintendentes.ID'), nullable=False)
    Nome = db.Column(db.String(100), nullable=False)
    Cargo = db.Column(db.String(100), nullable=False)
    Email = db.Column(db.String(100), nullable=False)
    Tipo_Funcionario = db.Column(db.String, nullable=False)

    superintendente = db.relationship('Superintendente', backref=db.backref('funcionarios', lazy=True))
    def __repr__(self):
        return f'<Funcionario {self.ID} - {self.Nome}>'
    
class Funcionario_TI(db.Model):
    __tablename__ = 'func_tecnologia'
    ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    IDSuperintendente = db.Column(db.Integer, db.ForeignKey('superintendentes.ID'), nullable=False)
    Nome = db.Column(db.String(100), nullable=False)
    Cargo = db.Column(db.String(100), nullable=False)
    Email = db.Column(db.String(100), nullable=False)

    superintendente = db.relationship('Superintendente', backref=db.backref('func_tecnologia', lazy=True))
    def __repr__(self):
        return f'<Funcionario TI {self.ID} - {self.Nome}>'