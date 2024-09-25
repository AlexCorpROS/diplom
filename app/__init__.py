from flask import Flask

from .extensions import db, migrate, login_manager
from .config import Config

from .routes.user import user
from .routes.post import post
from .routes.main import main
from .routes.comment import comment

def create_app(config=Config):
    
    app = Flask(__name__)
    
    app.config.from_object(config)    
        
    app.register_blueprint(user)
    app.register_blueprint(post)
    app.register_blueprint(main)
    app.register_blueprint(comment)    
    
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    
    # Настройка маршрутов для login_manager
    login_manager.login_view = 'user.login'
    login_manager.login_message = 'Для доступа к странице требуется авторизация'
    login_manager.login_message_category = 'info'
    
    with app.app_context():
        db.create_all()
    
    return app

