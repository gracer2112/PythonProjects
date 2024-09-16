from flask import Blueprint, render_template, request, redirect, url_for
from models import db, Superintendente

superintendentes_bp = Blueprint('superintendentes_bp', __name__)

@superintendentes_bp.route('/list')
def list_superintendentes():
    superintendentes = Superintendente.query.all()
    return render_template('superintendentes.html', superintendentes=superintendentes)

@superintendentes_bp.route('/add', methods=['GET', 'POST'])
@superintendentes_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
def manage_superintendente(id=None):
    if id:
        superintendente = Superintendente.query.get_or_404(id)
    else:
        superintendente = Superintendente()

    if request.method == 'POST':
        superintendente.Superintendencia = request.form['superintendencia']
        superintendente.NomeSuperintendente = request.form['nomeSuperintendente']
        superintendente.EmailSuperintendente = request.form['emailSuperintendente']

        if not id:
            db.session.add(superintendente)
        db.session.commit()
        return redirect(url_for('superintendentes_bp.list_superintendentes'))

    return render_template('manage_superintendente.html', superintendente=superintendente)

@superintendentes_bp.route('/delete/<int:id>', methods=['POST'])
def delete_superintendente(id):
    superintendente = Superintendente.query.get_or_404(id)
    db.session.delete(superintendente)
    db.session.commit()
    return redirect(url_for('superintendentes_bp.list_superintendentes'))