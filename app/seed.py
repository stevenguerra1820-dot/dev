from app import create_app, db
from app.models import Estudiante, Docente, Curso, Matricula, Calificacion
from datetime import date, datetime
import os
import sys

def seed_data():
    """Poblar la base de datos con datos de ejemplo"""
    # Determinar entorno
    env = os.getenv('FLASK_ENV', 'development')
    print(f"🌱 Sembrando datos en entorno: {env}")
    
    app = create_app(env)
    
    with app.app_context():
        # Verificar si ya hay datos
        if Docente.query.first() is not None:
            print("📦 La base de datos ya tiene datos. Omitiendo seed.")
            return
        
        print("🌱 Creando datos de ejemplo...")
        
        # Crear docentes
        docente1 = Docente(
            nombre='Carlos Rodríguez', 
            email='carlos.rodriguez@academica.com', 
            especialidad='Matemáticas'
        )
        docente2 = Docente(
            nombre='Ana Martínez', 
            email='ana.martinez@academica.com', 
            especialidad='Física'
        )
        docente3 = Docente(
            nombre='Miguel Sánchez', 
            email='miguel.sanchez@academica.com', 
            especialidad='Programación'
        )
        
        db.session.add_all([docente1, docente2, docente3])
        db.session.commit()
        print(f"✅ {len([docente1, docente2, docente3])} docentes creados")
        
        # Crear cursos
        curso1 = Curso(
            nombre='Cálculo I', 
            descripcion='Introducción al cálculo diferencial e integral', 
            creditos=4, 
            docente_id=docente1.id
        )
        curso2 = Curso(
            nombre='Física I', 
            descripcion='Mecánica clásica y termodinámica', 
            creditos=4, 
            docente_id=docente2.id
        )
        curso3 = Curso(
            nombre='Programación I', 
            descripcion='Fundamentos de algoritmos y Python', 
            creditos=3, 
            docente_id=docente3.id
        )
        curso4 = Curso(
            nombre='Álgebra Lineal', 
            descripcion='Vectores, matrices y espacios vectoriales', 
            creditos=3, 
            docente_id=docente1.id
        )
        
        db.session.add_all([curso1, curso2, curso3, curso4])
        db.session.commit()
        print(f"✅ {len([curso1, curso2, curso3, curso4])} cursos creados")
        
        # Crear estudiantes
        est1 = Estudiante(
            nombre='Luis Torres', 
            email='luis.torres@estudiante.com', 
            fecha_nacimiento=date(2001, 3, 10)
        )
        est2 = Estudiante(
            nombre='Laura Ríos', 
            email='laura.rios@estudiante.com', 
            fecha_nacimiento=date(2000, 7, 22)
        )
        est3 = Estudiante(
            nombre='Pedro Gómez', 
            email='pedro.gomez@estudiante.com', 
            fecha_nacimiento=date(2002, 1, 15)
        )
        est4 = Estudiante(
            nombre='Sofia Herrera', 
            email='sofia.herrera@estudiante.com', 
            fecha_nacimiento=date(2001, 11, 3)
        )
        
        db.session.add_all([est1, est2, est3, est4])
        db.session.commit()
        print(f"✅ {len([est1, est2, est3, est4])} estudiantes creados")
        
        # Crear matrículas
        mat1 = Matricula(estudiante_id=est1.id, curso_id=curso1.id, estado='activa')
        mat2 = Matricula(estudiante_id=est2.id, curso_id=curso1.id, estado='activa')
        mat3 = Matricula(estudiante_id=est3.id, curso_id=curso2.id, estado='activa')
        mat4 = Matricula(estudiante_id=est4.id, curso_id=curso2.id, estado='activa')
        mat5 = Matricula(estudiante_id=est1.id, curso_id=curso3.id, estado='activa')
        mat6 = Matricula(estudiante_id=est2.id, curso_id=curso4.id, estado='activa')
        mat7 = Matricula(estudiante_id=est3.id, curso_id=curso3.id, estado='completada')
        
        db.session.add_all([mat1, mat2, mat3, mat4, mat5, mat6, mat7])
        db.session.commit()
        print(f"✅ {len([mat1, mat2, mat3, mat4, mat5, mat6, mat7])} matrículas creadas")
        
        # Crear calificaciones
        cal1 = Calificacion(matricula_id=mat1.id, nota=9.0, observaciones='Excelente participación')
        cal2 = Calificacion(matricula_id=mat2.id, nota=7.5, observaciones='Buen trabajo')
        cal3 = Calificacion(matricula_id=mat3.id, nota=8.0, observaciones='Aprobado')
        cal4 = Calificacion(matricula_id=mat4.id, nota=6.5, observaciones='Necesita mejorar')
        cal5 = Calificacion(matricula_id=mat5.id, nota=9.5, observaciones='Sobresaliente')
        cal6 = Calificacion(matricula_id=mat7.id, nota=8.5, observaciones='Completado exitosamente')
        
        db.session.add_all([cal1, cal2, cal3, cal4, cal5, cal6])
        db.session.commit()
        print(f"✅ {len([cal1, cal2, cal3, cal4, cal5, cal6])} calificaciones creadas")
        
        print("\n" + "="*50)
        print("✅ ¡BASE DE DATOS INICIALIZADA CON ÉXITO!")
        print("="*50)
        print(f"📊 Estadísticas:")
        print(f"   - Docentes: {Docente.query.count()}")
        print(f"   - Cursos: {Curso.query.count()}")
        print(f"   - Estudiantes: {Estudiante.query.count()}")
        print(f"   - Matrículas: {Matricula.query.count()}")
        print(f"   - Calificaciones: {Calificacion.query.count()}")
        print("="*50)

if __name__ == '__main__':
    seed_data()