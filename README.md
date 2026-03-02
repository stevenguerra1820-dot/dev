# Plataforma Web de Gestión Académica

Proyecto final de desarrollo de software que implementa una plataforma para gestión académica con integración de prácticas DevOps.

## Descripción

Sistema para administrar:
- Estudiantes
- Docentes
- Cursos
- Matrículas
- Calificaciones

## Tecnologías Principales
- Backend: Python con Flask
- Base de datos: PostgreSQL
- Contenedores: Docker
- CI/CD: GitHub Actions
- Pruebas: Pytest

## Estado del Proyecto
🚧 En construcción - Fase inicial

## Instalación y Configuración

### Requisitos Previos
- Python 3.8 o superior
- pip (gestor de paquetes de Python)
- Git

### Pasos para ejecutar localmente

1. Clonar el repositorio:
   ```bash
   git clone https://github.com/tu-usuario/plataforma-gestion-academica.git
   cd plataforma-gestion-academica

   ### Paso 13: Crear archivo de ejemplo para variables de entorno

Crea `.env.example` (sin datos sensibles):

```env
# Configuración de Flask
FLASK_APP=app
FLASK_ENV=development
SECRET_KEY=tu-clave-secreta-aqui

# Base de datos (SQLite para desarrollo)
DATABASE_URL=sqlite:///academica.db

## Ejecución con Docker

### Requisitos Previos
- Docker
- Docker Compose

### Pasos para ejecutar con Docker

1. Clonar el repositorio:
   ```bash
   git clone <url-repositorio>
   cd plataforma-gestion-academica