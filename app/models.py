from app import db
from datetime import datetime

class Estudiante(db.Model):
    """Modelo para representar un estudiante"""
    __tablename__ = 'estudiantes'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    fecha_nacimiento = db.Column(db.Date, nullable=False)
    fecha_registro = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relaciones
    matriculas = db.relationship('Matricula', back_populates='estudiante', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Estudiante {self.nombre}>'
    
    def to_dict(self):
        """Convertir objeto a diccionario para respuestas JSON"""
        return {
            'id': self.id,
            'nombre': self.nombre,
            'email': self.email,
            'fecha_nacimiento': self.fecha_nacimiento.strftime('%Y-%m-%d'),
            'fecha_registro': self.fecha_registro.strftime('%Y-%m-%d %H:%M:%S')
        }


class Docente(db.Model):
    """Modelo para representar un docente/profesor"""
    __tablename__ = 'docentes'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    especialidad = db.Column(db.String(100))
    fecha_registro = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relaciones
    cursos = db.relationship('Curso', back_populates='docente', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Docente {self.nombre}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'email': self.email,
            'especialidad': self.especialidad,
            'fecha_registro': self.fecha_registro.strftime('%Y-%m-%d %H:%M:%S')
        }


class Curso(db.Model):
    """Modelo para representar un curso académico"""
    __tablename__ = 'cursos'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text)
    creditos = db.Column(db.Integer, default=3)
    docente_id = db.Column(db.Integer, db.ForeignKey('docentes.id'), nullable=False)
    
    # Relaciones
    docente = db.relationship('Docente', back_populates='cursos')
    matriculas = db.relationship('Matricula', back_populates='curso', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Curso {self.nombre}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'descripcion': self.descripcion,
            'creditos': self.creditos,
            'docente_id': self.docente_id,
            'docente_nombre': self.docente.nombre if self.docente else None
        }


class Matricula(db.Model):
    """Modelo para representar la inscripción de un estudiante en un curso"""
    __tablename__ = 'matriculas'
    
    id = db.Column(db.Integer, primary_key=True)
    estudiante_id = db.Column(db.Integer, db.ForeignKey('estudiantes.id'), nullable=False)
    curso_id = db.Column(db.Integer, db.ForeignKey('cursos.id'), nullable=False)
    fecha_matricula = db.Column(db.DateTime, default=datetime.utcnow)
    estado = db.Column(db.String(20), default='activa')  # activa, cancelada, completada
    
    # Relaciones
    estudiante = db.relationship('Estudiante', back_populates='matriculas')
    curso = db.relationship('Curso', back_populates='matriculas')
    calificaciones = db.relationship('Calificacion', back_populates='matricula', cascade='all, delete-orphan')
    
    # Asegurar que un estudiante no se matricule dos veces en el mismo curso
    __table_args__ = (db.UniqueConstraint('estudiante_id', 'curso_id', name='unique_matricula'),)
    
    def __repr__(self):
        return f'<Matricula {self.estudiante.nombre} - {self.curso.nombre}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'estudiante_id': self.estudiante_id,
            'estudiante_nombre': self.estudiante.nombre if self.estudiante else None,
            'curso_id': self.curso_id,
            'curso_nombre': self.curso.nombre if self.curso else None,
            'fecha_matricula': self.fecha_matricula.strftime('%Y-%m-%d %H:%M:%S'),
            'estado': self.estado
        }


class Calificacion(db.Model):
    """Modelo para representar las notas de un estudiante en un curso"""
    __tablename__ = 'calificaciones'
    
    id = db.Column(db.Integer, primary_key=True)
    matricula_id = db.Column(db.Integer, db.ForeignKey('matriculas.id'), nullable=False)
    nota = db.Column(db.Float, nullable=False)
    fecha_registro = db.Column(db.DateTime, default=datetime.utcnow)
    observaciones = db.Column(db.Text)
    
    # Relaciones
    matricula = db.relationship('Matricula', back_populates='calificaciones')
    
    # Validación: nota entre 0 y 10 (opcional, se puede hacer a nivel de aplicación)
    
    def __repr__(self):
        return f'<Calificacion {self.nota} - Matricula {self.matricula_id}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'matricula_id': self.matricula_id,
            'estudiante_nombre': self.matricula.estudiante.nombre if self.matricula and self.matricula.estudiante else None,
            'curso_nombre': self.matricula.curso.nombre if self.matricula and self.matricula.curso else None,
            'nota': self.nota,
            'fecha_registro': self.fecha_registro.strftime('%Y-%m-%d %H:%M:%S'),
            'observaciones': self.observaciones
        }