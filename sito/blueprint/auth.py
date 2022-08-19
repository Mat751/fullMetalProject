from utils.models import Role, User
from flask import Blueprint, render_template, request, flash, redirect, url_for, Markup
from utils.passwordChecker import password_check
from werkzeug.security import generate_password_hash, check_password_hash
from db import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash(Markup("<h1>Login effettuato!</h1>"))
                login_user(user,remember=True)
                return redirect(url_for('views.index'))
            else:
                flash(Markup("<h1>Password non corretta</h1>"))
        else:
            flash(Markup("<h1>Non sei registrato! Effettua prima la registrazione.</h1>"))

    return render_template("login.html", user=current_user)

@auth.route('/registrazione',methods=['GET','POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        name = request.form.get('nome')
        surname = request.form.get('cognome')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        if user:
            flash("L'utente si è già registrato.", category='error')
        elif len(email) < 4:
            flash("Email deve essere più lunga di 4 caratteri.", category='error')
        elif len(name) < 2:
            flash("Nome non corretto.",category='error')
        elif not password_check(password1)['password_ok']:
            flash("""La password deve essere lunga almeno 8 caratteri. 
                   Avere almeno 1 cifra, 
                   1 simbolo, 
                   1 lettera maiuscola e 1 minuscola.""",category='error')
        elif password1 != password2:
            flash("La prima e la seconda password non coincidono.",category='error')
        else:
            new_user = User(email=email,first_name=name,surname=surname,
                            password=generate_password_hash(password1,method='sha256'))
            new_user.roles.append(Role.query.filter_by(name='user').first())
            new_user.active = True
            db.session.add(new_user)
            db.session.commit()
            flash('Account creato!')
            return redirect(url_for('views.index'))
        

    return render_template("registrazione.html", user=current_user)