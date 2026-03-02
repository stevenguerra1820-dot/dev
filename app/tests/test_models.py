# tests/test_models.py
import pytest
from datetime import date
from app.models import Estudiante, Docente, Curso, Matricula, Calificacion

def test_crear_estudiante(db_session):
    """Prueba unitaria: crear un estudiante"""
    estudiante = Estudiante(
        nombre='Juan Pérez',
        email='juan@test.com',
        fecha_nacimiento=date(2000, 1, 1)
    )
    db_session.add(estudiante)
    db_session.commit()
    
    assert estudiante.id is not None
    assert estudiante.nombre == 'Juan Pérez'
    assert estudiante.email == 'juan@test.com'

def test_crear_docente(db_session):
    """Prueba unitaria: crear un docente"""
    docente = Docente(
        nombre='María García',
        email='maria@test.com',
        especialidad='Matemáticas'
    )
    db_session.add(docente)
    db_session.commit()
    
    assert docente.id is not None
    assert docente.especialidad == 'Matemáticas'

def test_crear_curso(db_session, sample_docente):
    """Prueba unitaria: crear un curso"""
    curso = Curso(
        nombre='Álgebra',
        descripcion='Curso de álgebra básica',
        creditos=4,
        docente_id=sample_docente.id
    )
    db_session.add(curso)
    db_session.commit()
    
    assert curso.id is not None
    assert curso.docente_id == sample_docente.id
    assert curso.creditos == 4

def test_relacion_curso_docente(db_session, sample_docente, sample_curso):
    """Prueba unitaria: verificar relación curso-docente"""
    assert sample_curso.docente.id == sample_docente.id
    assert sample_docente in sample_curso.docente.cursos

def test_relacion_estudiante_matricula(db_session, sample_estudiante, sample_matricula):
    """Prueba unitaria: verificar relación estudiante-matrícula"""
    assert sample_matricula.estudiante.id == sample_estudiante.id
    assert sample_matricula in sample_estudiante.matriculas

def test_crear_calificacion(db_session, sample_matricula):
    """Prueba unitaria: crear una calificación"""
    calificacion = Calificacion(
        matricula_id=sample_matricula.id,
        nota=9.5,
        observaciones='Excelente'
    )
    db_session.add(calificacion)
    db_session.commit()
    
    assert calificacion.id is not None
    assert calificacion.nota == 9.5
    assert calificacion.matricula_id == sample_matricula.id

def test_to_dict_estudiante(db_session, sample_estudiante):
    """Prueba unitaria: método to_dict de estudiante"""
    dict_data = sample_estudiante.to_dict()
    assert dict_data['id'] == sample_estudiante.id
    assert dict_data['nombre'] == sample_estudiante.nombre
    assert dict_data['email'] == sample_estudiante.email
    assert 'fecha_nacimiento' in dict_data