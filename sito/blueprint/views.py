import sys
from flask import Blueprint, render_template, request,flash,redirect, url_for
from flask_login import login_required, current_user
from utils.models import Iscritto
from datetime import datetime as dt
from db import db


views = Blueprint('views', __name__)

@views.route('/')
def index():
    return render_template('index.html')

@views.route('/iscrizione', methods=['GET','POST'])
@login_required
def iscrizione():
    if request.method == 'POST':
        name = request.form.get('nome')
        surname = request.form.get('cognome')
        codice_fiscale = request.form.get('codice_fiscale')
        data_nascita = request.form.get('data_di_nascita')
        data_nascita = dt.strptime(data_nascita,'%Y-%m-%d')
        indirizzo = request.form.get('indirizzo')
        citta = request.form.get('citta')
        cap = request.form.get('cap')
        
        iscritto = Iscritto.query.filter_by(codice_fiscale=codice_fiscale).first()
        if iscritto:
            flash("L'utente si è già iscritto.", category='error')
        elif len(name) < 2:
            flash("Nome non corretto.",category='error')
        elif len(codice_fiscale) != 16:
            flash("Codice fiscale non corretto.",category='error')
        else:
            nuovo_iscritto = Iscritto(nome=name,cognome=surname,
                                      codice_fiscale=codice_fiscale,data_nascita=data_nascita,
                                      indirizzo=indirizzo,citta=citta,cap=cap,
                                      user_id=current_user.get_id(),
                                      iscrizione_caricata = False, identita_caricata = False)

            print(nuovo_iscritto,file=sys.stderr)
            db.session.add(nuovo_iscritto)
            db.session.commit()
            flash('Utente Iscritto')
            return redirect(url_for('views.iscrizione'))
    return render_template("iscrizione.html", result=current_user)

@views.route('/iscrizione_documenti', methods=['GET','POST'])
@login_required
def iscrizione_documenti():
    if request.method == 'POST':
        iscrizione = request.form.get('iscrizione')
        identita = request.form.get('identita')
        
        iscritto = Iscritto.query.filter_by(codice_fiscale=codice_fiscale).first()
        if iscritto == None:
            flash("Compila prima il paragrafo sui dati.", category='error')
        
        elif iscritto.iscrizione_caricata == True:
            flash("Documenti già caricati.", category='error')
        
        else:
            nuovo_iscritto = Iscritto(identita = identita, iscrizione = iscrizione, 
                                      iscrizione_caricata = True, identita_caricata = True)
            db.session.add(nuovo_iscritto)
            db.session.commit()
            flash('Utente Iscritto')
            return redirect(url_for('views.iscrizione'))
    return render_template("iscrizione.html", result=current_user)