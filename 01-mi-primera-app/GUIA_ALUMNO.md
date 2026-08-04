# 📋 Guía del Alumno — Mi Primera APP

> **Materia**: Desarrollo de Software
> **Duración**: 90 minutos
>
> **IMPORTANTE**: Vas a construir el proyecto **desde cero**, archivo por archivo.
> Abrí esta guía en tu navegador y copiá el código de cada archivo en tu editor.
> No clonamos nada — todo lo escribís vos.

---

## Cómo usar esta guía

1. Cada archivo tiene su bloque de código **completo y listo para copiar**
2. Respetá el **orden** de creación (las partes dependen entre sí)
3. Después de cada archivo, seguí las **instrucciones de verificación** antes de avanzar
4. Si algo falla: **leé el error**, preguntá al docente, NO sigas adelante

---

## PARTE A — Setup y estructura (5 min)

### A.1 Verificar herramientas

Abrí una terminal y ejecutá cada comando. Todos deben responder OK:

```bash
python3 --version      # Python 3.12+ (Windows: python --version)
uv --version           # uv instalado
node --version         # Node.js 18+ (ideal 22)
pnpm --version         # pnpm instalado
```

> **¿Falta alguna?** Avisá al docente antes de continuar.

### A.2 Crear la estructura de directorios

```bash
mkdir -p 01-mi-primera-app/backend
mkdir -p 01-mi-primera-app/frontend/src
mkdir -p 01-mi-primera-app/frontend/public
```

Verificá con:

```bash
ls -R 01-mi-primera-app
```

Debés ver:

```
01-mi-primera-app/
├── backend/
└── frontend/
    ├── public/
    └── src/
```

---

## PARTE B — Backend desde cero (25 min)

### B.1 Crear `backend/pyproject.toml`

> **Editor**: creá el archivo `pyproject.toml` dentro de `backend/` con este contenido.

```toml
[project]
name = "mi-primera-app-backend"
version = "0.1.0"
description = "API de Tareas — Taller Mi Primera APP"
requires-python = ">=3.12"
dependencies = [
    "fastapi>=0.115.0",
    "uvicorn[standard]>=0.30.0",
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.build.targets.wheel]
packages = ["."]
```

**Qué es**: el manifiesto del proyecto Python. Declara el nombre, la versión y las dependencias. `uv` lo lee para instalar todo automáticamente.

---

### B.2 Crear `backend/main.py`

> **Editor**: creá el archivo `main.py` dentro de `backend/` con este contenido.
> **Son ~200 líneas. Copialo completo, no saltees ninguna parte.**

```python
"""
Mi Primera APP — Backend API de Tareas
======================================

API REST completa para gestionar tareas (To-Do List).
Desarrollada con FastAPI como parte del taller "Mi Primera APP".

Ejecutar:
    uv run main.py

Endpoints:
    GET    /api/tasks         → Listar todas las tareas
    POST   /api/tasks         → Crear una tarea nueva
    PATCH  /api/tasks/{id}    → Toggle completada / no completada
    DELETE /api/tasks/{id}    → Eliminar una tarea
"""

from datetime import datetime, timezone
from typing import Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

# ============================================================
# 1. MODELOS DE DATOS (Pydantic)
# ============================================================
# Pydantic valida automáticamente que los datos que llegan
# sean del tipo correcto. Si mandás un string donde va un int,
# FastAPI devuelve un error 422 claro y descriptivo.


class TaskCreate(BaseModel):
    """Modelo para CREAR una tarea. Solo pedimos el título."""

    title: str = Field(..., min_length=1, max_length=200, examples=["Comprar leche"])


class Task(BaseModel):
    """Modelo completo de una tarea (lo que devolvemos al frontend)."""

    id: int
    title: str
    completed: bool
    created_at: str


# ============================================================
# 2. ALMACENAMIENTO EN MEMORIA
# ============================================================
# Para este taller NO usamos base de datos.
# Los datos viven en una lista de Python mientras el servidor
# está corriendo. Si reiniciás el servidor, se pierden.
# Esto es INTENCIONAL — el foco está en el ciclo HTTP,
# no en la persistencia.

tasks: list[dict] = []
next_id: int = 1


def find_task(task_id: int) -> Optional[dict]:
    """Busca una tarea por ID. Devuelve None si no existe."""
    for task in tasks:
        if task["id"] == task_id:
            return task
    return None


# ============================================================
# 3. APLICACIÓN FASTAPI
# ============================================================

app = FastAPI(
    title="Mi Primera APP — API de Tareas",
    description="API REST para gestionar tareas. Taller de Desarrollo de Software 2026.",
    version="0.1.0",
)

# ============================================================
# 4. CORS (Cross-Origin Resource Sharing)
# ============================================================
# CORS es un mecanismo de seguridad del navegador.
# Por defecto, un frontend en localhost:5173 NO puede hacer
# fetch a localhost:8000 — el navegador lo bloquea.
#
# En desarrollo usamos el proxy de Vite para evitar esto,
# pero configuramos CORS de todas formas porque:
#   1. Es un concepto fundamental que todo dev debe entender
#   2. Lo necesitás cuando deployás el frontend por separado
#
# En producción, acá irían solo los dominios reales.

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción: listar dominios específicos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# 5. ENDPOINTS
# ============================================================


@app.get("/api/tasks", response_model=list[Task])
def list_tasks():
    """Devuelve la lista completa de tareas."""
    return tasks


@app.post("/api/tasks", response_model=Task, status_code=201)
def create_task(body: TaskCreate):
    """
    Crea una tarea nueva.

    El body debe tener:
      - "title": string no vacío (máximo 200 caracteres)

    FastAPI valida automáticamente con Pydantic.
    Si falta el title o está vacío, devuelve error 422.
    """
    global next_id

    task = {
        "id": next_id,
        "title": body.title.strip(),
        "completed": False,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    next_id += 1
    tasks.append(task)
    return task


@app.patch("/api/tasks/{task_id}", response_model=Task)
def toggle_task(task_id: int):
    """
    Cambia el estado de una tarea (completada ↔ no completada).

    PATCH = actualización parcial. Solo modificamos el campo
    'completed', no necesitamos enviar toda la tarea.
    """
    task = find_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail=f"Tarea {task_id} no encontrada")

    task["completed"] = not task["completed"]
    return task


@app.delete("/api/tasks/{task_id}")
def delete_task(task_id: int):
    """
    Elimina una tarea por su ID.

    Devuelve { "ok": true } si se eliminó,
    o error 404 si la tarea no existe.
    """
    task = find_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail=f"Tarea {task_id} no encontrada")

    tasks.remove(task)
    return {"ok": True}


# ============================================================
# 6. HEALTH CHECK
# ============================================================
# Un health check es un endpoint que verifica que el servicio
# está funcionando. Es estándar en cualquier API moderna.
# Los load balancers y monitores lo llaman periódicamente.


@app.get("/api/health")
def health_check():
    return {"status": "ok", "service": "mi-primera-app-backend", "tasks_count": len(tasks)}


# ============================================================
# 7. MAIN — Ejecutar el servidor
# ============================================================
# uvicorn es el servidor ASGI que ejecuta FastAPI.
# --reload: reinicia automáticamente al guardar cambios
# --port 8000: puerto del servidor
#
# NOTA: En producción se usa:
#   uvicorn main:app --host 0.0.0.0 --port 8000
# Sin --reload y con host 0.0.0.0 para aceptar conexiones externas.

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
```

---

### B.3 Instalar dependencias

```bash
cd 01-mi-primera-app/backend
uv sync
```

Debés ver que se instalan `fastapi`, `uvicorn` y el resto (21 paquetes). Si falla, revisá que el `pyproject.toml` no tenga errores de sintaxis.

---

### B.4 Ejecutar el servidor

```bash
uv run main.py
```

Debés ver:

```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

> ⚠️ **NO cierres esta terminal** — el servidor tiene que quedar corriendo.

---

### ✅ CHECKPOINT 1 — Swagger

Abrí en tu navegador: **http://localhost:8000/docs**

Debés ver la interfaz de Swagger con los 4 endpoints de la API.

**¿No aparece?** Revisá:
- ¿La terminal muestra errores? (pegale el mensaje al docente)
- ¿Está corriendo `uv run main.py`?

---

## PARTE C — Verificar la API (10 min)

### C.1 Probar con curl (nueva terminal)

```bash
# Listar (debería estar vacío)
curl http://localhost:8000/api/tasks

# Crear una tarea
curl -X POST http://localhost:8000/api/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "Aprender FastAPI"}'

# Listar de nuevo (debería tener 1 tarea)
curl http://localhost:8000/api/tasks

# Marcar como completada (ID 1)
curl -X PATCH http://localhost:8000/api/tasks/1

# Eliminar (ID 1)
curl -X DELETE http://localhost:8000/api/tasks/1

# Health check
curl http://localhost:8000/api/health
```

### C.2 Probar con Postman / Bruno

1. Abrí Postman (o Bruno)
2. Creá una Collection llamada "Mi Primera APP"
3. Agregá los 4 requests:

| Nombre | Método | URL | Body |
|--------|--------|-----|------|
| Listar tareas | `GET` | `http://localhost:8000/api/tasks` | — |
| Crear tarea | `POST` | `http://localhost:8000/api/tasks` | `{"title": "Mi tarea"}` |
| Toggle tarea | `PATCH` | `http://localhost:8000/api/tasks/1` | — |
| Eliminar tarea | `DELETE` | `http://localhost:8000/api/tasks/1` | — |

---

## PARTE D — Frontend desde cero (35 min)

> En esta parte creás el frontend **sin usar `pnpm create vite`** —
> cada archivo lo escribís vos. Así entendés la estructura de Vite de verdad.

### D.1 Crear `frontend/package.json`

> **Editor**: creá el archivo `package.json` dentro de `frontend/` con este contenido.
> **CUIDADO**: JSON es estricto — una coma de más o de menos rompe todo.

```json
{
  "name": "mi-primera-app-frontend",
  "private": true,
  "version": "0.1.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview"
  },
  "dependencies": {
    "react": "^19.0.0",
    "react-dom": "^19.0.0"
  },
  "devDependencies": {
    "@vitejs/plugin-react": "^4.4.0",
    "vite": "^6.0.0"
  }
}
```

---

### D.2 Crear `frontend/index.html`

> **Editor**: creá el archivo `index.html` dentro de `frontend/`.

```html
<!DOCTYPE html>
<html lang="es">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Mi Primera APP — Tareas</title>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.jsx"></script>
  </body>
</html>
```

**Qué es**: el único HTML de la app. React dibuja todo dentro de `<div id="root">`.

---

### D.3 Crear `frontend/vite.config.js`

> **Editor**: creá el archivo `vite.config.js` dentro de `frontend/`.

```javascript
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    // Proxy: redirige /api/* al backend en localhost:8000
    // Así el frontend puede hacer fetch("/api/tasks")
    // sin problemas de CORS ni URLs absolutas.
    //
    // EN PRODUCCIÓN: no existe este proxy. El frontend se
    // builda como archivos estáticos y se sirve desde nginx
    // o similar, que redirige /api al backend.
    proxy: {
      "/api": {
        target: "http://localhost:8000",
        changeOrigin: true,
      },
    },
  },
});
```

---

### D.4 Crear `frontend/src/main.jsx`

> **Editor**: creá el archivo `main.jsx` dentro de `frontend/src/`.

```jsx
import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App.jsx";

ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
```

**Qué es**: el punto de entrada de React. Toma el `<div id="root">` del HTML y monta la app dentro.

---

### D.5 Crear `frontend/src/api.js`

> **Editor**: creá el archivo `api.js` dentro de `frontend/src/`.

```javascript
/**
 * api.js — Servicio de comunicación con el Backend
 * ==================================================
 *
 * Este archivo encapsula TODA la comunicación con la API.
 * El componente App.jsx NUNCA hace fetch directamente —
 * siempre pasa por acá.
 *
 * POR QUÉ separar esto:
 *   1. Si cambia la URL base, se cambia en UN solo lugar
 *   2. Si necesitás agregar headers (auth), se agrega acá
 *   3. El componente se queda limpio, solo con lógica de UI
 *
 * Nota: Usamos rutas relativas (/api/tasks) porque el proxy
 * de Vite las redirige al backend. En producción, acá iría
 * la URL completa (https://api.miserver.com/api/tasks).
 */

const API_BASE = "/api";

/**
 * Helper genérico para hacer fetch con manejo de errores.
 * Si el servidor responde con error (4xx, 5xx), lanza una
 * excepción con el mensaje del backend.
 */
async function request(url, options = {}) {
  const response = await fetch(`${API_BASE}${url}`, {
    headers: {
      "Content-Type": "application/json",
      ...options.headers,
    },
    ...options,
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({}));
    throw new Error(error.detail || `Error ${response.status}`);
  }

  // DELETE devuelve { ok: true } — no intentamos parsear como JSON
  // si el status es 204 No Content
  if (response.status === 204) return null;

  return response.json();
}

/**
 * GET /api/tasks → Devuelve la lista de tareas
 */
export async function fetchTasks() {
  return request("/tasks");
}

/**
 * POST /api/tasks → Crea una tarea nueva
 * @param {string} title - Título de la tarea
 */
export async function createTask(title) {
  return request("/tasks", {
    method: "POST",
    body: JSON.stringify({ title }),
  });
}

/**
 * PATCH /api/tasks/{id} → Cambia completed ↔ !completed
 * @param {number} id - ID de la tarea
 */
export async function toggleTask(id) {
  return request(`/tasks/${id}`, {
    method: "PATCH",
  });
}

/**
 * DELETE /api/tasks/{id} → Elimina una tarea
 * @param {number} id - ID de la tarea
 */
export async function deleteTask(id) {
  return request(`/tasks/${id}`, {
    method: "DELETE",
  });
}
```

---

### D.6 Crear `frontend/src/App.jsx`

> **Editor**: creá el archivo `App.jsx` dentro de `frontend/src/`.

```jsx
/**
 * App.jsx — Componente principal de la aplicación
 * =================================================
 *
 * Toda la UI vive en este componente. Para un taller de
 * 90 minutos, un solo componente es suficiente. En un proyecto
 * real, esto se dividiría en:
 *
 *   <TaskInput onAdd={...} />
 *   <TaskList tasks={...} onToggle={...} onDelete={...} />
 *
 * Conceptos de React que practicamos acá:
 *   - useState: estado local del componente
 *   - useEffect: efectos secundarios (fetch al montar)
 *   - JSX: sintaxis similar a HTML dentro de JavaScript
 *   - Event handling: onSubmit, onChange, onClick
 *   - Conditional rendering: mostrar cosas según condiciones
 *   - Lists: renderizar arrays con .map()
 */

import { useState, useEffect } from "react";
import { fetchTasks, createTask, toggleTask, deleteTask } from "./api";
import "./App.css";

export default function App() {
  // ---- Estado ----
  const [tasks, setTasks] = useState([]); // Lista de tareas
  const [newTitle, setNewTitle] = useState(""); // Input controlado
  const [loading, setLoading] = useState(true); // Estado de carga
  const [error, setError] = useState(null); // Mensaje de error

  // ---- Cargar tareas al montar el componente ----
  // useEffect con [] vacío = se ejecuta UNA sola vez,
  // cuando el componente se "monta" (aparece en pantalla).
  useEffect(() => {
    loadTasks();
  }, []);

  async function loadTasks() {
    try {
      setLoading(true);
      const data = await fetchTasks();
      setTasks(data);
      setError(null);
    } catch (err) {
      setError("No se pudo conectar con el backend. ¿Está corriendo en :8000?");
    } finally {
      setLoading(false);
    }
  }

  // ---- Crear tarea ----
  async function handleAdd(e) {
    e.preventDefault(); // Evita que el form recargue la página

    const title = newTitle.trim();
    if (!title) return; // No crear tareas vacías

    try {
      const task = await createTask(title);
      setTasks([...tasks, task]); // Agrego al final (inmutabilidad)
      setNewTitle(""); // Limpio el input
      setError(null);
    } catch (err) {
      setError("Error al crear la tarea");
    }
  }

  // ---- Toggle completada ----
  async function handleToggle(id) {
    try {
      const updated = await toggleTask(id);
      setTasks(
        tasks.map((t) => (t.id === id ? updated : t)) // Reemplazo solo la que cambió
      );
    } catch (err) {
      setError("Error al actualizar la tarea");
    }
  }

  // ---- Eliminar tarea ----
  async function handleDelete(id) {
    try {
      await deleteTask(id);
      setTasks(tasks.filter((t) => t.id !== id)); // Filtro la eliminada
    } catch (err) {
      setError("Error al eliminar la tarea");
    }
  }

  // ---- Render ----
  return (
    <div className="app">
      <header className="header">
        <h1>Mis Tareas</h1>
        <p className="subtitle">Mi Primera APP — FastAPI + React</p>
      </header>

      {/* Formulario para agregar tareas */}
      <form className="add-form" onSubmit={handleAdd}>
        <input
          type="text"
          className="add-input"
          placeholder="¿Qué necesitás hacer?"
          value={newTitle}
          onChange={(e) => setNewTitle(e.target.value)}
          autoFocus
        />
        <button type="submit" className="add-button" disabled={!newTitle.trim()}>
          Agregar
        </button>
      </form>

      {/* Mensaje de error */}
      {error && (
        <div className="error">
          <span>⚠️ {error}</span>
          <button onClick={() => setError(null)}>×</button>
        </div>
      )}

      {/* Lista de tareas */}
      {loading ? (
        <p className="empty">Cargando tareas...</p>
      ) : tasks.length === 0 ? (
        <p className="empty">
          No hay tareas todavía. ¡Agregá una arriba!
        </p>
      ) : (
        <ul className="task-list">
          {tasks.map((task) => (
            <li key={task.id} className={`task-item ${task.completed ? "completed" : ""}`}>
              <label className="task-label">
                <input
                  type="checkbox"
                  checked={task.completed}
                  onChange={() => handleToggle(task.id)}
                />
                <span className="task-title">{task.title}</span>
              </label>
              <button
                className="delete-button"
                onClick={() => handleDelete(task.id)}
                title="Eliminar tarea"
              >
                ×
              </button>
            </li>
          ))}
        </ul>
      )}

      {/* Contador */}
      {tasks.length > 0 && (
        <footer className="footer">
          <span>
            {tasks.filter((t) => t.completed).length} de {tasks.length} completadas
          </span>
        </footer>
      )}
    </div>
  );
}
```

---

### D.7 Crear `frontend/src/App.css`

> **Editor**: creá el archivo `App.css` dentro de `frontend/src/`.

```css
/* ============================================================
   App.css — Estilos de la aplicación
   ============================================================
   Para un taller de 90 minutos, CSS inline o un solo archivo
   es suficiente. En un proyecto real usarías Tailwind, CSS
   Modules, o Styled Components.
*/

/* ---- Reset básico ---- */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto,
    "Helvetica Neue", Arial, sans-serif;
  background: #f5f5f5;
  color: #333;
  line-height: 1.6;
}

/* ---- Contenedor principal ---- */
.app {
  max-width: 600px;
  margin: 40px auto;
  padding: 0 20px;
}

/* ---- Header ---- */
.header {
  text-align: center;
  margin-bottom: 30px;
}

.header h1 {
  font-size: 2rem;
  color: #2563eb;
  margin-bottom: 4px;
}

.subtitle {
  color: #888;
  font-size: 0.9rem;
}

/* ---- Formulario ---- */
.add-form {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
}

.add-input {
  flex: 1;
  padding: 12px 16px;
  border: 2px solid #e0e0e0;
  border-radius: 8px;
  font-size: 1rem;
  outline: none;
  transition: border-color 0.2s;
}

.add-input:focus {
  border-color: #2563eb;
}

.add-button {
  padding: 12px 24px;
  background: #2563eb;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s;
}

.add-button:hover {
  background: #1d4ed8;
}

.add-button:disabled {
  background: #ccc;
  cursor: not-allowed;
}

/* ---- Lista de tareas ---- */
.task-list {
  list-style: none;
}

.task-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 16px;
  background: white;
  border-radius: 8px;
  margin-bottom: 8px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  transition: transform 0.1s;
}

.task-item:hover {
  transform: translateX(4px);
}

.task-item.completed .task-title {
  text-decoration: line-through;
  color: #999;
}

.task-label {
  display: flex;
  align-items: center;
  gap: 12px;
  cursor: pointer;
  flex: 1;
}

.task-label input[type="checkbox"] {
  width: 18px;
  height: 18px;
  cursor: pointer;
}

.task-title {
  font-size: 1rem;
}

.delete-button {
  background: none;
  border: none;
  font-size: 1.4rem;
  color: #ccc;
  cursor: pointer;
  padding: 0 4px;
  line-height: 1;
  transition: color 0.2s;
}

.delete-button:hover {
  color: #ef4444;
}

/* ---- Estado vacío ---- */
.empty {
  text-align: center;
  color: #999;
  padding: 40px 0;
  font-size: 1.1rem;
}

/* ---- Error ---- */
.error {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 16px;
  background: #fef2f2;
  border: 1px solid #fecaca;
  border-radius: 8px;
  margin-bottom: 16px;
  color: #dc2626;
}

.error button {
  background: none;
  border: none;
  font-size: 1.2rem;
  color: #dc2626;
  cursor: pointer;
}

/* ---- Footer / Contador ---- */
.footer {
  text-align: center;
  margin-top: 20px;
  color: #888;
  font-size: 0.9rem;
}
```

---

### D.8 Instalar dependencias del frontend

```bash
cd 01-mi-primera-app/frontend
pnpm install
```

Debés ver que se instalan `react`, `react-dom`, `vite` y `@vitejs/plugin-react`.

> **Si pnpm pregunta por build scripts** (`esbuild`): ejecutá `pnpm approve-builds esbuild` y repetí `pnpm install`.

---

### D.9 Ejecutar el frontend

```bash
pnpm dev
```

Debés ver:

```
  VITE v6.x.x  ready in xxx ms
  ➜  Local:   http://localhost:5173/
```

> ⚠️ **NO cierres esta terminal** — el frontend tiene que quedar corriendo.

---

### ✅ CHECKPOINT 2 — Frontend andando

Abrí **http://localhost:5173** — debe mostrarte la app con el input para agregar tareas.

**¿Aparece la página de Vite pero sin tu app?** Revisá:
- ¿Creaste todos los archivos en las rutas correctas?
- ¿La terminal de `pnpm dev` muestra errores?

---

## PARTE E — Integración y verificación final (15 min)

Con **ambos servidores corriendo** (backend :8000 y frontend :5173):

### E.1 Probar la app completa

1. En **http://localhost:5173** escribí una tarea: "Comprar leche"
2. Click en **Agregar** → la tarea aparece en la lista
3. Marcala como completada (checkbox) → se tacha el texto
4. Eliminala (botón ×) → desaparece

### E.2 Verificar con Swagger

1. Abrí **http://localhost:8000/docs**
2. Creá una tarea desde Swagger (`POST /api/tasks`)
3. Volvé a **http://localhost:5173** → la tarea debería aparecer (recargá si hace falta)

### E.3 Probar el manejo de errores

1. Apagá el backend (`CTRL+C` en la terminal del backend)
2. En el frontend, agregá una tarea
3. Debe aparecer el mensaje de error rojo: "No se pudo conectar con el backend..."
4. Volvé a prender el backend y recargá

---

## Resumen de archivos creados

| # | Archivo | Ubicación |
|---|---------|-----------|
| 1 | `pyproject.toml` | `backend/` |
| 2 | `main.py` | `backend/` |
| 3 | `package.json` | `frontend/` |
| 4 | `index.html` | `frontend/` |
| 5 | `vite.config.js` | `frontend/` |
| 6 | `main.jsx` | `frontend/src/` |
| 7 | `api.js` | `frontend/src/` |
| 8 | `App.jsx` | `frontend/src/` |
| 9 | `App.css` | `frontend/src/` |

**¿Los tenés todos?** ¡Felicitaciones — construiste una app fullstack desde cero! 🎉

---

## Ejercicios para después de clase

### Nivel 🟢 Comprensión
1. Abrí Swagger y contá cuántos endpoints tiene la API
2. Modificá el mensaje del health check y recargá Swagger
3. Eliminá `created_at` del modelo `Task` — ¿qué pasa?

### Nivel 🟡 Aplicación
4. Agregá un campo `priority` (baja/media/alta) a las tareas
5. Agregá un endpoint `GET /api/tasks/stats` que devuelva totales
6. Creá filtros en el frontend: "Todas", "Pendientes", "Completadas"

### Nivel 🔴 Análisis
7. Investigá: ¿por qué `PATCH` y no `PUT` para el toggle?
8. Reemplazá el almacenamiento en memoria por un archivo JSON
9. Agregá autenticación con JWT

---

> *La Universidad te da el mapa. El recorrido lo hacés vos.*
