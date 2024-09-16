# config.py
import os

class Config:
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'supersecretkey'
    #SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'instance', 'projetos.db')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///C:/Users/erica.araujo/OneDrive - 200DEV/Documentos/PythonProjects/database/projetos.db'     
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TEMPLATE_FOLDER = os.path.abspath(r'C:\Users\erica.araujo\OneDrive - 200DEV\Documentos\PythonProjects\SR\templates')