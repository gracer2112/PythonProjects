from flask import Blueprint, render_template, request, redirect, url_for
from models import db, Funcionario, Superintendente

funcionarios_TI_bp = Blueprint('funcionarios_TI_bp', __name__)

@funcionarios_TI_bp.route('/list')
def list_funcionarios_TI():
    func_tecnologia =  Funcionario.query.filter(Funcionario.Tipo_Funcionario=='TEC').order_by(Funcionario.Nome).all()
    superintendentes = Superintendente.query.all()
    return render_template('func_TI.html', func_tecnologia=func_tecnologia, superintendentes=superintendentes)

@funcionarios_TI_bp.route('/add', methods=['GET', 'POST'])
@funcionarios_TI_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
def manage_funcionario_TI(id=None):
    if id:
        func_tecnologia = Funcionario.query.get_or_404(id)
    else:
        func_tecnologia = Funcionario()

    superintendentes = Superintendente.query.all()

    if request.method == 'POST':
        func_tecnologia.IDSuperintendente = request.form['idSuperintendente']
        func_tecnologia.Nome = request.form['nomeFuncionario']
        func_tecnologia.Cargo = request.form['cargoFuncionario']
        func_tecnologia.Email = request.form['emailFuncionario']
        func_tecnologia.Tipo_Funcionario = 'TEC'

        if not id:
            db.session.add(func_tecnologia)
        db.session.commit()
        return redirect(url_for('funcionarios_TI_bp.list_funcionarios_TI'))

    return render_template('manage_funcionario_TI.html', func_tecnologia=func_tecnologia, superintendentes=superintendentes)

@funcionarios_TI_bp.route('/delete/<int:id>', methods=['POST'])
def delete_funcionario_TI(id):
    func_tecnologia = Funcionario.query.get_or_404(id)
    db.session.delete(func_tecnologia)
    db.session.commit()
    return redirect(url_for('funcionarios_TI_bp.list_funcionarios_TI'))