from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class TestCase(db.Model):
    __tablename__ = 'test_case'
    id = db.Column(db.Integer, primary_key=True)
    seq = db.Column(db.Integer, nullable=False)
    dependencia = db.Column(db.Integer, nullable=False)
    id_cenario = db.Column(db.Integer, nullable=False)
    modulo = db.Column(db.String(100), nullable=False)
    caso_teste = db.Column(db.String(255), nullable=False)
    info_teste = db.Column(db.Text, nullable=False)
    passos = db.Column(db.Text, nullable=False)
    resultado_esperado = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(50))
    id_responsavel = db.Column(db.String(50))
    id_coordenador = db.Column(db.String(50))
    data_inicio_planejada = db.Column(db.Date)
    data_fim_planejada = db.Column(db.Date)
    data_inicio_realizada = db.Column(db.Date)
    data_fim_realizada = db.Column(db.Date)
    observacao = db.Column(db.Text)
    id_projeto = db.Column(db.Integer)

    id_projeto = db.Column(db.Integer, db.ForeignKey('projeto.id'))
    projeto = db.relationship('Projeto', backref='test_cases')

    def __repr__(self):
        return f'<TestCase {self.id}>'
    
class Funcionarios(db.Model):
    __tablename__ = 'funcionarios'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    idsuperintendente = db.Column(db.Integer, db.ForeignKey('superintendentes.ID'), nullable=False)
    nome = db.Column(db.String, nullable=False)
    cargo = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    tipo_funcionario = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f'<Funcionarios {self.id}>'
    
class Funcionario_TI(db.Model):
    __tablename__ = 'func_tecnologia'
    ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    IDSuperintendente = db.Column(db.Integer, db.ForeignKey('superintendentes.ID'), nullable=False)
    Nome = db.Column(db.String(100), nullable=False)
    Cargo = db.Column(db.String(100), nullable=False)
    Email = db.Column(db.String(100), nullable=False)
    def __repr__(self):
        return f'<Funcionario TI {self.ID} - {self.Nome}>'    
    
class Projeto(db.Model):
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
    id_jira = db.Column(db.String(10), nullable=False)

    def __repr__(self):
        return f'<Projeto {self.id}>'
    
class Superintendente(db.Model):
    __tablename__ = 'superintendentes'
    ID = db.Column(db.Integer, primary_key=True)
    Superintendencia = db.Column(db.String(100), nullable=False)
    NomeSuperintendente = db.Column(db.String(100), nullable=False)
    EmailSuperintendente = db.Column(db.String(100), nullable=False)
    def __repr__(self):
        return f'<Superintendente {self.ID} - {self.NomeSuperintendente}>'