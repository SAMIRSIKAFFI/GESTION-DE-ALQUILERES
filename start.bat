@echo off
REM Script de Inicio Rápido para Windows
REM Sistema de Gestión de Alquileres

echo 🏢 Sistema de Gestión de Alquileres - Inicio Rápido
echo ==================================================
echo.

REM Verificar si Docker está instalado
docker --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Error: Docker no está instalado
    echo Por favor instala Docker Desktop desde: https://docs.docker.com/desktop/windows/install/
    pause
    exit /b 1
)

docker-compose --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Error: Docker Compose no está instalado
    echo Por favor instala Docker Compose
    pause
    exit /b 1
)

echo ✅ Docker y Docker Compose están instalados
echo.

REM Verificar si existe .env
if not exist .env (
    echo ⚙️  Creando archivo .env desde .env.example...
    copy .env.example .env
    echo ✅ Archivo .env creado
    echo ⚠️  IMPORTANTE: Edita el archivo .env con tus configuraciones
    echo.
)

REM Detener contenedores existentes
echo 🛑 Deteniendo contenedores existentes si los hay...
docker-compose down

REM Iniciar servicios
echo.
echo 🚀 Iniciando servicios con Docker Compose...
docker-compose up -d

REM Esperar a que la base de datos esté lista
echo.
echo ⏳ Esperando a que la base de datos esté lista...
timeout /t 10 /nobreak

REM Verificar estado
echo.
echo 📊 Estado de los servicios:
docker-compose ps

echo.
echo ✅ ¡Sistema iniciado correctamente!
echo.
echo 📍 Accesos:
echo    - API: http://localhost:8000
echo    - Documentación: http://localhost:8000/docs
echo    - PgAdmin: http://localhost:5050
echo.
echo 🔐 Credenciales PgAdmin:
echo    - Email: admin@alquileres.com
echo    - Password: admin123
echo.
echo 📝 Próximos pasos:
echo    1. Abre http://localhost:8000/docs en tu navegador
echo    2. Usa el endpoint /api/v1/auth/register para crear un usuario
echo    3. ¡Comienza a usar el sistema!
echo.
echo 📋 Ver logs: docker-compose logs -f
echo 🛑 Detener: docker-compose down
echo.
pause
