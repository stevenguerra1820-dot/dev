from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flasgger import Swagger
import os

db = SQLAlchemy()
swagger = Swagger()

def create_app(config_name=None):
    app = Flask(__name__)
    
    # Cargar configuración
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'default')
    
    from config import config
    app.config.from_object(config.get(config_name))
    
    # Configuración de Swagger
    app.config['SWAGGER'] = {
        'title': 'API de Gestión Académica',
        'description': '''API RESTful para sistema de gestión académica.
        
        ## Características
        * Gestión de estudiantes
        * Gestión de docentes
        * Gestión de cursos
        * Matrículas
        * Calificaciones
        
        ## Autenticación
        Esta versión no requiere autenticación.
        ''',
        'version': '1.0.0',
        'termsOfService': '',
        'hide_top_bar': True,
        'specs_route': '/docs/',
        'specs': [
            {
                'endpoint': 'apispec',
                'route': '/apispec.json',
                'rule_filter': lambda rule: True,
                'model_filter': lambda tag: True,
            }
        ],
        'static_url_path': '/flasgger_static',
    }
    
    # Inicializar extensiones
    db.init_app(app)
    swagger.init_app(app)
    
    # Registrar blueprints
    from app.routes import api_bp
    app.register_blueprint(api_bp)
    
    # Crear tablas
    with app.app_context():
        from app import models
        db.create_all()
        print(f"✅ Base de datos inicializada en modo: {config_name}")
    
    return app