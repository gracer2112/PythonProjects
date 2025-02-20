# importar as configurações apropriadas
import sys
from datetime import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError
from config import Config  # Importar as configurações diretamente

app = Flask(__name__)
app.config.from_object(Config)  # Usar as configurações da classe Config

db = SQLAlchemy(app)

# Assumindo suas definições de modelo
class Tarefa(db.Model):
    __tablename__ = 'tarefa'

    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(50))
    data_inicio = db.Column(db.Date)
    data_termino = db.Column(db.Date)

class EntregaTarefa(db.Model):
    __tablename__ = 'entrega_tarefa'

    id = db.Column(db.Integer, primary_key=True)
    tarefa_id = db.Column(db.Integer, db.ForeignKey('tarefa.id'))
    data_entrega_inicio = db.Column(db.Date)
    data_entrega_fim = db.Column(db.Date)

def copiar_datas_entrega():
    with app.app_context():  # Entrando explicitamente no contexto da aplicação

        try:
            # Iniciar a sessão
            with app.app_context():
                # Localizar todas as tarefas concluídas que não possuem entrega
                tarefas_concluidas = Tarefa.query.all()

                for tarefa in tarefas_concluidas:
                    # Verificar se já existe uma entrada na EntregaTarefa
                    entrega_existente = EntregaTarefa.query.filter_by(tarefa_id=tarefa.id).first()

                    if not entrega_existente:
                        if tarefa.status == 'Concluída':
                            data_inicio = tarefa.data_inicio
                            data_fim = tarefa.data_termino
                        else:
                            data_inicio = tarefa.data_inicio
                            data_fim = tarefa.data_inicio  # Usa data de início para não-concluídas

                    if not entrega_existente:
                        # Se não houver, criar uma
                        nova_entrega = EntregaTarefa(
                            tarefa_id=tarefa.id,
                            data_entrega_inicio=data_inicio,
                            data_entrega_fim=data_fim
                        )
                        db.session.add(nova_entrega)

                # Commit para persistir alterações no banco de dados
                db.session.commit()
                print("Datas de entrega copiadas com sucesso para tarefas concluídas.")

        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"Erro ao copiar datas de entrega: {str(e)}", file=sys.stderr)

        finally:
            # Fechar a sessão
            db.session.close()

if __name__ == '__main__':
    copiar_datas_entrega()