from flask import (
        Blueprint, redirect, render_template,
        Response, request, url_for
)
from flask_login import login_user, login_required, logout_user, current_user
from sqlalchemy.exc import IntegrityError

from project import db
from project.models import User, Subject, Assignment, Lesson

from . import app

import time




@app.route('/')
def index():
		if current_user:
			logout_user()

		return render_template('index.html')

@app.route('/private')
@login_required
def private_route():

	all_subjects = db.session.query(Subject).filter_by(user=current_user.id).all()
	all_assignments = db.session.query(Assignment).filter_by(user=current_user.id).all()
	done_assignments = db.session.query(Assignment).filter_by(user=current_user.id,is_done=True).all()
	not_done_assignments = db.session.query(Assignment).filter_by(user=current_user.id,is_done=False).all()
	absolutely_all_subjects = db.session.query(Subject).all()
	today = time.localtime(time.time())[6]
	lessons_by_day = []
	lessons_by_subjects = []
	numbers = [0,1,2,3,4,5,6]
	for d in range(7):
		l =  db.session.query(Lesson).filter_by(user=current_user.id,day=d).all()

		l.sort(key = lambda x: x.start_time)
		
		lessons_by_day.append(l)

	all_assignments_by_difficulty = all_assignments.copy()
	all_assignments_by_subject = all_assignments.copy()

	all_assignments_by_difficulty.sort(key=lambda x: x.difficulty)
	all_assignments_by_subject.sort(key=lambda x: x.subject)
	done_assignments.sort(key=lambda x: time.mktime(time.struct_time([x.d_year,x.d_month,x.d_date,0,0,0,0,0,0])))
	not_done_assignments.sort(key=lambda x: time.mktime(time.struct_time([x.d_year,x.d_month,x.d_date,0,0,0,0,0,0])))
	all_assignments_by_deadline = not_done_assignments+done_assignments



	return render_template('private.html',
		all_subjects=all_subjects,
		all_assignments=all_assignments,
		all_assignments_by_deadline = all_assignments_by_deadline,
		all_assignments_by_difficulty = all_assignments_by_difficulty,
		all_assignments_by_subject = all_assignments_by_subject,
		absolutely_all_subjects=absolutely_all_subjects,
		lessons_by_day=lessons_by_day,
		today=today,
		numbers=numbers)