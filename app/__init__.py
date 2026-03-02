from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

# Inicializar extensiones
db = SQLAlchemy()

def create_app():
    """Factory function para crear la aplicación Flask"""
    app = Flask(__name__)
    
    # Configuración
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'clave-secreta-desarrollo')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///academica.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Inicializar extensiones con la app
    db.init_app(app)
    
    # Registrar blueprints (rutas)
    with app.app_context():
        from . import routes
        # Crear tablas si no existen
        db.create_all()
    
    return app