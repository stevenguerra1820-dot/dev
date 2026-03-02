# config.py
import os

class Config:
    """Configuración base"""
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-key-cambiar-en-produccion')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
class DevelopmentConfig(Config):
    """Configuración de desarrollo"""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///academica.db')

class DockerConfig(Config):
    """Configuración para Docker"""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://admin:admin123@db:5432/academica')

class ProductionConfig(Config):
    """Configuración de producción"""
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    
# Seleccionar configuración según entorno
config = {
    'development': DevelopmentConfig,
    'docker': DockerConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}