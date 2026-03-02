import pytest
from app import create_app

@pytest.fixture
def app():
    """Fixture de aplicación para pruebas"""
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    with app.app_context():
        from app import db
        db.create_all()
    
    return app

@pytest.fixture
def client(app):
    """Fixture para cliente de pruebas"""
    return app.test_client()

def test_app_exists(client):
    """Prueba básica: verificar que la app responde"""
    response = client.get('/')
    assert response.status_code == 404  # Aún no hay rutas definidas