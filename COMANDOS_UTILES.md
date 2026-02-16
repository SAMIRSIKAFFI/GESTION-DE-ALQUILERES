# 🛠️ Comandos Útiles - Sistema de Alquileres

## 🚀 Inicio y Control

### Iniciar el sistema
```bash
docker-compose up -d
```

### Ver logs en tiempo real
```bash
docker-compose logs -f
```

### Ver logs solo de la API
```bash
docker-compose logs -f api
```

### Detener el sistema
```bash
docker-compose down
```

### Reiniciar el sistema
```bash
docker-compose restart
```

### Detener y eliminar todo (incluyendo base de datos)
```bash
docker-compose down -v
```

## 🔍 Inspección

### Ver contenedores activos
```bash
docker-compose ps
```

### Ver uso de recursos
```bash
docker stats
```

### Entrar a la consola de la API
```bash
docker-compose exec api bash
```

### Entrar a PostgreSQL
```bash
docker-compose exec db psql -U postgres -d alquileres_db
```

## 🗄️ Base de Datos

### Hacer backup de la base de datos
```bash
docker-compose exec db pg_dump -U postgres alquileres_db > backup.sql
```

### Restaurar backup
```bash
cat backup.sql | docker-compose exec -T db psql -U postgres alquileres_db
```

### Conectar con psql
```bash
docker-compose exec db psql -U postgres -d alquileres_db
```

### Comandos SQL útiles dentro de psql:
```sql
-- Ver todas las tablas
\dt

-- Describir una tabla
\d propiedades

-- Ver copropietarios
SELECT * FROM copropietarios;

-- Ver pagos con mora
SELECT id, periodo, monto_esperado, monto_pagado, mora_calculada, dias_atraso 
FROM pagos 
WHERE mora_calculada > 0;

-- Ver distribuciones pendientes
SELECT c.nombre, d.monto_asignado, d.estado 
FROM distribuciones_pago d
JOIN copropietarios c ON d.copropietario_id = c.id
WHERE d.estado = 'pendiente';

-- Salir
\q
```

## 📊 Monitoreo

### Ver tamaño de la base de datos
```bash
docker-compose exec db psql -U postgres -d alquileres_db -c "SELECT pg_size_pretty(pg_database_size('alquileres_db'));"
```

### Ver número de registros por tabla
```bash
docker-compose exec db psql -U postgres -d alquileres_db -c "
SELECT 
  schemaname,
  tablename,
  n_tup_ins - n_tup_del as row_count
FROM pg_stat_user_tables
ORDER BY row_count DESC;
"
```

## 🧪 Testing

### Ejecutar tests (cuando estén implementados)
```bash
docker-compose exec api pytest tests/
```

### Ejecutar tests con cobertura
```bash
docker-compose exec api pytest --cov=app tests/
```

## 🔐 Seguridad

### Ver usuarios activos
```bash
curl -X GET http://localhost:8000/api/v1/users \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Cambiar contraseña de BD (editar .env y reiniciar)
```bash
nano .env
docker-compose down
docker-compose up -d
```

## 📝 Desarrollo

### Ver estructura del proyecto
```bash
tree -L 3 -I '__pycache__|*.pyc'
```

### Buscar en el código
```bash
grep -r "mora_calculator" app/
```

### Contar líneas de código
```bash
find app/ -name "*.py" -exec wc -l {} + | sort -n
```

### Formatear código con black
```bash
docker-compose exec api black app/
```

## 🌐 API Testing

### Health check
```bash
curl http://localhost:8000/health
```

### Registrar usuario
```bash
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "full_name": "Test User",
    "password": "password123"
  }'
```

### Login y obtener token
```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "password123"
  }'
```

### Guardar token en variable (Linux/Mac)
```bash
export TOKEN=$(curl -s -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"password123"}' \
  | jq -r '.access_token')
```

### Usar token en peticiones
```bash
curl -X GET http://localhost:8000/api/v1/propiedades \
  -H "Authorization: Bearer $TOKEN"
```

## 🔧 Mantenimiento

### Limpiar contenedores no usados
```bash
docker system prune -a
```

### Ver espacio usado por Docker
```bash
docker system df
```

### Actualizar imagen base
```bash
docker-compose pull
docker-compose up -d --build
```

### Rebuild completo
```bash
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

## 📦 Git

### Ver estado
```bash
git status
```

### Agregar cambios
```bash
git add .
```

### Commit
```bash
git commit -m "Descripción del cambio"
```

### Push a GitHub
```bash
git push origin main
```

### Pull últimos cambios
```bash
git pull origin main
```

### Ver diferencias
```bash
git diff
```

### Ver historial
```bash
git log --oneline -10
```

## 🎯 Atajos Útiles

### Script todo-en-uno (Linux/Mac)
```bash
# Crear archivo start.sh
./start.sh
```

### Script todo-en-uno (Windows)
```bash
start.bat
```

### Alias útiles (agregar a ~/.bashrc o ~/.zshrc)
```bash
alias alq-start='docker-compose up -d'
alias alq-stop='docker-compose down'
alias alq-logs='docker-compose logs -f'
alias alq-api='docker-compose exec api bash'
alias alq-db='docker-compose exec db psql -U postgres -d alquileres_db'
```

## 📱 Accesos Rápidos

- API: http://localhost:8000
- Documentación: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- PgAdmin: http://localhost:5050
- Health Check: http://localhost:8000/health

## 🆘 Solución de Problemas

### Puerto 8000 ya en uso
```bash
# Ver qué está usando el puerto
lsof -i :8000

# Matar el proceso
kill -9 PID
```

### Base de datos no responde
```bash
docker-compose restart db
docker-compose logs db
```

### Resetear todo
```bash
docker-compose down -v
docker-compose up -d
```

### Ver logs de errores
```bash
docker-compose logs api | grep ERROR
```

---

**💡 Tip**: Guarda estos comandos en favoritos o imprímelos para referencia rápida.
