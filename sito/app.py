import os
import sys
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_nav import Nav, register_renderer
from flask_nav.elements import *
from db import db
from dotenv import load_dotenv
from flask_security import Security, SQLAlchemyUserDatastore, current_user
from flask_migrate import Migrate
from utils.dbConnector import dbConnector
from utils.models import User, Role
from bootstrapRenderer import RightRenderer   
from flask_login import LoginManager


load_dotenv()

bootstrap = Bootstrap()
nav = Nav()
security = Security()

def create_app():
    
    app = Flask(__name__,template_folder='templates')
    
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = dbConnector.create_postgres_url('sito')
    app.config['DEBUG'] = True
    app.config['ADMIN_MAIL'] = os.getenv('ADMIN_MAIL')
    app.config['ADMIN_PASSWORD'] = os.getenv('ADMIN_PASSWORD')
    app.config['SECURITY_PASSWORD_SALT'] = 'some arbitrary super secret string'
    
    from blueprint.auth import auth
    app.register_blueprint(auth,url_prefix='/')

    from blueprint.error import error
    app.register_blueprint(error,url_prefix='/')

    from blueprint.views import views
    app.register_blueprint(views,url_prefix='/')
     
    migrate = Migrate(app, db)
    
    register_renderer(app, 'right_rendered', RightRenderer)
    
    @nav.navigation()
    def main_nav():
        navbar = Navbar('Basket')
        navbar.items.append(View('Home', 'views.index'))
        navbar.items.append(View('Iscrizione', 'views.iscrizione'))
        if current_user.is_authenticated:
            usergrp = []
            usergrp.append(current_user.email)
            if current_user.has_role('admin'):
                usergrp.append(View('Admin', 'views.index'))
            usergrp.append(View('Logout', 'security.logout'))
            grp = Subgroup(*usergrp)
            grp.right = True
            navbar.items.append(grp)
        else:
            login_view = View('Login', 'auth.login')
            login_view.right = True
            navbar.items.append(login_view)
        return navbar
    
    bootstrap.init_app(app)
    nav.init_app(app)
    db.init_app(app)

    with app.app_context():
        dbConnector.create_database_if_not_exists('sito')
        dbConnector.run_migration('sito')
        Role.insert_roles()
        User.insert_admin()

    user_datastore = SQLAlchemyUserDatastore(db, User, Role)
    security.init_app(app, user_datastore)

    login_manager = LoginManager()
    login_manager.login_message = "Effettua il login per collegarti a questa pagina."
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    
    return app





if __name__ == '__main__':
    app = create_app()
    app.run(debug=True,host='0.0.0.0')
