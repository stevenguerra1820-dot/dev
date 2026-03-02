# tests/conftest.py
import pytest
from app import create_app, db
from app.models import Estudiante, Docente, Curso, Matricula, Calificacion
from tests.factories import (
    EstudianteFactory, DocenteFactory, 
    CursoFactory, MatriculaFactory, CalificacionFactory
)

@pytest.fixture(scope='session')
def app():
    """Fixture de aplicación para todas las pruebas"""
    app = create_app('testing')
    app.config.update({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'SQLALCHEMY_TRACK_MODIFICATIONS': False
    })
    return app

@pytest.fixture
def client(app):
    """Fixture para cliente de pruebas"""
    return app.test_client()

@pytest.fixture
def db_session(app):
    """Fixture para sesión de base de datos"""
    with app.app_context():
        db.create_all()
        yield db.session
        db.session.remove()
        db.drop_all()

@pytest.fixture
def estudiante_factory(db_session):
    """Fixture factory de estudiantes"""
    return EstudianteFactory

@pytest.fixture
def docente_factory(db_session):
    """Fixture factory de docentes"""
    return DocenteFactory

@pytest.fixture
def curso_factory(db_session):
    """Fixture factory de cursos"""
    return CursoFactory

@pytest.fixture
def matricula_factory(db_session):
    """Fixture factory de matrículas"""
    return MatriculaFactory

@pytest.fixture
def calificacion_factory(db_session):
    """Fixture factory de calificaciones"""
    return CalificacionFactory

@pytest.fixture
def sample_docente(db_session):
    """Crear un docente de ejemplo"""
    docente = DocenteFactory()
    db_session.add(docente)
    db_session.commit()
    return docente

@pytest.fixture
def sample_estudiante(db_session):
    """Crear un estudiante de ejemplo"""
    estudiante = EstudianteFactory()
    db_session.add(estudiante)
    db_session.commit()
    return estudiante

@pytest.fixture
def sample_curso(db_session, sample_docente):
    """Crear un curso de ejemplo"""
    curso = CursoFactory(docente_id=sample_docente.id)
    db_session.add(curso)
    db_session.commit()
    return curso

@pytest.fixture
def sample_matricula(db_session, sample_estudiante, sample_curso):
    """Crear una matrícula de ejemplo"""
    matricula = MatriculaFactory(
        estudiante_id=sample_estudiante.id,
        curso_id=sample_curso.id
    )
    db_session.add(matricula)
    db_session.commit()
    return matricula