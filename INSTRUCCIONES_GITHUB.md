# 📝 Instrucciones para Subir el Código a GitHub

## Opción 1: Subir desde tu Computadora (Recomendado)

### Paso 1: Instalar Git

Si no tienes Git instalado:

**Windows**: Descarga desde https://git-scm.com/download/win

**Mac**: 
```bash
brew install git
```

**Linux**:
```bash
sudo apt install git
```

### Paso 2: Configurar Git (Solo la primera vez)

Abre tu terminal/consola y ejecuta:
```bash
git config --global user.name "Tu Nombre"
git config --global user.email "tu_email@example.com"
```

### Paso 3: Clonar tu Repositorio
```bash
git clone https://github.com/SAMIRSIKAFFI/GESTION-DE-ALQUILERES.git
cd GESTION-DE-ALQUILERES
```

### Paso 4: Hacer Cambios

Edita los archivos que necesites modificar.

### Paso 5: Agregar Cambios
```bash
git add .
```

### Paso 6: Hacer Commit
```bash
git commit -m "Descripción de los cambios"
```

### Paso 7: Subir a GitHub
```bash
git push origin main
```

---

## Opción 2: Subir Directamente desde GitHub

### Paso 1: Ir a tu Repositorio

https://github.com/SAMIRSIKAFFI/GESTION-DE-ALQUILERES

### Paso 2: Subir Archivos

1. Haz clic en **"Add file"** → **"Upload files"**
2. Arrastra archivos o carpetas
3. Escribe un mensaje descriptivo
4. Haz clic en **"Commit changes"**

### Paso 3: Crear Archivos Nuevos

1. Haz clic en **"Add file"** → **"Create new file"**
2. Escribe el nombre del archivo
3. Agrega el contenido
4. Haz clic en **"Commit new file"**

---

## 📱 Usando GitHub Desktop

Si prefieres una interfaz gráfica:

1. Descarga **GitHub Desktop**: https://desktop.github.com/
2. Instala e inicia sesión
3. Clona tu repositorio
4. Haz cambios en los archivos
5. Commit y Push desde la interfaz

---

## 🔄 Comandos Git Útiles

### Ver estado de archivos:
```bash
git status
```

### Ver diferencias:
```bash
git diff
```

### Actualizar repositorio local:
```bash
git pull origin main
```

### Ver historial:
```bash
git log --oneline
```

### Deshacer cambios locales:
```bash
git checkout .
```

---

## 🆘 Solución de Problemas

### Error: "Permission denied (publickey)"

**Solución**: Usar HTTPS en lugar de SSH
```bash
git remote set-url origin https://github.com/SAMIRSIKAFFI/GESTION-DE-ALQUILERES.git
```

### Error: "Your local changes would be overwritten"

**Solución**: 
```bash
git stash
git pull
git stash pop
```

### Olvidé subir un archivo

**Solución**:
```bash
git add archivo_olvidado.py
git commit -m "Agregar archivo olvidado"
git push
```

---

## ✅ Checklist de Verificación

Antes de hacer push, verifica:

- [ ] ✅ Todos los archivos necesarios están agregados
- [ ] ✅ El archivo `.env` NO está incluido (solo `.env.example`)
- [ ] ✅ No hay contraseñas o datos sensibles
- [ ] ✅ El mensaje de commit es descriptivo
- [ ] ✅ Los archivos grandes están en `.gitignore`

---

## 📞 Recursos Adicionales

- Documentación oficial de Git: https://git-scm.com/doc
- GitHub Guides: https://guides.github.com/
- GitHub Desktop: https://desktop.github.com/

---

**¡Listo para colaborar! 🚀**
```

5. **Mensaje:** `Agregar instrucciones de GitHub`
6. **Commit new file**

---

## 🎯 ESTADO FINAL DEL REPOSITORIO

Después de agregar `INSTRUCCIONES_GITHUB.md`, tendrás:
```
✅ .env.example
✅ .gitignore
✅ COMANDOS_UTILES.md
✅ Dockerfile
✅ INDEX.md
✅ INSTRUCCIONES_GITHUB.md  ← Nuevo
✅ README.md
✅ RESUMEN.md
✅ app/
✅ docker-compose.yml
✅ requirements.txt
✅ start.bat
✅ start.sh
