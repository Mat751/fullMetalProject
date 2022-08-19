import sys
from db import db
from flask_security import UserMixin, RoleMixin
from datetime import datetime
from sqlalchemy.sql import func
from flask import current_app

roles_users = db.Table('roles_users',
        db.Column('user_id', db.Integer(), db.ForeignKey('users.id')),
        db.Column('role_id', db.Integer(), db.ForeignKey('roles.id')))

class Role(db.Model, RoleMixin):
    __tablename__ = 'roles'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    def __repr__(self):
        return "<Role %r>"%self.name
    
    @staticmethod
    def insert_roles():
        for role_name in "admin user".split():
            if Role.query.filter_by(name=role_name).first() is None:
                role = Role(name = role_name)
                db.session.add(role)
        db.session.commit()


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255), nullable=False)
    surname = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    username = db.Column(db.String(255))
    about = db.Column(db.Text())
    roles = db.relationship('Role', secondary=roles_users, backref=db.backref('users', lazy='dynamic'))
    iscritto = db.relationship('Iscritto',backref = 'users')

    def __repr__(self):
        return "<User %r>"%self.email
    
    @staticmethod
    def insert_admin():
        if User.query.filter_by(email=current_app.config['ADMIN_MAIL']).first() is None:
            user = User(
                first_name = "Matteo",
                surname = "Milani",
                email=current_app.config['ADMIN_MAIL'],
                password=current_app.config['ADMIN_PASSWORD'],
                active=True)
            user.roles.append(Role.query.filter_by(name='admin').first())
            db.session.add(user)
            db.session.commit()

class Iscritto(db.Model):
    __tablename__ = 'iscritti'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(150))
    cognome = db.Column(db.String(150))
    data_nascita = db.Column(db.DateTime(timezone=True))
    codice_fiscale = db.Column(db.String(150))
    data_iscrizione = db.Column(db.DateTime(timezone=True),default=func.now())
    indirizzo = db.Column(db.String(150))
    citta = db.Column(db.String(150))
    cap = db.Column(db.Integer)
    identita = db.Column(db.LargeBinary)
    iscrizione = db.Column(db.LargeBinary)
    identita_caricata = db.Column(db.Boolean)
    iscrizione_caricata = db.Column(db.Boolean)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))