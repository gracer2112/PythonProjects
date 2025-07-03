# config.py
import os

class Config:
    BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    #TEMPLATE_FOLDER = os.path.join(BASE_DIR, 'templates')
    DATABASE_DIR = os.path.join(BASE_DIR, 'database')
    # Garante que a pasta existe ao importar a configuração
    if not os.path.exists(DATABASE_DIR):
        os.makedirs(DATABASE_DIR)
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(DATABASE_DIR, 'projetos.db')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
