# 🏢 Sistema de Gestión de Alquileres - Bolivia

Sistema profesional de gestión de alquileres con soporte para **copropiedades** y **sistema tributario boliviano** (IVA, IT, RC-IVA).

[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104-green.svg)](https://fastapi.tiangolo.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue.svg)](https://www.postgresql.org/)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://www.docker.com/)

---

## ✨ Características Principales

### 🏠 Gestión de Propiedades
- ✅ Propiedades **100% propias**
- ✅ Propiedades en **copropiedad** con múltiples copropietarios
- ✅ Porcentajes de participación personalizables
- ✅ Datos bancarios de cada copropietario
- ✅ Validación automática: porcentajes deben sumar 100%

### 👥 Gestión de Inquilinos
- ✅ Registro completo de datos personales
- ✅ Historial de contratos
- ✅ Estados: activo/inactivo

### 📄 Contratos de Alquiler
- ✅ Canon mensual configurable
- ✅ Garantía (depósito)
- ✅ Incremento anual automático
- ✅ Día de pago personalizable
- ✅ Tasa de mora diaria según normativa boliviana
- ✅ Estados: activo/vencido/cancelado

### 💰 Pagos con Distribución Automática
- ✅ Registro de pagos mensuales
- ✅ **Distribución AUTOMÁTICA** a copropietarios según porcentaje
- ✅ Cálculo automático de mora por días de atraso
- ✅ Múltiples formas de pago (transferencia, efectivo, QR, etc.)
- ✅ Visualización clara de cuentas bancarias de cada copropietario

### 💼 Sistema Tributario Boliviano

#### IVA 13% (Mensual)
- **Determinado:** Alquiler × 13%
- **Compensable:** Con facturas hasta **30% del monto del alquiler**
- **Efectivo:** Determinado - Facturas aplicadas

#### IT 3% (Mensual)
- **Determinado:** Alquiler × 3%
- **Compensable:** ❌ NO (siempre se paga el total)
- **Efectivo:** Igual al determinado

#### RC-IVA 12.5% (Trimestral)
- **Determinado:** Acumulado trimestre × 12.5%
- **Compensable:** ✅ SÍ, hasta el **100%** con facturas
- **Efectivo:** Determinado - Facturas aplicadas
- **Meses de cierre:** Marzo, Junio, Septiembre, Diciembre

**El sistema muestra SIEMPRE:**
- 💵 Impuesto DETERMINADO (lo que exige la ley)
- 💸 Impuesto EFECTIVO (lo que realmente pagas con facturas)
- 💚 Ahorro con facturas
- 📊 Neto a distribuir entre copropietarios

### 📊 Reportes y Estadísticas
- ✅ Dashboard con KPIs principales
- ✅ Ingresos mensuales y anuales
- ✅ Reporte de morosidad
- ✅ Resumen anual de impuestos por contrato
- ✅ Rendimiento por propiedad

---

## 🏗️ Arquitectura del Sistema

```
├── Backend (FastAPI + PostgreSQL)
│   ├── API REST con documentación Swagger
│   ├── Autenticación JWT
│   ├── ORM SQLAlchemy
│   └── Migraciones con Alembic
│
├── Frontend (HTML + React + TailwindCSS)
│   ├── Interfaz moderna y responsive
│   ├── Formularios intuitivos
│   ├── Tablas interactivas
│   └── Visualización de distribuciones
│
└── Base de Datos (PostgreSQL)
    ├── 10 tablas relacionadas
    ├── Enums para estados
    └── Soft deletes
```

---

## 🚀 Instalación y Uso

### Requisitos Previos
- Docker Desktop
- Git

### 1️⃣ Clonar el Repositorio

```bash
git clone https://github.com/SAMIRSIKAFFI/GESTION-DE-ALQUILERES.git
cd GESTION-DE-ALQUILERES
```

### 2️⃣ Configurar Variables de Entorno

Crea un archivo `.env` en la raíz:

```env
DATABASE_URL=postgresql://postgres:Samir2026Bolivia@db:5432/alquileres_db
SECRET_KEY=alquileres_samir_2026_la_paz_bolivia_secreto_12345
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
APP_NAME=Sistema de Gestión de Alquileres
APP_VERSION=1.0.0
ENVIRONMENT=development
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8000
TIMEZONE=America/La_Paz
```

### 3️⃣ Iniciar el Sistema

```bash
docker-compose up -d --build
```

**Espera 2-3 minutos mientras se construyen los contenedores.**

### 4️⃣ Acceder a la Aplicación

#### 🎨 Interfaz Visual (Recomendado)
```
http://localhost:8000/app
```

#### 📚 API Swagger (Desarrolladores)
```
http://localhost:8000/docs
```

#### 🗄️ pgAdmin (Administrador de BD)
```
http://localhost:5050
Email: admin@alquileres.com
Password: admin
```

---

## 📖 Guía de Uso

### 1️⃣ Crear tu cuenta

1. Abre `http://localhost:8000/app`
2. Haz clic en **"Regístrate"**
3. Completa:
   - Nombre completo
   - Email
   - Contraseña
4. Haz clic en **"Registrarse"**

### 2️⃣ Crear una Propiedad con Copropiedad

1. Ve a la pestaña **"🏠 Propiedades"**
2. Haz clic en **"+ Nueva Propiedad"**
3. Llena los datos básicos:
   - Dirección
   - Ciudad
   - Tipo: **Copropiedad** ← Importante
   - Canon base
4. Agrega copropietarios:
   - Nombre completo
   - CI
   - % Participación (ejemplo: 60% y 40%)
   - Cuenta bancaria
   - Banco
5. **El sistema valida automáticamente que sumen 100%**
6. Haz clic en **"Crear Propiedad"**

### 3️⃣ Registrar un Pago

1. Ve a **"💰 Pagos"**
2. Selecciona el contrato
3. Haz clic en **"+ Crear Pago Pendiente"**
4. Completa:
   - Periodo: `2026-02`
   - Fecha vencimiento
   - Monto esperado
5. Cuando el inquilino pague, haz clic en **"Registrar Pago"**
6. **¡El sistema muestra AUTOMÁTICAMENTE la distribución!**

```
✅ PAGO REGISTRADO

🎉 Distribución Automática:

┌─────────────────────────────────┐
│ SAMIR SIKAFFI                   │
│ 60% = Bs. 1,800                │
│ Banco: BNB                      │
│ Cuenta: 1001234567              │
└─────────────────────────────────┘

┌─────────────────────────────────┐
│ SOCIO                           │
│ 40% = Bs. 1,200                │
│ Banco: Mercantil                │
│ Cuenta: 9876543                 │
└─────────────────────────────────┘
```

### 4️⃣ Calcular Impuestos

**Opción A - En la aplicación web:**
*(Próximamente integrado en el flujo de pagos)*

**Opción B - Via API Swagger:**

1. Abre `http://localhost:8000/docs`
2. Autentícate con tu token
3. Ve a **"Impuestos"** → `POST /api/v1/impuestos/calcular`
4. Ingresa:
   ```json
   {
     "monto_alquiler": 3000,
     "mes": 2,
     "anio": 2026,
     "facturas_iva": 300,
     "facturas_rc_iva": 0
   }
   ```
5. **Verás:**
   ```
   IVA Determinado: Bs. 390
   IVA Efectivo:    Bs. 90  (ahorraste Bs. 300)
   
   IT Determinado:  Bs. 90
   IT Efectivo:     Bs. 90  (no compensable)
   
   TOTAL:
   Determinado:     Bs. 480
   Efectivo:        Bs. 180
   Neto distribuir: Bs. 2,820
   ```

---

## 🔧 Comandos Útiles

### Ver logs de la API
```bash
docker-compose logs api --tail 50
```

### Reiniciar servicios
```bash
docker-compose restart
```

### Detener todo
```bash
docker-compose down
```

### Reconstruir desde cero
```bash
docker-compose down -v
docker-compose up -d --build
```

### Acceder a la base de datos
```bash
docker exec -it alquileres_db psql -U postgres -d alquileres_db
```

---

## 📊 Estructura de la Base de Datos

### Tablas Principales

```sql
usuarios
  ├── id, email, password_hash, full_name
  └── created_at, updated_at, deleted_at

propiedades
  ├── id, direccion, ciudad, tipo (propia/copropiedad)
  ├── canon_base, superficie, dormitorios, banos
  └── numero_copropietarios

copropietarios
  ├── id, propiedad_id
  ├── nombre, ci, telefono, email
  ├── porcentaje_participacion (validado: suma 100%)
  └── cuenta_bancaria, banco, tipo_cuenta

inquilinos
  ├── id, nombre_completo, ci, telefono, email
  └── estado (activo/inactivo)

contratos
  ├── id, numero_contrato
  ├── propiedad_id, inquilino_id
  ├── fecha_inicio, fecha_fin
  ├── canon_mensual, garantia
  ├── incremento_anual, dia_pago, tasa_mora_diaria
  └── estado (activo/vencido/cancelado)

pagos
  ├── id, contrato_id, periodo, fecha_vencimiento
  ├── monto_esperado, monto_pagado
  ├── mora_calculada, dias_atraso
  └── estado (pendiente/pagado/vencido)

distribucion_pagos
  ├── id, pago_id, copropietario_id
  ├── porcentaje, monto_distribuido
  └── cuenta_bancaria, banco

impuestos_alquiler
  ├── id, pago_id, contrato_id
  ├── IVA (determinado, efectivo, ahorro)
  ├── IT (determinado, efectivo)
  ├── RC-IVA (determinado, efectivo, ahorro)
  └── total_determinado, total_efectivo, neto_distribuir

facturas_compensacion
  ├── id, contrato_id, impuesto_id
  ├── numero_factura, fecha, monto
  └── tipo_impuesto (iva/rc_iva)
```

---

## 🌐 API Endpoints

### Autenticación
```
POST   /api/v1/auth/register     - Registrar usuario
POST   /api/v1/auth/login        - Iniciar sesión
```

### Propiedades
```
POST   /api/v1/propiedades       - Crear propiedad
GET    /api/v1/propiedades       - Listar propiedades
GET    /api/v1/propiedades/{id}  - Obtener propiedad
PUT    /api/v1/propiedades/{id}  - Actualizar propiedad
DELETE /api/v1/propiedades/{id}  - Eliminar propiedad
```

### Inquilinos
```
POST   /api/v1/inquilinos        - Crear inquilino
GET    /api/v1/inquilinos        - Listar inquilinos
GET    /api/v1/inquilinos/{id}   - Obtener inquilino
PUT    /api/v1/inquilinos/{id}   - Actualizar inquilino
DELETE /api/v1/inquilinos/{id}   - Eliminar inquilino
```

### Contratos
```
POST   /api/v1/contratos         - Crear contrato
GET    /api/v1/contratos         - Listar contratos
GET    /api/v1/contratos/{id}    - Obtener contrato
PUT    /api/v1/contratos/{id}    - Actualizar contrato
DELETE /api/v1/contratos/{id}    - Eliminar contrato
```

### Pagos
```
POST   /api/v1/pagos                        - Crear pago pendiente
POST   /api/v1/pagos/{id}/registrar         - Registrar pago (distribución automática)
GET    /api/v1/pagos/contrato/{contrato_id} - Pagos de un contrato
```

### Impuestos ⭐ NUEVO
```
POST   /api/v1/impuestos/calcular                      - Calcular impuestos (preview)
POST   /api/v1/impuestos/calcular/sin-facturas         - Ver determinado puro
POST   /api/v1/impuestos/registrar                     - Guardar impuestos en BD
GET    /api/v1/impuestos/contrato/{id}/anio/{anio}     - Resumen anual
```

### Reportes
```
GET    /api/v1/reportes/dashboard?anio=2026  - Dashboard con KPIs
GET    /api/v1/reportes/morosidad            - Reporte de mora
```

---

## 💡 Casos de Uso Reales

### Caso 1: Propiedad 100% Tuya
```
Alquiler: Bs. 4,000
Sin copropietarios
→ Todo el dinero es tuyo
```

### Caso 2: Copropiedad 60/40
```
Alquiler: Bs. 3,000
Samir: 60% → Bs. 1,800
Socio: 40% → Bs. 1,200

El sistema calcula y muestra automáticamente
las cuentas bancarias de cada uno.
```

### Caso 3: Mes con RC-IVA (Marzo)
```
Alquiler Marzo:     Bs. 3,000
Trimestre (Ene+Feb+Mar): Bs. 9,000

IMPUESTOS:
IVA 13%:     Determinado Bs. 390 → Efectivo Bs. 90 (con facturas)
IT 3%:       Bs. 90 (siempre)
RC-IVA 12.5%: Determinado Bs. 1,125 → Efectivo Bs. 325 (con facturas)

NETO: Bs. 2,495
  → Samir 60%: Bs. 1,497
  → Socio 40%: Bs. 998
```

---

## 🛠️ Stack Tecnológico

### Backend
- **FastAPI** - Framework web moderno y rápido
- **SQLAlchemy** - ORM para Python
- **PostgreSQL** - Base de datos relacional
- **Pydantic** - Validación de datos
- **JWT** - Autenticación segura
- **Uvicorn** - Servidor ASGI

### Frontend
- **React** - Librería UI
- **TailwindCSS** - Framework CSS
- **Fetch API** - Comunicación con backend

### DevOps
- **Docker** - Contenedores
- **Docker Compose** - Orquestación
- **pgAdmin** - Administración de BD

---

## 📋 TODO / Próximas Mejoras

- [ ] Integrar cálculo de impuestos en el flujo de registro de pagos
- [ ] Módulo de facturas de compensación con upload de archivos
- [ ] Reportes en PDF para presentar al contador
- [ ] Alertas automáticas de vencimientos
- [ ] Notificaciones por email a copropietarios
- [ ] Dashboard con gráficos interactivos
- [ ] Exportación a Excel de reportes
- [ ] Sistema de roles (admin/copropietario/solo lectura)
- [ ] Historial de cambios (auditoría)
- [ ] Backup automático de base de datos

---

## 👨‍💻 Desarrollo

### Estructura del Proyecto

```
GESTION-DE-ALQUILERES/
├── app/
│   ├── api/
│   │   └── v1/
│   │       ├── auth.py
│   │       ├── propiedades.py
│   │       ├── inquilinos.py
│   │       ├── contratos.py
│   │       ├── pagos.py
│   │       ├── reportes.py
│   │       └── impuestos.py ⭐ NUEVO
│   ├── core/
│   │   ├── config.py
│   │   ├── dependencies.py
│   │   └── security.py
│   ├── database/
│   │   ├── base.py
│   │   └── session.py
│   ├── models/
│   │   ├── user.py
│   │   ├── propiedad.py
│   │   ├── copropietario.py
│   │   ├── inquilino.py
│   │   ├── contrato.py
│   │   ├── pago.py
│   │   ├── distribucion_pago.py
│   │   └── impuesto.py ⭐ NUEVO
│   ├── schemas/
│   ├── services/
│   │   └── tax_calculator.py ⭐ NUEVO
│   ├── utils/
│   └── main.py
├── frontend/
│   └── index.html ⭐ NUEVO
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── .env.example
```

---

## 📄 Licencia

Este proyecto es privado y propiedad de **Samir Sikaffi**.

---

## 🤝 Contacto

**Desarrollador:** Samir Sikaffi  
**GitHub:** [@SAMIRSIKAFFI](https://github.com/SAMIRSIKAFFI)  
**Proyecto:** [GESTION-DE-ALQUILERES](https://github.com/SAMIRSIKAFFI/GESTION-DE-ALQUILERES)

---

## 🎯 Resumen

Este sistema te permite:

✅ Gestionar propiedades propias y copropiedades  
✅ Calcular distribuciones automáticas según porcentajes  
✅ Registrar pagos con mora automática  
✅ Calcular impuestos bolivianos (IVA/IT/RC-IVA)  
✅ Ver siempre: determinado vs efectivo  
✅ Optimizar con facturas de compensación  
✅ Obtener reportes completos  
✅ Todo en una interfaz visual moderna  

**¡Gestiona tus alquileres como un profesional!** 🏢💰
