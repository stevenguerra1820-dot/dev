from app import create_app, db
from app.models import Estudiante, Docente, Curso, Matricula, Calificacion
from datetime import date, datetime

def seed_data():
    """Poblar la base de datos con datos de ejemplo"""
    app = create_app()
    with app.app_context():
        # Crear tablas
        db.drop_all()  # Cuidado: esto borra todos los datos existentes
        db.create_all()
        
        # Crear docentes
        docente1 = Docente(nombre='Carlos Rodríguez', email='carlos@email.com', especialidad='Matemáticas')
        docente2 = Docente(nombre='Ana Martínez', email='ana@email.com', especialidad='Física')
        db.session.add_all([docente1, docente2])
        db.session.commit()
        
        # Crear cursos
        curso1 = Curso(nombre='Cálculo I', descripcion='Introducción al cálculo', creditos=4, docente_id=docente1.id)
        curso2 = Curso(nombre='Física I', descripcion='Mecánica clásica', creditos=4, docente_id=docente2.id)
        db.session.add_all([curso1, curso2])
        db.session.commit()
        
        # Crear estudiantes
        est1 = Estudiante(nombre='Luis Torres', email='luis@email.com', fecha_nacimiento=date(2001, 3, 10))
        est2 = Estudiante(nombre='Laura Ríos', email='laura@email.com', fecha_nacimiento=date(2000, 7, 22))
        db.session.add_all([est1, est2])
        db.session.commit()
        
        # Crear matrículas
        mat1 = Matricula(estudiante_id=est1.id, curso_id=curso1.id, estado='activa')
        mat2 = Matricula(estudiante_id=est2.id, curso_id=curso1.id, estado='activa')
        mat3 = Matricula(estudiante_id=est2.id, curso_id=curso2.id, estado='activa')
        db.session.add_all([mat1, mat2, mat3])
        db.session.commit()
        
        # Crear calificaciones
        cal1 = Calificacion(matricula_id=mat1.id, nota=9.0, observaciones='Excelente')
        cal2 = Calificacion(matricula_id=mat2.id, nota=7.5, observaciones='Bueno')
        db.session.add_all([cal1, cal2])
        db.session.commit()
        
        print("✅ Datos de prueba insertados correctamente")

if __name__ == '__main__':
    seed_data()