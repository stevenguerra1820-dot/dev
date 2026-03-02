# tests/test_integration.py
import pytest
from app.models import Estudiante, Docente, Curso, Matricula, Calificacion

class TestWorkflowCompleto:
    """Prueba de integración: flujo completo de la aplicación"""
    
    def test_workflow_registro_calificacion(self, client, db_session):
        """Prueba: registrar estudiante, matricular, calificar"""
        
        # 1. Crear docente
        docente_data = {
            'nombre': 'Prof. Rodríguez',
            'email': 'rodriguez@test.com',
            'especialidad': 'Matemáticas'
        }
        response_docente = client.post('/api/docentes', json=docente_data)
        assert response_docente.status_code == 201
        docente_id = response_docente.json['id']
        
        # 2. Crear curso
        curso_data = {
            'nombre': 'Geometría',
            'descripcion': 'Geometría analítica',
            'creditos': 3,
            'docente_id': docente_id
        }
        response_curso = client.post('/api/cursos', json=curso_data)
        assert response_curso.status_code == 201
        curso_id = response_curso.json['id']
        
        # 3. Crear estudiante
        estudiante_data = {
            'nombre': 'María Pérez',
            'email': 'maria.perez@test.com',
            'fecha_nacimiento': '2002-04-20'
        }
        response_estudiante = client.post('/api/estudiantes', json=estudiante_data)
        assert response_estudiante.status_code == 201
        estudiante_id = response_estudiante.json['id']
        
        # 4. Matricular estudiante
        matricula_data = {
            'estudiante_id': estudiante_id,
            'curso_id': curso_id
        }
        response_matricula = client.post('/api/matriculas', json=matricula_data)
        assert response_matricula.status_code == 201
        matricula_id = response_matricula.json['id']
        
        # 5. Asignar calificación
        calificacion_data = {
            'matricula_id': matricula_id,
            'nota': 8.7,
            'observaciones': 'Aprobado con mérito'
        }
        response_calificacion = client.post('/api/calificaciones', json=calificacion_data)
        assert response_calificacion.status_code == 201
        
        # 6. Verificar que todo se guardó correctamente
        response_estudiante_get = client.get(f'/api/estudiantes/{estudiante_id}')
        assert response_estudiante_get.status_code == 200
        
        response_calificaciones = client.get('/api/calificaciones')
        assert len(response_calificaciones.json) >= 1
        
        # 7. Verificar promedio del estudiante (lógica de negocio)
        matriculas_estudiante = Matricula.query.filter_by(estudiante_id=estudiante_id).all()
        for mat in matriculas_estudiante:
            if mat.calificaciones:
                promedio = sum(c.nota for c in mat.calificaciones) / len(mat.calificaciones)
                assert promedio == 8.7

class TestValidacionesComplejas:
    """Pruebas de validaciones y reglas de negocio"""
    
    def test_no_calificar_sin_matricula(self, client):
        """Prueba: no se puede calificar sin matrícula"""
        data = {
            'matricula_id': 9999,
            'nota': 8.0
        }
        response = client.post('/api/calificaciones', json=data)
        assert response.status_code == 404
    
    def test_estudiante_multiple_matriculas(self, client, db_session):
        """Prueba: estudiante en múltiples cursos"""
        # Crear datos
        estudiante = Estudiante(
            nombre='Test Student',
            email='test.student@test.com',
            fecha_nacimiento='2000-01-01'
        )
        db_session.add(estudiante)
        db_session.commit()
        
        # Crear dos cursos
        cursos = []
        for i in range(3):
            docente = Docente(
                nombre=f'Docente {i}',
                email=f'docente{i}@test.com'
            )
            db_session.add(docente)
            db_session.commit()
            
            curso = Curso(
                nombre=f'Curso {i}',
                docente_id=docente.id
            )
            db_session.add(curso)
            db_session.commit()
            cursos.append(curso)
        
        # Matricular en todos
        for curso in cursos:
            matricula = Matricula(
                estudiante_id=estudiante.id,
                curso_id=curso.id
            )
            db_session.add(matricula)
        db_session.commit()
        
        # Verificar matrículas
        assert len(estudiante.matriculas) == 3