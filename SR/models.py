from extensions import db
import pytz
from datetime import datetime

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

    # Relações
    tarefas = db.relationship('Tarefa', backref='projeto', lazy=True)
    problemas = db.relationship('Problema', backref='projeto', lazy=True)
    superintendencias = db.relationship('ProjetoSuperintendencia', backref='projeto', lazy=True)
    key_users = db.relationship('ProjetoKeyUser', backref='projeto', lazy=True)

    def __repr__(self):
        return f'<Projeto {self.id}>'

class Tarefa(db.Model):
    __tablename__ = 'tarefa'
    id = db.Column(db.Integer, primary_key=True)
    projeto_id = db.Column(db.Integer, db.ForeignKey('projeto.id'), nullable=False)
    tarefa = db.Column(db.String(200), nullable=False)
    responsavel = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(50), nullable=False)
    data_inicio = db.Column(db.Date, nullable=False)
    data_termino = db.Column(db.Date, nullable=False)
    observacoes = db.Column(db.String(200), nullable=False)

    entregas = db.relationship('EntregaTarefa', backref='tarefa', lazy=True)

    def __repr__(self):
        return f'<Tarefa {self.id}>'
    
class EntregaTarefa(db.Model):
    __tablename__ = 'entrega_tarefa'
    id = db.Column(db.Integer, primary_key=True)
    tarefa_id = db.Column(db.Integer, db.ForeignKey('tarefa.id'), nullable=False)
    data_entrega_inicio = db.Column(db.Date, nullable=False)
    data_entrega_fim = db.Column(db.Date, nullable=False)
    last_updated = db.Column(db.DateTime, default=datetime.now(tz=pytz.utc), onupdate=datetime.now(tz=pytz.utc)) 

    def __repr__(self):
        return f'<EntregaTarefa {self.id}>'

class Problema(db.Model):
    __tablename__ = 'problema'
    id = db.Column(db.Integer, primary_key=True)
    projeto_id = db.Column(db.Integer, db.ForeignKey('projeto.id'), nullable=False)
    tipo = db.Column(db.String(50), nullable=False)
    problema_risco = db.Column(db.String(200), nullable=False)
    impacto = db.Column(db.String(200), nullable=False)
    acao_corretiva = db.Column(db.String(200), nullable=False)
    agente_solucao = db.Column(db.String(100), nullable=False)
    data_alvo_solucao = db.Column(db.Date, nullable=False)
    coordenador_agente_solucao = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(50), nullable=False)
    data_abertura = db.Column(db.Date, default=datetime.now, nullable=False)
    dias_abertos = db.Column(db.Integer, default=0, nullable=False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if self.tipo == 'Problema' and not self.data_abertura:
            self.data_abertura = datetime.now().date()
                
    def __repr__(self):
        return f'<Problema {self.id}>'
    
class Superintendentes(db.Model):
    __tablename__ = 'superintendentes'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    superintendencia = db.Column(db.String, unique=True, nullable=False)
    nomesuperintendente = db.Column(db.String, nullable=False)
    emailsuperintendente = db.Column(db.String, nullable=False)
    # Relação
    funcionarios = db.relationship('Funcionarios', backref='superintendentes', lazy=True)

    def __repr__(self):
        return f'<Superintendentes {self.id}>'

class Funcionarios(db.Model):
    __tablename__ = 'funcionarios'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    idsuperintendente = db.Column(db.Integer, db.ForeignKey('superintendentes.id'), nullable=False)
    nome = db.Column(db.String, nullable=False)
    cargo = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    tipo_funcionario = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f'<Funcionarios {self.id}>'
    
class ProjetoSuperintendencia(db.Model):
    __tablename__ = 'projeto_superintendencia'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    projeto_id = db.Column(db.Integer, db.ForeignKey('projeto.id'), nullable=False)
    superintendencia_id = db.Column(db.Integer, db.ForeignKey('superintendentes.id'), nullable=False)

    def __repr__(self):
        return f'<ProjetoSuperintendencia {self.id}>'
                                               
class ProjetoKeyUser(db.Model):
    __tablename__ = 'projeto_key_user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    projeto_id = db.Column(db.Integer, db.ForeignKey('projeto.id'), nullable=False)
    funcionario_id = db.Column(db.Integer, db.ForeignKey('funcionarios.id'), nullable=False)
    def __repr__(self):
        return f'<ProjetoKeyUser {self.id}>'
    
class Funcionario_TI(db.Model):
    __tablename__ = 'func_tecnologia'
    ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    IDSuperintendente = db.Column(db.Integer, db.ForeignKey('superintendentes.id'), nullable=False)
    Nome = db.Column(db.String(100), nullable=False)
    Cargo = db.Column(db.String(100), nullable=False)
    Email = db.Column(db.String(100), nullable=False)

    superintendente = db.relationship('Superintendentes', backref=db.backref('func_tecnologia', lazy=True))
    def __repr__(self):
        return f'<Funcionario TI {self.ID} - {self.Nome}>'
    
class ProjetoFuncTI(db.Model):
    __tablename__ = 'projetofuncTI'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    projeto_id = db.Column(db.Integer, db.ForeignKey('projeto.id'), nullable=False)
    funcionario_id = db.Column(db.Integer, db.ForeignKey('funcionarios.id'), nullable=False)
    def __repr__(self):
        return f'<ProjetoFuncTI {self.id}>'