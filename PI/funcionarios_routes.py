from flask import Blueprint, render_template, request, redirect, url_for
from models import db, Funcionario, Superintendente

funcionarios_bp = Blueprint('funcionarios_bp', __name__)

@funcionarios_bp.route('/list')
def list_funcionarios():
    funcionarios =  Funcionario.query.filter(Funcionario.Tipo_Funcionario == 'GEN').order_by(Funcionario.Nome).all()
    superintendentes = Superintendente.query.all()
    return render_template('funcionarios.html', funcionarios=funcionarios, superintendentes=superintendentes)

@funcionarios_bp.route('/add', methods=['GET', 'POST'])
@funcionarios_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
def manage_funcionario(id=None):
    if id:
        funcionario = Funcionario.query.get_or_404(id)
    else:
        funcionario = Funcionario()

    superintendentes = Superintendente.query.all()

    if request.method == 'POST':
        funcionario.IDSuperintendente = request.form['idSuperintendente']
        funcionario.Nome = request.form['nomeFuncionario']
        funcionario.Cargo = request.form['cargoFuncionario']
        funcionario.Email = request.form['emailFuncionario']
        funcionario.Tipo_Funcionario = 'GEN'

        if not id:
            db.session.add(funcionario)
        db.session.commit()
        return redirect(url_for('funcionarios_bp.list_funcionarios'))

    return render_template('manage_funcionario.html', funcionario=funcionario, superintendentes=superintendentes)

@funcionarios_bp.route('/delete/<int:id>', methods=['POST'])
def delete_funcionario(id):
    funcionario = Funcionario.query.get_or_404(id)
    db.session.delete(funcionario)
    db.session.commit()
    return redirect(url_for('funcionarios_bp.list_funcionarios'))