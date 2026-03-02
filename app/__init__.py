from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

# Inicializar extensiones
db = SQLAlchemy()

def create_app():
    """Factory function para crear la aplicación Flask"""
    app = Flask(__name__)
    
    # Configuración (igual que antes)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'clave-secreta-desarrollo')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///academica.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Inicializar extensiones
    db.init_app(app)
    
    # Registrar blueprints
    from app.routes import api_bp
    app.register_blueprint(api_bp)
    
    # Crear tablas
    with app.app_context():
        from app import models
        db.create_all()
        print("✅ Base de datos inicializada")
    
    return app