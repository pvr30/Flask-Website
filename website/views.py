from datetime import date
from flask import Blueprint, render_template, request, flash, jsonify, redirect
from flask_login import login_required, current_user
from sqlalchemy.sql.functions import user
from .models import Note
from . import db
import json

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        note = request.form.get('note')
        if len(note) < 1:
            flash('Note Is Too Short!', category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note Was Added Successfully', category='success')
    return render_template('home.html', user=current_user)



@views.route('/delete_note/<int:id>', methods=['POST'])
def delete_note(id):
    if request.method == 'POST':
        note = Note.query.get(id)
        print(note)
        db.session.delete(note)
        db.session.commit()
    return redirect('/')