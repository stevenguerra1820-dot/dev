#!/bin/bash
# run_tests.sh

echo "🧪 Ejecutando pruebas unitarias y de integración..."
echo "================================================"

# Ejecutar pruebas con cobertura
pytest --cov=app --cov-report=term --cov-report=html tests/

# Mostrar resultado
if [ $? -eq 0 ]; then
    echo "✅ ¡Todas las pruebas pasaron!"
    echo "📊 Reporte de cobertura generado en htmlcov/"
else
    echo "❌ Algunas pruebas fallaron"
    exit 1
fi