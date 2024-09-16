# config.py
import os
import logging

class Config:
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'supersecretkey'
    #SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'instance', 'projetos.db')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///C:/Users/erica.araujo/OneDrive - 200DEV/Documentos/PythonProjects/database/projetos.db'     
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TEMPLATE_FOLDER = os.path.abspath(r'C:\Users\erica.araujo\OneDrive - 200DEV\Documentos\PythonProjects\PT\templates')

    # Para ativar o log coloque na linha de comando set ENABLE_LOGGING=true
    # Variável para controlar o logging
    ENABLE_LOGGING = os.environ.get('ENABLE_LOGGING', 'true').lower() == 'true'

    @staticmethod
    def init_logging():
        if Config.ENABLE_LOGGING:
            logging.basicConfig(
                level=logging.INFO,
                format='%(asctime)s - %(levelname)s - %(message)s',
                handlers=[
                    logging.FileHandler("app.log"),
                    logging.StreamHandler()
                ]
            )

# Inicializa o logging se habilitado
Config.init_logging()