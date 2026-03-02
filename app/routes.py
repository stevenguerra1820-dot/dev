# app/routes.py
from flask import jsonify, request, Blueprint
from app import db
from app.models import Estudiante, Docente, Curso, Matricula, Calificacion
from datetime import datetime
from flasgger import swag_from

api_bp = Blueprint('api', __name__, url_prefix='/api')

# ============================================================================
# ENDPOINTS DE ESTUDIANTES
# ============================================================================

@api_bp.route('/estudiantes', methods=['GET'])
@swag_from({
    'tags': ['Estudiantes'],
    'summary': 'Obtener todos los estudiantes',
    'description': 'Retorna una lista completa de todos los estudiantes registrados en el sistema',
    'responses': {
        200: {
            'description': 'Lista exitosa de estudiantes',
            'schema': {
                'type': 'array',
                'items': {
                    'type': 'object',
                    'properties': {
                        'id': {'type': 'integer', 'example': 1},
                        'nombre': {'type': 'string', 'example': 'Juan Pérez'},
                        'email': {'type': 'string', 'example': 'juan.perez@email.com'},
                        'fecha_nacimiento': {'type': 'string', 'example': '2000-05-15'},
                        'fecha_registro': {'type': 'string', 'example': '2024-01-15 10:30:00'}
                    }
                }
            }
        }
    }
})
def get_estudiantes():
    """Obtener todos los estudiantes"""
    estudiantes = Estudiante.query.all()
    return jsonify([e.to_dict() for e in estudiantes])


@api_bp.route('/estudiantes/<int:id>', methods=['GET'])
@swag_from({
    'tags': ['Estudiantes'],
    'summary': 'Obtener un estudiante por ID',
    'description': 'Retorna los detalles de un estudiante específico usando su ID',
    'parameters': [
        {
            'name': 'id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'ID único del estudiante'
        }
    ],
    'responses': {
        200: {
            'description': 'Estudiante encontrado',
            'schema': {
                'type': 'object',
                'properties': {
                    'id': {'type': 'integer', 'example': 1},
                    'nombre': {'type': 'string', 'example': 'Juan Pérez'},
                    'email': {'type': 'string', 'example': 'juan.perez@email.com'},
                    'fecha_nacimiento': {'type': 'string', 'example': '2000-05-15'},
                    'fecha_registro': {'type': 'string', 'example': '2024-01-15 10:30:00'}
                }
            }
        },
        404: {
            'description': 'Estudiante no encontrado',
            'schema': {
                'type': 'object',
                'properties': {
                    'error': {'type': 'string', 'example': 'Estudiante no encontrado'}
                }
            }
        }
    }
})
def get_estudiante(id):
    """Obtener un estudiante por ID"""
    estudiante = Estudiante.query.get(id)
    if not estudiante:
        return jsonify({'error': 'Estudiante no encontrado'}), 404
    return jsonify(estudiante.to_dict())


@api_bp.route('/estudiantes', methods=['POST'])
@swag_from({
    'tags': ['Estudiantes'],
    'summary': 'Crear un nuevo estudiante',
    'description': 'Registra un nuevo estudiante en el sistema con los datos proporcionados',
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'description': 'Datos del estudiante a crear',
            'schema': {
                'type': 'object',
                'required': ['nombre', 'email', 'fecha_nacimiento'],
                'properties': {
                    'nombre': {
                        'type': 'string', 
                        'example': 'María García',
                        'description': 'Nombre completo del estudiante'
                    },
                    'email': {
                        'type': 'string', 
                        'example': 'maria.garcia@email.com',
                        'description': 'Correo electrónico único'
                    },
                    'fecha_nacimiento': {
                        'type': 'string', 
                        'example': '2001-08-20',
                        'description': 'Fecha de nacimiento en formato YYYY-MM-DD'
                    }
                }
            }
        }
    ],
    'responses': {
        201: {
            'description': 'Estudiante creado exitosamente',
            'schema': {
                'type': 'object',
                'properties': {
                    'id': {'type': 'integer', 'example': 1},
                    'nombre': {'type': 'string', 'example': 'María García'},
                    'email': {'type': 'string', 'example': 'maria.garcia@email.com'},
                    'fecha_nacimiento': {'type': 'string', 'example': '2001-08-20'},
                    'fecha_registro': {'type': 'string', 'example': '2024-01-15 10:30:00'}
                }
            }
        },
        400: {
            'description': 'Error en los datos enviados',
            'schema': {
                'type': 'object',
                'properties': {
                    'error': {'type': 'string', 'example': 'El email ya está registrado'}
                }
            }
        }
    }
})
def create_estudiante():
    """Crear un nuevo estudiante"""
    data = request.get_json()
    
    # Validar datos requeridos
    if not data:
        return jsonify({'error': 'No se enviaron datos'}), 400
    
    campos_requeridos = ['nombre', 'email', 'fecha_nacimiento']
    for campo in campos_requeridos:
        if campo not in data:
            return jsonify({'error': f'Falta el campo requerido: {campo}'}), 400
    
    # Validar formato de email (básico)
    if '@' not in data['email'] or '.' not in data['email']:
        return jsonify({'error': 'Formato de email inválido'}), 400
    
    # Verificar email único
    if Estudiante.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'El email ya está registrado'}), 400
    
    # Validar fecha
    try:
        fecha_nac = datetime.strptime(data['fecha_nacimiento'], '%Y-%m-%d').date()
    except ValueError:
        return jsonify({'error': 'Formato de fecha inválido. Use YYYY-MM-DD'}), 400
    
    # Validar edad mínima (18 años)
    hoy = datetime.now().date()
    edad = hoy.year - fecha_nac.year - ((hoy.month, hoy.day) < (fecha_nac.month, fecha_nac.day))
    if edad < 18:
        return jsonify({'error': 'El estudiante debe ser mayor de 18 años'}), 400
    
    # Crear estudiante
    estudiante = Estudiante(
        nombre=data['nombre'].strip(),
        email=data['email'].strip().lower(),
        fecha_nacimiento=fecha_nac
    )
    
    db.session.add(estudiante)
    db.session.commit()
    
    return jsonify(estudiante.to_dict()), 201


@api_bp.route('/estudiantes/<int:id>', methods=['PUT'])
@swag_from({
    'tags': ['Estudiantes'],
    'summary': 'Actualizar un estudiante existente',
    'description': 'Actualiza los datos de un estudiante específico',
    'parameters': [
        {
            'name': 'id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'ID del estudiante a actualizar'
        },
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'nombre': {'type': 'string', 'example': 'María García López'},
                    'email': {'type': 'string', 'example': 'maria.nuevo@email.com'},
                    'fecha_nacimiento': {'type': 'string', 'example': '2001-08-20'}
                }
            }
        }
    ],
    'responses': {
        200: {
            'description': 'Estudiante actualizado'
        },
        404: {
            'description': 'Estudiante no encontrado'
        }
    }
})
def update_estudiante(id):
    """Actualizar un estudiante existente"""
    estudiante = Estudiante.query.get(id)
    if not estudiante:
        return jsonify({'error': 'Estudiante no encontrado'}), 404
    
    data = request.get_json()
    
    # Actualizar campos si están presentes
    if data.get('nombre'):
        estudiante.nombre = data['nombre'].strip()
    
    if data.get('email'):
        # Verificar que el nuevo email no exista (excepto el del mismo estudiante)
        existe = Estudiante.query.filter(
            Estudiante.email == data['email'].strip().lower(),
            Estudiante.id != id
        ).first()
        if existe:
            return jsonify({'error': 'El email ya está registrado por otro estudiante'}), 400
        estudiante.email = data['email'].strip().lower()
    
    if data.get('fecha_nacimiento'):
        try:
            estudiante.fecha_nacimiento = datetime.strptime(data['fecha_nacimiento'], '%Y-%m-%d').date()
        except ValueError:
            return jsonify({'error': 'Formato de fecha inválido. Use YYYY-MM-DD'}), 400
    
    db.session.commit()
    
    return jsonify(estudiante.to_dict())


@api_bp.route('/estudiantes/<int:id>', methods=['DELETE'])
@swag_from({
    'tags': ['Estudiantes'],
    'summary': 'Eliminar un estudiante',
    'description': 'Elimina un estudiante y todas sus matrículas asociadas',
    'parameters': [
        {
            'name': 'id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'ID del estudiante a eliminar'
        }
    ],
    'responses': {
        200: {
            'description': 'Estudiante eliminado',
            'schema': {
                'type': 'object',
                'properties': {
                    'mensaje': {'type': 'string', 'example': 'Estudiante eliminado exitosamente'}
                }
            }
        },
        404: {
            'description': 'Estudiante no encontrado'
        }
    }
})
def delete_estudiante(id):
    """Eliminar un estudiante"""
    estudiante = Estudiante.query.get(id)
    if not estudiante:
        return jsonify({'error': 'Estudiante no encontrado'}), 404
    
    db.session.delete(estudiante)
    db.session.commit()
    
    return jsonify({'mensaje': 'Estudiante eliminado exitosamente'})


# ============================================================================
# ENDPOINTS DE DOCENTES
# ============================================================================

@api_bp.route('/docentes', methods=['GET'])
@swag_from({
    'tags': ['Docentes'],
    'summary': 'Obtener todos los docentes',
    'description': 'Retorna una lista de todos los docentes registrados'
})
def get_docentes():
    """Obtener todos los docentes"""
    docentes = Docente.query.all()
    return jsonify([d.to_dict() for d in docentes])


@api_bp.route('/docentes/<int:id>', methods=['GET'])
@swag_from({
    'tags': ['Docentes'],
    'summary': 'Obtener un docente por ID',
    'parameters': [
        {
            'name': 'id',
            'in': 'path',
            'type': 'integer',
            'required': True
        }
    ]
})
def get_docente(id):
    """Obtener un docente por ID"""
    docente = Docente.query.get(id)
    if not docente:
        return jsonify({'error': 'Docente no encontrado'}), 404
    return jsonify(docente.to_dict())


@api_bp.route('/docentes', methods=['POST'])
@swag_from({
    'tags': ['Docentes'],
    'summary': 'Crear un nuevo docente',
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'required': ['nombre', 'email'],
                'properties': {
                    'nombre': {'type': 'string', 'example': 'Carlos Rodríguez'},
                    'email': {'type': 'string', 'example': 'carlos.rodriguez@email.com'},
                    'especialidad': {'type': 'string', 'example': 'Matemáticas'}
                }
            }
        }
    ]
})
def create_docente():
    """Crear un nuevo docente"""
    data = request.get_json()
    
    if not data or not data.get('nombre') or not data.get('email'):
        return jsonify({'error': 'Faltan datos requeridos'}), 400
    
    if Docente.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'El email ya está registrado'}), 400
    
    docente = Docente(
        nombre=data['nombre'].strip(),
        email=data['email'].strip().lower(),
        especialidad=data.get('especialidad', '').strip()
    )
    
    db.session.add(docente)
    db.session.commit()
    
    return jsonify(docente.to_dict()), 201


@api_bp.route('/docentes/<int:id>', methods=['PUT'])
@swag_from({
    'tags': ['Docentes'],
    'summary': 'Actualizar un docente'
})
def update_docente(id):
    """Actualizar un docente existente"""
    docente = Docente.query.get(id)
    if not docente:
        return jsonify({'error': 'Docente no encontrado'}), 404
    
    data = request.get_json()
    
    if data.get('nombre'):
        docente.nombre = data['nombre'].strip()
    
    if data.get('email'):
        existe = Docente.query.filter(
            Docente.email == data['email'].strip().lower(),
            Docente.id != id
        ).first()
        if existe:
            return jsonify({'error': 'El email ya está registrado'}), 400
        docente.email = data['email'].strip().lower()
    
    if data.get('especialidad') is not None:
        docente.especialidad = data['especialidad'].strip()
    
    db.session.commit()
    
    return jsonify(docente.to_dict())


@api_bp.route('/docentes/<int:id>', methods=['DELETE'])
@swag_from({
    'tags': ['Docentes'],
    'summary': 'Eliminar un docente'
})
def delete_docente(id):
    """Eliminar un docente"""
    docente = Docente.query.get(id)
    if not docente:
        return jsonify({'error': 'Docente no encontrado'}), 404
    
    # Verificar si tiene cursos asignados
    if docente.cursos:
        return jsonify({'error': 'No se puede eliminar un docente con cursos asignados'}), 400
    
    db.session.delete(docente)
    db.session.commit()
    
    return jsonify({'mensaje': 'Docente eliminado exitosamente'})


# ============================================================================
# ENDPOINTS DE CURSOS
# ============================================================================

@api_bp.route('/cursos', methods=['GET'])
@swag_from({
    'tags': ['Cursos'],
    'summary': 'Obtener todos los cursos',
    'description': 'Retorna todos los cursos con información del docente'
})
def get_cursos():
    """Obtener todos los cursos"""
    cursos = Curso.query.all()
    return jsonify([c.to_dict() for c in cursos])


@api_bp.route('/cursos/<int:id>', methods=['GET'])
@swag_from({
    'tags': ['Cursos'],
    'summary': 'Obtener un curso por ID'
})
def get_curso(id):
    """Obtener un curso por ID"""
    curso = Curso.query.get(id)
    if not curso:
        return jsonify({'error': 'Curso no encontrado'}), 404
    return jsonify(curso.to_dict())


@api_bp.route('/cursos', methods=['POST'])
@swag_from({
    'tags': ['Cursos'],
    'summary': 'Crear un nuevo curso',
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'required': ['nombre', 'docente_id'],
                'properties': {
                    'nombre': {'type': 'string', 'example': 'Cálculo I'},
                    'descripcion': {'type': 'string', 'example': 'Introducción al cálculo diferencial'},
                    'creditos': {'type': 'integer', 'example': 4},
                    'docente_id': {'type': 'integer', 'example': 1}
                }
            }
        }
    ]
})
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
        nombre=data['nombre'].strip(),
        descripcion=data.get('descripcion', '').strip(),
        creditos=data.get('creditos', 3),
        docente_id=data['docente_id']
    )
    
    db.session.add(curso)
    db.session.commit()
    
    return jsonify(curso.to_dict()), 201


@api_bp.route('/cursos/<int:id>', methods=['PUT'])
@swag_from({
    'tags': ['Cursos'],
    'summary': 'Actualizar un curso'
})
def update_curso(id):
    """Actualizar un curso existente"""
    curso = Curso.query.get(id)
    if not curso:
        return jsonify({'error': 'Curso no encontrado'}), 404
    
    data = request.get_json()
    
    if data.get('nombre'):
        curso.nombre = data['nombre'].strip()
    
    if data.get('descripcion') is not None:
        curso.descripcion = data['descripcion'].strip()
    
    if data.get('creditos'):
        curso.creditos = data['creditos']
    
    if data.get('docente_id'):
        docente = Docente.query.get(data['docente_id'])
        if not docente:
            return jsonify({'error': 'Docente no encontrado'}), 404
        curso.docente_id = data['docente_id']
    
    db.session.commit()
    
    return jsonify(curso.to_dict())


@api_bp.route('/cursos/<int:id>', methods=['DELETE'])
@swag_from({
    'tags': ['Cursos'],
    'summary': 'Eliminar un curso'
})
def delete_curso(id):
    """Eliminar un curso"""
    curso = Curso.query.get(id)
    if not curso:
        return jsonify({'error': 'Curso no encontrado'}), 404
    
    # Verificar si tiene matrículas activas
    if curso.matriculas:
        return jsonify({'error': 'No se puede eliminar un curso con matrículas activas'}), 400
    
    db.session.delete(curso)
    db.session.commit()
    
    return jsonify({'mensaje': 'Curso eliminado exitosamente'})


# ============================================================================
# ENDPOINTS DE MATRÍCULAS
# ============================================================================

@api_bp.route('/matriculas', methods=['GET'])
@swag_from({
    'tags': ['Matrículas'],
    'summary': 'Obtener todas las matrículas'
})
def get_matriculas():
    """Obtener todas las matrículas"""
    matriculas = Matricula.query.all()
    return jsonify([m.to_dict() for m in matriculas])


@api_bp.route('/matriculas/<int:id>', methods=['GET'])
@swag_from({
    'tags': ['Matrículas'],
    'summary': 'Obtener una matrícula por ID'
})
def get_matricula(id):
    """Obtener una matrícula por ID"""
    matricula = Matricula.query.get(id)
    if not matricula:
        return jsonify({'error': 'Matrícula no encontrada'}), 404
    return jsonify(matricula.to_dict())


@api_bp.route('/matriculas', methods=['POST'])
@swag_from({
    'tags': ['Matrículas'],
    'summary': 'Crear una nueva matrícula',
    'description': 'Inscribe un estudiante en un curso',
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'required': ['estudiante_id', 'curso_id'],
                'properties': {
                    'estudiante_id': {'type': 'integer', 'example': 1},
                    'curso_id': {'type': 'integer', 'example': 1},
                    'estado': {'type': 'string', 'example': 'activa'}
                }
            }
        }
    ]
})
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


@api_bp.route('/matriculas/<int:id>', methods=['PUT'])
@swag_from({
    'tags': ['Matrículas'],
    'summary': 'Actualizar una matrícula (ej. cambiar estado)'
})
def update_matricula(id):
    """Actualizar una matrícula existente"""
    matricula = Matricula.query.get(id)
    if not matricula:
        return jsonify({'error': 'Matrícula no encontrada'}), 404
    
    data = request.get_json()
    
    if data.get('estado'):
        estados_validos = ['activa', 'cancelada', 'completada']
        if data['estado'] not in estados_validos:
            return jsonify({'error': f'Estado debe ser uno de: {estados_validos}'}), 400
        matricula.estado = data['estado']
    
    db.session.commit()
    
    return jsonify(matricula.to_dict())


@api_bp.route('/matriculas/<int:id>', methods=['DELETE'])
@swag_from({
    'tags': ['Matrículas'],
    'summary': 'Eliminar una matrícula'
})
def delete_matricula(id):
    """Eliminar una matrícula"""
    matricula = Matricula.query.get(id)
    if not matricula:
        return jsonify({'error': 'Matrícula no encontrada'}), 404
    
    db.session.delete(matricula)
    db.session.commit()
    
    return jsonify({'mensaje': 'Matrícula eliminada exitosamente'})


# ============================================================================
# ENDPOINTS DE CALIFICACIONES
# ============================================================================

@api_bp.route('/calificaciones', methods=['GET'])
@swag_from({
    'tags': ['Calificaciones'],
    'summary': 'Obtener todas las calificaciones'
})
def get_calificaciones():
    """Obtener todas las calificaciones"""
    calificaciones = Calificacion.query.all()
    return jsonify([c.to_dict() for c in calificaciones])


@api_bp.route('/calificaciones/<int:id>', methods=['GET'])
@swag_from({
    'tags': ['Calificaciones'],
    'summary': 'Obtener una calificación por ID'
})
def get_calificacion(id):
    """Obtener una calificación por ID"""
    calificacion = Calificacion.query.get(id)
    if not calificacion:
        return jsonify({'error': 'Calificación no encontrada'}), 404
    return jsonify(calificacion.to_dict())


@api_bp.route('/calificaciones', methods=['POST'])
@swag_from({
    'tags': ['Calificaciones'],
    'summary': 'Registrar una nueva calificación',
    'description': 'Asigna una nota a una matrícula existente',
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'required': ['matricula_id', 'nota'],
                'properties': {
                    'matricula_id': {'type': 'integer', 'example': 1},
                    'nota': {'type': 'number', 'example': 8.5},
                    'observaciones': {'type': 'string', 'example': 'Buen trabajo'}
                }
            }
        }
    ]
})
def create_calificacion():
    """Crear una nueva calificación"""
    data = request.get_json()
    
    if not data or not data.get('matricula_id') or data.get('nota') is None:
        return jsonify({'error': 'Faltan datos requeridos'}), 400
    
    # Validar que la nota esté entre 0 y 10
    try:
        nota = float(data['nota'])
    except (ValueError, TypeError):
        return jsonify({'error': 'La nota debe ser un número'}), 400
    
    if nota < 0 or nota > 10:
        return jsonify({'error': 'La nota debe estar entre 0 y 10'}), 400
    
    # Verificar que la matrícula existe
    matricula = Matricula.query.get(data['matricula_id'])
    if not matricula:
        return jsonify({'error': 'Matrícula no encontrada'}), 404
    
    # Verificar que la matrícula está activa
    if matricula.estado != 'activa':
        return jsonify({'error': 'Solo se pueden calificar matrículas activas'}), 400
    
    calificacion = Calificacion(
        matricula_id=data['matricula_id'],
        nota=nota,
        observaciones=data.get('observaciones', '').strip()
    )
    
    db.session.add(calificacion)
    db.session.commit()
    
    return jsonify(calificacion.to_dict()), 201


@api_bp.route('/calificaciones/<int:id>', methods=['PUT'])
@swag_from({
    'tags': ['Calificaciones'],
    'summary': 'Actualizar una calificación'
})
def update_calificacion(id):
    """Actualizar una calificación existente"""
    calificacion = Calificacion.query.get(id)
    if not calificacion:
        return jsonify({'error': 'Calificación no encontrada'}), 404
    
    data = request.get_json()
    
    if data.get('nota') is not None:
        try:
            nota = float(data['nota'])
        except (ValueError, TypeError):
            return jsonify({'error': 'La nota debe ser un número'}), 400
        
        if nota < 0 or nota > 10:
            return jsonify({'error': 'La nota debe estar entre 0 y 10'}), 400
        calificacion.nota = nota
    
    if data.get('observaciones') is not None:
        calificacion.observaciones = data['observaciones'].strip()
    
    db.session.commit()
    
    return jsonify(calificacion.to_dict())


@api_bp.route('/calificaciones/<int:id>', methods=['DELETE'])
@swag_from({
    'tags': ['Calificaciones'],
    'summary': 'Eliminar una calificación'
})
def delete_calificacion(id):
    """Eliminar una calificación"""
    calificacion = Calificacion.query.get(id)
    if not calificacion:
        return jsonify({'error': 'Calificación no encontrada'}), 404
    
    db.session.delete(calificacion)
    db.session.commit()
    
    return jsonify({'mensaje': 'Calificación eliminada exitosamente'})


# ============================================================================
# ENDPOINTS DE BÚSQUEDA Y REPORTES
# ============================================================================

@api_bp.route('/estudiantes/<int:id>/cursos', methods=['GET'])
@swag_from({
    'tags': ['Reportes'],
    'summary': 'Obtener cursos de un estudiante',
    'description': 'Retorna todos los cursos en los que está matriculado un estudiante'
})
def get_cursos_estudiante(id):
    """Obtener cursos de un estudiante específico"""
    estudiante = Estudiante.query.get(id)
    if not estudiante:
        return jsonify({'error': 'Estudiante no encontrado'}), 404
    
    cursos = []
    for matricula in estudiante.matriculas:
        curso_info = matricula.curso.to_dict()
        curso_info['estado_matricula'] = matricula.estado
        curso_info['fecha_matricula'] = matricula.fecha_matricula.strftime('%Y-%m-%d %H:%M:%S')
        
        # Agregar calificaciones si existen
        if matricula.calificaciones:
            curso_info['calificaciones'] = [c.to_dict() for c in matricula.calificaciones]
        
        cursos.append(curso_info)
    
    return jsonify(cursos)


@api_bp.route('/cursos/<int:id>/estudiantes', methods=['GET'])
@swag_from({
    'tags': ['Reportes'],
    'summary': 'Obtener estudiantes de un curso',
    'description': 'Retorna todos los estudiantes matriculados en un curso'
})
def get_estudiantes_curso(id):
    """Obtener estudiantes de un curso específico"""
    curso = Curso.query.get(id)
    if not curso:
        return jsonify({'error': 'Curso no encontrado'}), 404
    
    estudiantes = []
    for matricula in curso.matriculas:
        estudiante_info = matricula.estudiante.to_dict()
        estudiante_info['estado_matricula'] = matricula.estado
        estudiante_info['fecha_matricula'] = matricula.fecha_matricula.strftime('%Y-%m-%d %H:%M:%S')
        
        # Agregar calificaciones si existen
        if matricula.calificaciones:
            estudiante_info['calificaciones'] = [c.to_dict() for c in matricula.calificaciones]
            # Calcular promedio
            promedio = sum(c.nota for c in matricula.calificaciones) / len(matricula.calificaciones)
            estudiante_info['promedio'] = round(promedio, 2)
        
        estudiantes.append(estudiante_info)
    
    return jsonify(estudiantes)


@api_bp.route('/reportes/promedios', methods=['GET'])
@swag_from({
    'tags': ['Reportes'],
    'summary': 'Reporte de promedios por curso',
    'description': 'Calcula el promedio de calificaciones por cada curso'
})
def reporte_promedios():
    """Generar reporte de promedios por curso"""
    cursos = Curso.query.all()
    reporte = []
    
    for curso in cursos:
        calificaciones = []
        for matricula in curso.matriculas:
            for calif in matricula.calificaciones:
                calificaciones.append(calif.nota)
        
        if calificaciones:
            promedio = sum(calificaciones) / len(calificaciones)
            reporte.append({
                'curso_id': curso.id,
                'curso_nombre': curso.nombre,
                'docente': curso.docente.nombre if curso.docente else 'N/A',
                'total_estudiantes': len(curso.matriculas),
                'total_calificaciones': len(calificaciones),
                'promedio_general': round(promedio, 2),
                'nota_minima': min(calificaciones),
                'nota_maxima': max(calificaciones)
            })
    
    return jsonify(reporte)


# ============================================================================
# ENDPOINT DE BIENVENIDA
# ============================================================================

@api_bp.route('/', methods=['GET'])
@swag_from({
    'tags': ['Sistema'],
    'summary': 'Información de la API',
    'description': 'Retorna información básica sobre la API y sus endpoints'
})
def index():
    """Endpoint de bienvenida"""
    return jsonify({
        'nombre': 'API de Gestión Académica',
        'version': '1.0.0',
        'descripcion': 'Sistema para administrar estudiantes, docentes, cursos, matrículas y calificaciones',
        'documentacion': '/docs/',
        'endpoints_disponibles': {
            'estudiantes': '/api/estudiantes',
            'docentes': '/api/docentes',
            'cursos': '/api/cursos',
            'matriculas': '/api/matriculas',
            'calificaciones': '/api/calificaciones',
            'reportes': {
                'cursos_por_estudiante': '/api/estudiantes/{id}/cursos',
                'estudiantes_por_curso': '/api/cursos/{id}/estudiantes',
                'promedios': '/api/reportes/promedios'
            }
        },
        'fecha': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    })