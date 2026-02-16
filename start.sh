#!/bin/bash

# Script de Inicio Rápido
# Sistema de Gestión de Alquileres

echo "🏢 Sistema de Gestión de Alquileres - Inicio Rápido"
echo "=================================================="
echo ""

# Verificar si Docker está instalado
if ! command -v docker &> /dev/null; then
    echo "❌ Error: Docker no está instalado"
    echo "Por favor instala Docker desde: https://docs.docker.com/get-docker/"
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ Error: Docker Compose no está instalado"
    echo "Por favor instala Docker Compose desde: https://docs.docker.com/compose/install/"
    exit 1
fi

echo "✅ Docker y Docker Compose están instalados"
echo ""

# Verificar si existe .env
if [ ! -f .env ]; then
    echo "⚙️  Creando archivo .env desde .env.example..."
    cp .env.example .env
    echo "✅ Archivo .env creado"
    echo "⚠️  IMPORTANTE: Edita el archivo .env con tus configuraciones"
    echo ""
fi

# Detener contenedores existentes
echo "🛑 Deteniendo contenedores existentes (si los hay)..."
docker-compose down

# Iniciar servicios
echo ""
echo "🚀 Iniciando servicios con Docker Compose..."
docker-compose up -d

# Esperar a que la base de datos esté lista
echo ""
echo "⏳ Esperando a que la base de datos esté lista..."
sleep 10

# Verificar estado
echo ""
echo "📊 Estado de los servicios:"
docker-compose ps

echo ""
echo "✅ ¡Sistema iniciado correctamente!"
echo ""
echo "📍 Accesos:"
echo "   - API: http://localhost:8000"
echo "   - Documentación: http://localhost:8000/docs"
echo "   - PgAdmin: http://localhost:5050"
echo ""
echo "🔐 Credenciales PgAdmin:"
echo "   - Email: admin@alquileres.com"
echo "   - Password: admin123"
echo ""
echo "📝 Próximos pasos:"
echo "   1. Abre http://localhost:8000/docs en tu navegador"
echo "   2. Usa el endpoint /api/v1/auth/register para crear un usuario"
echo "   3. ¡Comienza a usar el sistema!"
echo ""
echo "📋 Ver logs: docker-compose logs -f"
echo "🛑 Detener: docker-compose down"
echo ""
