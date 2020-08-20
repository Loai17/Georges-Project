from flask import (
        Blueprint, redirect, render_template,
        Response, request, url_for
)
from flask_login import login_user, login_required, logout_user, current_user
from sqlalchemy.exc import IntegrityError

from project import db
from project.models import User, Subject, Assignment, Lesson


users_bp = Blueprint('users', __name__)

@users_bp.route('/add_lessons_by_day', methods=['GET','POST'])
@login_required
def add_lessons_by_day():
    if request.method == "POST":
        form = request.form

        param = ['subject','start_time','end_time','day_of_the_week']

        number_of_lessons = int((len(form)-2)/4)
        number_of_old_lessons = len(db.session.query(Lesson).filter_by(user=current_user.id).all())

        old_lessons = db.session.query(Lesson).filter_by(user=current_user.id).all()

        number_of_new_lessons = int(form.get('number_of_new'))

        for o in old_lessons:
            o.subject = form.get(param[0]+str(o.id))
            o.day = form.get(param[3]+str(o.id))
            st = form.get(param[1]+str(o.id))
            o.start_time = (int(st.split(':')[0])*3600)+(int(st.split(':')[1])*60)
            et = form.get(param[2]+str(o.id))
            o.end_time = (int(et.split(':')[0])*3600)+(int(et.split(':')[1])*60)


        n = 1
        c = 0

        while c < number_of_new_lessons:
            if ('new_'+param[0]+str(n)) in form:
                l = Lesson()
                l.user = current_user.id
                l.day = form.get('new_day_of_the_week'+str(n))
                st = form.get('new_start_time'+str(n))
                l.start_time = (int(st.split(':')[0])*3600)+(int(st.split(':')[1])*60)
                et = form.get('new_end_time'+str(n))
                l.end_time = (int(et.split(':')[0])*3600)+(int(et.split(':')[1])*60)
                l.subject = form.get('new_subject'+str(n))

                db.session.add(l)
            

                c += 1
            n+=1

        db.session.commit()

            

        return redirect(url_for('private_route'))



@users_bp.route('/add_subject', methods=['GET','POST'])
@login_required
def add_subject():
    if request.method == "POST":
        form = request.form

        s = Subject()
        s.user = current_user.id
        s.subject = form.get('name')
        s.color = form.get('color')

        db.session.add(s)
        db.session.commit()

    return redirect(url_for('private_route'))

@users_bp.route('/add_assignment', methods=['GET','POST'])
@login_required
def add_assignment():
    if request.method == "POST":
        form = request.form

        deadline = str(form.get('deadline'))

        a = Assignment()

        a.user = current_user.id
        a.subject = form.get('subject')
        a.title = form.get('title') 
        a.description = form.get('description')
        a.d_date = int(deadline[8:])
        a.d_month = int(deadline[5:7])
        a.d_year = int(deadline[0:4])
        a.difficulty = form.get('difficulty')
        a.is_done = False

        db.session.add(a)
        db.session.commit()
    return redirect(url_for('private_route'))

@users_bp.route('/delete_assignment/<int:assignment_id>',methods=['GET','POST'])
@login_required
def remove_assignment(assignment_id):

    a = db.session.query(Assignment).filter_by(id=assignment_id).first()

    db.session.delete(a)
    db.session.commit()

    return redirect(url_for('private_route'))

@users_bp.route('/delete_lesson/<int:lesson_id>',methods=['GET','POST'])
@login_required
def remove_lesson(lesson_id):

    l = db.session.query(Lesson).filter_by(id=lesson_id).first()

    db.session.delete(l)
    db.session.commit()

    return redirect(url_for('private_route'))

@users_bp.route('/mark_assignment/<int:assignment_id>',methods=['GET','POST'])
@login_required
def mark_assignment(assignment_id):

    a = db.session.query(Assignment).filter_by(id=assignment_id).first()
    a.is_done = True;

    db.session.commit() 

    return redirect(url_for('private_route'))  

@users_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        form = request.form

        name = request.form.get('name')
        username = form.get('username')
        password = form.get('password')
        confirm = form.get('confirm')

        if password == confirm:
            u = User(username,password)
            u.name = name
            u.is_activated = True

            db.session.add(u)
            db.session.commit()
            return redirect(url_for('index'))
        else:
            return Response("Passwords don't match")
    else:
        return redirect(url_for('index'))

    #return render_template('register.html')
                

@users_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        form = request.form

        email = form.get('username')
        password = form.get('password')

        u = db.session.query(User).filter_by(username = email).first()

        if u:
            if u.check_password(password) and u.is_activated:
                login_user(u, remember = True)

                return redirect(url_for('private_route'))
        
    return redirect(url_for('index'))

@users_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))
