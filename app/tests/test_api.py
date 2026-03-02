# tests/test_api.py
import pytest
import json
from app.models import Estudiante, Docente, Curso, Matricula, Calificacion

class TestEstudiantesAPI:
    """Pruebas de integración para endpoints de estudiantes"""
    
    def test_get_estudiantes_empty(self, client):
        """GET /api/estudiantes - lista vacía"""
        response = client.get('/api/estudiantes')
        assert response.status_code == 200
        assert response.json == []
    
    def test_create_estudiante(self, client):
        """POST /api/estudiantes - crear estudiante"""
        data = {
            'nombre': 'Ana López',
            'email': 'ana@test.com',
            'fecha_nacimiento': '2001-05-15'
        }
        response = client.post('/api/estudiantes', 
                               json=data,
                               content_type='application/json')
        
        assert response.status_code == 201
        assert response.json['nombre'] == 'Ana López'
        assert response.json['email'] == 'ana@test.com'
        assert 'id' in response.json
    
    def test_create_estudiante_missing_data(self, client):
        """POST /api/estudiantes - datos incompletos"""
        data = {'nombre': 'Ana López'}  # Falta email y fecha
        response = client.post('/api/estudiantes', json=data)
        assert response.status_code == 400
        assert 'error' in response.json
    
    def test_create_duplicate_email(self, client, db_session):
        """POST /api/estudiantes - email duplicado"""
        # Crear primer estudiante
        data1 = {
            'nombre': 'Ana López',
            'email': 'ana@test.com',
            'fecha_nacimiento': '2001-05-15'
        }
        response1 = client.post('/api/estudiantes', json=data1)
        assert response1.status_code == 201
        
        # Intentar crear otro con mismo email
        data2 = {
            'nombre': 'Ana García',
            'email': 'ana@test.com',
            'fecha_nacimiento': '2000-03-10'
        }
        response2 = client.post('/api/estudiantes', json=data2)
        assert response2.status_code == 400
        assert 'email ya está registrado' in response2.json['error']
    
    def test_get_estudiante_by_id(self, client, db_session):
        """GET /api/estudiantes/<id> - obtener por ID"""
        # Crear estudiante primero
        estudiante = Estudiante(
            nombre='Carlos Ruiz',
            email='carlos@test.com',
            fecha_nacimiento='2000-07-20'
        )
        db_session.add(estudiante)
        db_session.commit()
        
        response = client.get(f'/api/estudiantes/{estudiante.id}')
        assert response.status_code == 200
        assert response.json['nombre'] == 'Carlos Ruiz'
    
    def test_get_estudiante_not_found(self, client):
        """GET /api/estudiantes/<id> - ID no existe"""
        response = client.get('/api/estudiantes/9999')
        assert response.status_code == 404

class TestDocentesAPI:
    """Pruebas de integración para endpoints de docentes"""
    
    def test_create_docente(self, client):
        """POST /api/docentes - crear docente"""
        data = {
            'nombre': 'Prof. Martínez',
            'email': 'martinez@test.com',
            'especialidad': 'Física'
        }
        response = client.post('/api/docentes', json=data)
        assert response.status_code == 201
        assert response.json['nombre'] == 'Prof. Martínez'
        assert response.json['especialidad'] == 'Física'

class TestCursosAPI:
    """Pruebas de integración para endpoints de cursos"""
    
    def test_create_curso(self, client, db_session):
        """POST /api/cursos - crear curso"""
        # Crear docente primero
        docente = Docente(
            nombre='Prof. García',
            email='garcia@test.com',
            especialidad='Matemáticas'
        )
        db_session.add(docente)
        db_session.commit()
        
        data = {
            'nombre': 'Cálculo I',
            'descripcion': 'Curso de cálculo diferencial',
            'creditos': 4,
            'docente_id': docente.id
        }
        response = client.post('/api/cursos', json=data)
        assert response.status_code == 201
        assert response.json['nombre'] == 'Cálculo I'
        assert response.json['docente_id'] == docente.id
    
    def test_create_curso_invalid_docente(self, client):
        """POST /api/cursos - docente no existe"""
        data = {
            'nombre': 'Cálculo I',
            'docente_id': 9999
        }
        response = client.post('/api/cursos', json=data)
        assert response.status_code == 404

class TestMatriculasAPI:
    """Pruebas de integración para endpoints de matrículas"""
    
    def test_create_matricula(self, client, db_session):
        """POST /api/matriculas - crear matrícula"""
        # Crear estudiante y curso
        estudiante = Estudiante(
            nombre='Luis Torres',
            email='luis@test.com',
            fecha_nacimiento='2001-03-10'
        )
        docente = Docente(
            nombre='Prof. Ruiz',
            email='ruiz@test.com',
            especialidad='Programación'
        )
        db_session.add_all([estudiante, docente])
        db_session.commit()
        
        curso = Curso(
            nombre='Python Básico',
            docente_id=docente.id
        )
        db_session.add(curso)
        db_session.commit()
        
        data = {
            'estudiante_id': estudiante.id,
            'curso_id': curso.id,
            'estado': 'activa'
        }
        response = client.post('/api/matriculas', json=data)
        assert response.status_code == 201
        assert response.json['estudiante_id'] == estudiante.id
        assert response.json['curso_id'] == curso.id
    
    def test_create_duplicate_matricula(self, client, db_session, sample_matricula):
        """POST /api/matriculas - matrícula duplicada"""
        data = {
            'estudiante_id': sample_matricula.estudiante_id,
            'curso_id': sample_matricula.curso_id
        }
        response = client.post('/api/matriculas', json=data)
        assert response.status_code == 400
        assert 'ya está matriculado' in response.json['error']

class TestCalificacionesAPI:
    """Pruebas de integración para endpoints de calificaciones"""
    
    def test_create_calificacion(self, client, db_session, sample_matricula):
        """POST /api/calificaciones - crear calificación"""
        data = {
            'matricula_id': sample_matricula.id,
            'nota': 9.0,
            'observaciones': 'Muy buen trabajo'
        }
        response = client.post('/api/calificaciones', json=data)
        assert response.status_code == 201
        assert response.json['nota'] == 9.0
        assert response.json['matricula_id'] == sample_matricula.id
    
    def test_create_calificacion_invalid_nota(self, client, sample_matricula):
        """POST /api/calificaciones - nota fuera de rango"""
        data = {
            'matricula_id': sample_matricula.id,
            'nota': 15.0  # Nota inválida > 10
        }
        response = client.post('/api/calificaciones', json=data)
        assert response.status_code == 400
        assert 'entre 0 y 10' in response.json['error']

def test_api_index(client):
    """GET /api/ - endpoint de bienvenida"""
    response = client.get('/api/')
    assert response.status_code == 200
    assert 'mensaje' in response.json
    assert 'endpoints' in response.json