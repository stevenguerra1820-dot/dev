# tests/factories.py
import factory
from factory.fuzzy import FuzzyChoice, FuzzyFloat
from datetime import date, datetime
from app import db
from app.models import Estudiante, Docente, Curso, Matricula, Calificacion

class EstudianteFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Estudiante
        sqlalchemy_session = db.session
    
    nombre = factory.Faker('name')
    email = factory.Faker('email')
    fecha_nacimiento = factory.Faker('date_of_birth', minimum_age=18, maximum_age=30)
    fecha_registro = factory.LazyFunction(datetime.utcnow)

class DocenteFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Docente
        sqlalchemy_session = db.session
    
    nombre = factory.Faker('name')
    email = factory.Faker('email')
    especialidad = FuzzyChoice(['Matemáticas', 'Física', 'Programación', 'Literatura', 'Historia'])
    fecha_registro = factory.LazyFunction(datetime.utcnow)

class CursoFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Curso
        sqlalchemy_session = db.session
    
    nombre = factory.Faker('word')
    descripcion = factory.Faker('text', max_nb_chars=200)
    creditos = FuzzyChoice([2, 3, 4, 5])
    docente_id = None  # Se asigna después

class MatriculaFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Matricula
        sqlalchemy_session = db.session
    
    estudiante_id = None
    curso_id = None
    fecha_matricula = factory.LazyFunction(datetime.utcnow)
    estado = FuzzyChoice(['activa', 'cancelada', 'completada'])

class CalificacionFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Calificacion
        sqlalchemy_session = db.session
    
    matricula_id = None
    nota = FuzzyFloat(0, 10)
    fecha_registro = factory.LazyFunction(datetime.utcnow)
    observaciones = factory.Faker('text', max_nb_chars=100)