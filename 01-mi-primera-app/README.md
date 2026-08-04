# Módulo 01 — Mi Primera APP

> **Materia**: Desarrollo de Software
> **Duración**: 90 minutos
> **Taller guiado**: Sí — construcción **desde cero**, archivo por archivo, sin clonar el repo

---

## Material del aula

| Archivo | Para quién | Qué es |
|---------|------------|--------|
| [`GUIA_ALUMNO.md`](./GUIA_ALUMNO.md) | Alumnos | **Material de trabajo**. Código completo en orden de creación, con tiempos y checkpoints. Cada alumno la abre en su navegador y copia los archivos. |
| [`PRESENTACION.md`](./PRESENTACION.md) | Docente | Slides Marp (fases, comandos clave, checkpoints) |
| `README.md` | Todos | **Esta guía de referencia**. Instalación multi-OS y explicación del código. |
| [`SPEC.md`](./SPEC.md) | Todos | Especificación completa del software |

> **Flujo del aula**: los alumnos construyen el proyecto a mano siguiendo `GUIA_ALUMNO.md`. Este README queda como referencia para instalación de herramientas (Parte 1) y para entender el código (Parte 4).

---

## Objetivo del Taller

Construir una **API REST de Tareas** con FastAPI y un **frontend en React** que la consuma. En el camino vamos a cubrir:

- Instalación de herramientas de desarrollo
- Creación de un backend con FastAPI + uv
- Verificación de la API con Swagger y herramientas externas
- Creación de un frontend con React + Vite + pnpm
- Integración frontend ↔ backend
- El ciclo de vida completo del software

## Qué vamos a construir

Una aplicación de **Tareas (To-Do)** con 4 operaciones:

| Operación | HTTP | Endpoint | Descripción |
|-----------|------|----------|-------------|
| Listar | `GET` | `/api/tasks` | Devuelve todas las tareas |
| Crear | `POST` | `/api/tasks` | Crea una tarea nueva |
| Completar | `PATCH` | `/api/tasks/{id}` | Marca como hecha / desmarca |
| Eliminar | `DELETE` | `/api/tasks/{id}` | Borra una tarea |

## Arquitectura

```
┌─────────────────┐       HTTP        ┌─────────────────┐
│                  │  ──────────────►  │                  │
│   Frontend       │  ◄──────────────  │   Backend        │
│   React + Vite   │     JSON          │   FastAPI        │
│   :5173          │                   │   :8000          │
│                  │                   │                  │
│   ui@localhost   │    /api/tasks     │   api@localhost  │
└─────────────────┘                   └─────────────────┘
```

---

## Estructura del Módulo

```
01-mi-primera-app/
├── README.md                    # Esta guía de referencia
├── GUIA_ALUMNO.md               # Material de aula — código completo desde cero
├── SPEC.md                      # Especificación del software
├── PRESENTACION.md              # Slides Marp (fases + checkpoints)
├── PRESENTACION.html            # Slides exportadas (HTML)
├── PRESENTACION.pdf             # Slides exportadas (PDF)
│
├── backend/
│   ├── pyproject.toml           # Dependencias Python (uv)
│   └── main.py                  # API completa (~200 líneas)
│
└── frontend/
    ├── package.json             # Dependencias Node (pnpm)
    ├── vite.config.js           # Configuración Vite + proxy
    ├── index.html               # Entry point HTML
    └── src/
        ├── main.jsx             # Bootstrap React
        ├── App.jsx              # Componente principal (~160 líneas)
        ├── App.css              # Estilos
        └── api.js               # Servicio de comunicación con la API
```

---

# PARTE 1 — Instalación de Herramientas

> **IMPORTANTE**: Si ya tenés instalado Python, Node.js, uv y pnpm, saltá a la [Parte 2](#parte-2--backend-fastapi--uv).

---

## 1.1 Python 3.12+

### Ubuntu / Debian

```bash
sudo apt update
sudo apt install -y python3 python3-venv python3-pip
python3 --version   # Debe mostrar 3.12.x o superior
```

### Linux Rocky / RHEL / CentOS / Fedora

```bash
sudo dnf install -y python3.12 python3.12-pip
# Si python3.12 no está en los repos:
sudo dnf install -y python3.11 python3.11-pip

python3 --version
```

### macOS

```bash
# macOS ya viene con Python, pero es viejo. Usá Homebrew:
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
brew install python@3.12
python3 --version
```

### Windows

```bash
# Descargá el instalador desde:
# https://www.python.org/downloads/
# ✅ IMPORTANTE: tildá "Add Python to PATH" durante la instalación

python --version
# Si no funciona, cerrá y abrí una nueva terminal
```

---

## 1.2 uv (gestor de paquetes Python)

uv es un gestor de paquetes Python ultrarrápido. Reemplaza `pip`, `venv` y `pip-tools` con un solo comando.

### Linux (Ubuntu, Rocky, cualquier distro)

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
# Recargá la terminal o ejecutá:
source ~/.bashrc
uv --version
```

### macOS

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
source ~/.zshrc   # o ~/.bashrc si usás bash
uv --version
```

### Windows

```powershell
# PowerShell como administrador:
irm https://astral.sh/uv/install.ps1 | iex
# Cerrá y abrí una nueva terminal
uv --version
```

> **¿Qué hace uv?** En una sola línea:
> - Crea el entorno virtual (`python -m venv`)
> - Instala dependencias (`pip install`)
> - Resuelve conflictos de versiones
> Todo esto en ~100ms vs los ~30s de pip.

---

## 1.3 Node.js 18+ (runtime de JavaScript)

### Ubuntu / Debian

```bash
# Usamos nvm (Node Version Manager) para instalar Node
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.3/install.sh | bash
source ~/.bashrc
nvm install 22
nvm use 22
node --version   # Debe mostrar v22.x.x
```

### Linux Rocky / RHEL / CentOS

```bash
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.3/install.sh | bash
source ~/.bashrc
nvm install 22
nvm use 22
node --version
```

### macOS

```bash
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.3/install.sh | bash
source ~/.zshrc
nvm install 22
nvm use 22
node --version
```

### Windows

```powershell
# Descargá el instalador LTS desde:
# https://nodejs.org/
# ✅ Tildá "Automatically install the necessary tools"

node --version
```

---

## 1.4 pnpm (gestor de paquetes Node)

> **IMPORTANTE en la UTN**: npm está bloqueado por el firewall Fortigate. Usamos pnpm.

### Todos los SO (después de instalar Node)

```bash
# Habilitar corepack (viene con Node 16+)
corepack enable
corepack prepare pnpm@latest --activate
pnpm --version
```

### Si corepack no funciona (Ubuntu Rocky / versiones viejas)

```bash
npm install -g pnpm
# Nota: npm funciona para INSTALAR pnpm, aunque esté bloqueado para el resto
pnpm --version
```

---

## 1.5 Herramientas de Testing HTTP

Elegí **una** de estas herramientas para probar la API:

### Postman (recomendado para principiantes)

| SO | Instalación |
|----|------------|
| Ubuntu | `sudo snap install postman` |
| Rocky | Descargá el .AppImage desde [postman.com](https://www.postman.com/downloads/) |
| macOS | Descargá desde [postman.com](https://www.postman.com/downloads/) o `brew install --cask postman` |
| Windows | Descargá el instalador desde [postman.com](https://www.postman.com/downloads/) |

### Bruno (open source, alternativa a Postman)

```bash
# Ubuntu / Rocky
sudo snap install bruno

# macOS
brew install --cask bruno

# Windows
winget install Bruno.Bruno
```

### curl (ya viene instalado en todos los SO)

```bash
# Si tenés curl (casi seguro que sí), no necesitás instalar nada
curl --version
```

---

# PARTE 2 — Backend (FastAPI + uv)

## 2.1 Crear el proyecto

**En el aula**: seguí `GUIA_ALUMNO.md` — Parte B. Creás `backend/pyproject.toml` y `backend/main.py` a mano, copiando el código completo. No usás `uv init`.

```bash
cd 01-mi-primera-app/backend
```

> **Atajo (fuera del aula)**: cuando ya sabés, `uv init` + `uv add` hacen el scaffolding en segundos.

## 2.2 Instalar dependencias

```bash
# Si ya existe pyproject.toml:
uv sync
```

Esto crea el entorno virtual `.venv` e instala FastAPI + uvicorn automáticamente.

## 2.3 Ejecutar el servidor

```bash
uv run main.py
```

Deberías ver algo como:

```
INFO:     Will watch for changes in these directories: [...]
INFO:     Started reloader process [...]
INFO:     Started server process [...]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

**¡El servidor está corriendo!** No cierres esta terminal.

## 2.4 Verificar con el navegador

Abrí en tu navegador:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

En Swagger podés probar todos los endpoints directamente desde el navegador.

## 2.5 Probar con curl

En una **nueva terminal**:

```bash
# Listar tareas (debería estar vacío)
curl http://localhost:8000/api/tasks

# Crear una tarea
curl -X POST http://localhost:8000/api/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "Aprender FastAPI"}'

# Listar de nuevo (debería tener 1 tarea)
curl http://localhost:8000/api/tasks

# Crear otra
curl -X POST http://localhost:8000/api/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "Hacer el taller de React"}'

# Marcar como completada (ID 1)
curl -X PATCH http://localhost:8000/api/tasks/1

# Eliminar (ID 2)
curl -X DELETE http://localhost:8000/api/tasks/2

# Health check
curl http://localhost:8000/api/health
```

## 2.6 Probar con Postman / Bruno

1. Abrí Postman (o Bruno)
2. Creá una nueva Collection llamada "Mi Primera APP"
3. Agregá estos requests:

| Nombre | Método | URL | Body (JSON) |
|--------|--------|-----|-------------|
| Listar tareas | `GET` | `http://localhost:8000/api/tasks` | — |
| Crear tarea | `POST` | `http://localhost:8000/api/tasks` | `{"title": "Mi tarea"}` |
| Toggle tarea | `PATCH` | `http://localhost:8000/api/tasks/1` | — |
| Eliminar tarea | `DELETE` | `http://localhost:8000/api/tasks/1` | — |

4. Ejecutá cada request y verificá la respuesta

---

# PARTE 3 — Frontend (React + Vite + pnpm)

## 3.1 Crear el proyecto

**En el aula**: seguí `GUIA_ALUMNO.md` — Parte D. Creás los 7 archivos a mano (`package.json`, `index.html`, `vite.config.js`, `src/main.jsx`, `src/api.js`, `src/App.jsx`, `src/App.css`), en ese orden. No usás `pnpm create vite` — así entendés la estructura real del proyecto.

```bash
cd 01-mi-primera-app/frontend
```

> **Atajo (fuera del aula)**: cuando ya sabés, `pnpm create vite . --template react` genera el esqueleto y solo modificás lo necesario.

## 3.2 Instalar dependencias

```bash
pnpm install
```

## 3.3 Ejecutar el frontend

```bash
pnpm dev
```

Deberías ver algo como:

```
  VITE v6.x.x  ready in xxx ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: http://192.168.x.x:5173/
```

**¡El frontend está corriendo!** Abrí http://localhost:5173 en tu navegador.

## 3.4 Verificar la integración

Con **ambos servidores corriendo** (backend en :8000 y frontend en :5173):

1. Abrí http://localhost:5173
2. Escribí una tarea en el input
3. Hacé click en "Agregar"
4. La tarea debería aparecer en la lista
5. Marcala como completada (checkbox)
6. Eliminala (botón ×)

Si funciona, **¡felicidades!** Tu primera app fullstack está funcionando.

---

# PARTE 4 — Entendiendo el Código

## Backend — main.py

### Modelos de datos (Pydantic)

```python
class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)

class Task(BaseModel):
    id: int
    title: str
    completed: bool
    created_at: str
```

**¿Por qué dos modelos?** `TaskCreate` es lo que el cliente ENVÍA (solo el título). `Task` es lo que el servidor DEVUELVE (con ID, estado y fecha). Separar entrada de salida es un patrón fundamental.

### Almacenamiento en memoria

```python
tasks: list[dict] = []
next_id: int = 1
```

Para este taller NO usamos base de datos. Los datos viven en una lista de Python. Si reiniciás el servidor, se pierden. Esto es intencional — el foco es el ciclo HTTP, no la persistencia.

### CORS

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
```

CORS (Cross-Origin Resource Sharing) es un mecanismo de seguridad. Por defecto, un navegador bloquea fetches de `localhost:5173` a `localhost:8000`. En desarrollo usamos el proxy de Vite, pero configuramos CORS como fallback y para futuro deploy.

## Frontend — api.js

```javascript
async function request(url, options = {}) {
  const response = await fetch(`/api${url}`, { ... });
  return response.json();
}

export async function fetchTasks() {
  return request("/tasks");
}
```

**¿Por qué separar api.js?** Porque si mañana cambiamos la URL base, o agregamos autenticación (headers), o cambiamos a axios, TODO se cambia en un solo archivo. El componente `App.jsx` no se entera.

## Frontend — App.jsx

Los conceptos clave de React que usa:

| Concepto | Dónde | Para qué |
|----------|-------|----------|
| `useState` | `[tasks, setTasks]` | Guardar la lista de tareas |
| `useEffect` | `loadTasks()` | Cargar datos al iniciar |
| `onChange` | Input controlado | Sincronizar input con estado |
| `onSubmit` | Formulario | Crear tarea sin recargar página |
| `map()` | Lista de tareas | Renderizar cada tarea |
| `filter()` | Eliminar | Quitar tarea del array |
| Filtrado condicional | `loading ? ... : ...` | Mostrar loading, lista o vacío |

---

# PARTE 5 — El Ciclo de Vida del Software

> Ver [SPEC.md](./SPEC.md) para la especificación completa.

En este taller cubrimos las primeras 4 fases del ciclo de vida:

| Fase | Qué hacemos acá | Herramientas |
|------|-----------------|-------------|
| 1. Requisitos | Definimos qué hace la app (4 endpoints) | Esta guía |
| 2. Diseño | Arquitectura client-server, modelos de datos | Diagrama de arquitectura |
| 3. Implementación | Escribimos el código | FastAPI, React, uv, pnpm |
| 4. Testing | Verificamos que funciona | Swagger, Postman, curl |
| 5. Deployment | (Futuro) Docker + hosting | — |
| 6. Mantenimiento | (Futuro) Agregar features, fix bugs | — |

---

# Ejercicios para Llevar a Casa

### Nivel 🟢 Comprensión

1. Abrí el Swagger UI (`/docs`) y respondé: ¿cuántos endpoints tiene la API? ¿Cuáles son?
2. Modificá el mensaje de `health_check()` y recargá el Swagger. ¿Qué cambió?
3. Eliminá el `created_at` del modelo `Task`. ¿Qué pasa con la API?

### Nivel 🟡 Aplicación

4. Agregá un campo `priority` (baja/media/alta) a las tareas. Actualizá el modelo, el endpoint de creación y el frontend.
5. Agregá un endpoint `GET /api/tasks/stats` que devuelva: `{ total: N, completed: N, pending: N }`.
6. Creá un filtro en el frontend: botones "Todas", "Pendientes", "Completadas".

### Nivel 🔴 Análisis

7. Investigá: ¿por qué FastAPI usa `PATCH` en vez de `PUT` para toggle? ¿Cuál es la diferencia?
8. Reemplazá el almacenamiento en memoria por un archivo JSON. Leé al iniciar, escribí al modificar.
9. Agregá autenticación con JWT. Solo el usuario autenticado puede ver y modificar sus tareas.

---

# Referencias

- [FastAPI — Documentación oficial](https://fastapi.tiangolo.com/)
- [FastAPI — CORS](https://fastapi.tiangolo.com/tutorial/cors/)
- [FastAPI — Pydantic](https://fastapi.tiangolo.com/tutorial/body/)
- [uv — Documentación](https://docs.astral.sh/uv/)
- [React — Documentación oficial](https://react.dev/)
- [Vite — Documentación](https://vite.dev/)
- [pnpm — Documentación](https://pnpm.io/)
- [Postman — Learning Center](https://learning.postman.com/)
