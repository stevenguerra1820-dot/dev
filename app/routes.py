from flask import jsonify, request, Blueprint
from app import db
from app.models import Estudiante, Docente, Curso, Matricula, Calificacion
from datetime import datetime

# Crear blueprint para organizar rutas
api_bp = Blueprint('api', __name__, url_prefix='/api')

# ========== RUTAS DE ESTUDIANTES ==========
@api_bp.route('/estudiantes', methods=['GET'])
def get_estudiantes():
    """Obtener todos los estudiantes"""
    estudiantes = Estudiante.query.all()
    return jsonify([e.to_dict() for e in estudiantes])

@api_bp.route('/estudiantes/<int:id>', methods=['GET'])
def get_estudiante(id):
    """Obtener un estudiante por ID"""
    estudiante = Estudiante.query.get(id)
    if not estudiante:
        return jsonify({'error': 'Estudiante no encontrado'}), 404
    return jsonify(estudiante.to_dict())

@api_bp.route('/estudiantes', methods=['POST'])
def create_estudiante():
    """Crear un nuevo estudiante"""
    data = request.get_json()
    
    # Validar datos requeridos
    if not data or not data.get('nombre') or not data.get('email') or not data.get('fecha_nacimiento'):
        return jsonify({'error': 'Faltan datos requeridos'}), 400
    
    # Verificar si el email ya existe
    if Estudiante.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'El email ya está registrado'}), 400
    
    try:
        fecha_nac = datetime.strptime(data['fecha_nacimiento'], '%Y-%m-%d').date()
    except:
        return jsonify({'error': 'Formato de fecha inválido. Use YYYY-MM-DD'}), 400
    
    estudiante = Estudiante(
        nombre=data['nombre'],
        email=data['email'],
        fecha_nacimiento=fecha_nac
    )
    
    db.session.add(estudiante)
    db.session.commit()
    
    return jsonify(estudiante.to_dict()), 201

# ========== RUTAS DE DOCENTES ==========
@api_bp.route('/docentes', methods=['GET'])
def get_docentes():
    """Obtener todos los docentes"""
    docentes = Docente.query.all()
    return jsonify([d.to_dict() for d in docentes])

@api_bp.route('/docentes', methods=['POST'])
def create_docente():
    """Crear un nuevo docente"""
    data = request.get_json()
    
    if not data or not data.get('nombre') or not data.get('email'):
        return jsonify({'error': 'Faltan datos requeridos'}), 400
    
    if Docente.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'El email ya está registrado'}), 400
    
    docente = Docente(
        nombre=data['nombre'],
        email=data['email'],
        especialidad=data.get('especialidad', '')
    )
    
    db.session.add(docente)
    db.session.commit()
    
    return jsonify(docente.to_dict()), 201

# ========== RUTAS DE CURSOS ==========
@api_bp.route('/cursos', methods=['GET'])
def get_cursos():
    """Obtener todos los cursos"""
    cursos = Curso.query.all()
    return jsonify([c.to_dict() for c in cursos])

@api_bp.route('/cursos', methods=['POST'])
def create_curso():
    """Crear un nuevo curso"""
    data = request.get_json()
    
    if not data or not data.get('nombre') or not data.get('docente_id'):
        return jsonify({'error': 'Faltan datos requeridos'}), 400
    
    # Verificar que el docente existe
    docente = Docente.query.get(data['docente_id'])
    if not docente:
        return jsonify({'error': 'Docente no encontrado'}), 404
    
    curso = Curso(
        nombre=data['nombre'],
        descripcion=data.get('descripcion', ''),
        creditos=data.get('creditos', 3),
        docente_id=data['docente_id']
    )
    
    db.session.add(curso)
    db.session.commit()
    
    return jsonify(curso.to_dict()), 201

# ========== RUTAS DE MATRÍCULAS ==========
@api_bp.route('/matriculas', methods=['GET'])
def get_matriculas():
    """Obtener todas las matrículas"""
    matriculas = Matricula.query.all()
    return jsonify([m.to_dict() for m in matriculas])

@api_bp.route('/matriculas', methods=['POST'])
def create_matricula():
    """Crear una nueva matrícula"""
    data = request.get_json()
    
    if not data or not data.get('estudiante_id') or not data.get('curso_id'):
        return jsonify({'error': 'Faltan datos requeridos'}), 400
    
    # Verificar que estudiante y curso existen
    estudiante = Estudiante.query.get(data['estudiante_id'])
    curso = Curso.query.get(data['curso_id'])
    
    if not estudiante:
        return jsonify({'error': 'Estudiante no encontrado'}), 404
    if not curso:
        return jsonify({'error': 'Curso no encontrado'}), 404
    
    # Verificar que no exista ya la matrícula
    existe = Matricula.query.filter_by(
        estudiante_id=data['estudiante_id'],
        curso_id=data['curso_id']
    ).first()
    
    if existe:
        return jsonify({'error': 'El estudiante ya está matriculado en este curso'}), 400
    
    matricula = Matricula(
        estudiante_id=data['estudiante_id'],
        curso_id=data['curso_id'],
        estado=data.get('estado', 'activa')
    )
    
    db.session.add(matricula)
    db.session.commit()
    
    return jsonify(matricula.to_dict()), 201

# ========== RUTAS DE CALIFICACIONES ==========
@api_bp.route('/calificaciones', methods=['GET'])
def get_calificaciones():
    """Obtener todas las calificaciones"""
    calificaciones = Calificacion.query.all()
    return jsonify([c.to_dict() for c in calificaciones])

@api_bp.route('/calificaciones', methods=['POST'])
def create_calificacion():
    """Crear una nueva calificación"""
    data = request.get_json()
    
    if not data or not data.get('matricula_id') or data.get('nota') is None:
        return jsonify({'error': 'Faltan datos requeridos'}), 400
    
    # Validar que la nota esté entre 0 y 10
    nota = float(data['nota'])
    if nota < 0 or nota > 10:
        return jsonify({'error': 'La nota debe estar entre 0 y 10'}), 400
    
    # Verificar que la matrícula existe
    matricula = Matricula.query.get(data['matricula_id'])
    if not matricula:
        return jsonify({'error': 'Matrícula no encontrada'}), 404
    
    calificacion = Calificacion(
        matricula_id=data['matricula_id'],
        nota=nota,
        observaciones=data.get('observaciones', '')
    )
    
    db.session.add(calificacion)
    db.session.commit()
    
    return jsonify(calificacion.to_dict()), 201

# ========== RUTA DE BIENVENIDA ==========
@api_bp.route('/', methods=['GET'])
def index():
    return jsonify({
        'mensaje': 'API de Gestión Académica',
        'versión': '1.0',
        'endpoints': [
            '/api/estudiantes',
            '/api/docentes',
            '/api/cursos',
            '/api/matriculas',
            '/api/calificaciones'
        ]
    })