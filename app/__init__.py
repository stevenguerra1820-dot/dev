from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()

def create_app(config_name=None):
    app = Flask(__name__)
    
    # Cargar configuración
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'default')
    
    from config import config
    app.config.from_object(config.get(config_name))
    
    # Inicializar extensiones
    db.init_app(app)
    
    # Registrar blueprints
    from app.routes import api_bp
    app.register_blueprint(api_bp)
    
    # Crear tablas
    with app.app_context():
        from app import models
        db.create_all()
        print(f"✅ Base de datos inicializada en modo: {config_name}")
        print(f"📊 URI: {app.config['SQLALCHEMY_DATABASE_URI']}")
    
    return app