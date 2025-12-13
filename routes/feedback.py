from flask import Blueprint, render_template, request, redirect, url_for
from models import db, Feedback

feedback_bp = Blueprint('feedback', __name__, url_prefix='/feedback')

@feedback_bp.route('/')
def list_feedback():
    feedbacks = Feedback.query.all()
    return render_template('feedback/list.html', feedbacks=feedbacks)

@feedback_bp.route('/add', methods=['GET', 'POST'])
def add_feedback():
    if request.method == 'POST':
        name = request.form['name']
        message = request.form['message']
        fb = Feedback(name=name, message=message)
        db.session.add(fb)
        db.session.commit()
        return redirect(url_for('feedback.list_feedback'))
    return render_template('feedback/add.html')

@feedback_bp.route('/delete/<int:id>')
def delete_feedback(id):
    fb = Feedback.query.get_or_404(id)
    db.session.delete(fb)
    db.session.commit()
    return redirect(url_for('feedback.list_feedback'))
