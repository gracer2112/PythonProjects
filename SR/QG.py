from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Funcionarios, Funcionario_TI

engine = create_engine('sqlite:///C:/Users/erica.araujo/OneDrive - 200DEV/Documentos/PythonProjects/database/projetos.db')
Session = sessionmaker(bind=engine)
session = Session()

funcionarios_ti = session.query(Funcionario_TI).all()
for func_ti in funcionarios_ti:
    novo_funcionario = Funcionarios(
        idsuperintendente=func_ti.IDSuperintendente,
        nome=func_ti.Nome,
        cargo=func_ti.Cargo,
        email=func_ti.Email,
        tipo_funcionario='TEC'
    )
    session.add(novo_funcionario)
session.commit()