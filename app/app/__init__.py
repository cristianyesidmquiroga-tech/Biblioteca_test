from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user
import click
import os

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)    
    app.config.from_object('config.Config')

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    @login_manager.user_loader
    def load_user(idUser):
        from .models.users import User
        return User.query.get(int(idUser))

    from app.routes import auth, book_routes, author_routes, users_route, loans_routes, cloans_routes, computers_routes, room_routes
    app.register_blueprint(auth.bp)
    app.register_blueprint(book_routes.bp)
    app.register_blueprint(author_routes.bp)
    app.register_blueprint(users_route.bp)
    app.register_blueprint(loans_routes.bp)
    app.register_blueprint(cloans_routes.bp)
    app.register_blueprint(computers_routes.bp)
    app.register_blueprint(room_routes.bp)

    @app.before_request
    def exigir_sesion():
        if request.endpoint not in ('auth.login', 'static') and not current_user.is_authenticated:
            return login_manager.unauthorized()

    @app.cli.command('crear-usuario')
    @click.argument('nombre')
    @click.password_option()
    def crear_usuario(nombre, password):
        from .models.users import User
        usuario = User(nameUser=nombre)
        usuario.set_password(password)
        db.session.add(usuario)
        db.session.commit()
        click.echo(f'Usuario {nombre} creado.')
    return app 