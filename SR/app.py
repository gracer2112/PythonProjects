from flask import Flask,Blueprint
import os
from extensions import db
from models import db, Projeto, Tarefa, Problema
from config import Config

def create_app():
    app = Flask(__name__, template_folder=Config.TEMPLATE_FOLDER)
    app.config.from_object(Config)

    # Definindo uma chave secreta segura
    app.secret_key = os.urandom(24)    
    
    # Certifique-se de que o diretório 'instance' existe
    if not os.path.exists(os.path.join(Config.BASE_DIR, 'instance')):
        os.makedirs(os.path.join(Config.BASE_DIR, 'instance'))

    db.init_app(app)
    
    with app.app_context():
        db.create_all()
    
    from routes import bp as main_bp
    app.register_blueprint(main_bp)
    
    return app

# Criação do blueprint para a aplicação de Status Report
status_report_bp = Blueprint('status_report', __name__, template_folder=Config.TEMPLATE_FOLDER)

@status_report_bp.route('/status_report')
def status_report():
    return "Status Report Page"

app = create_app() 

if __name__ == '__main__':
    app.run(debug=False,  port=5003)