---
marp: true
theme: default
paginate: true
backgroundColor: #0f172a
color: #e2e8f0
style: |
  /* ---- Base ---- */
  section {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    padding: 60px 70px;
    background-color: #0f172a;
    color: #e2e8f0;
  }
  h1 { color: #f8fafc; font-size: 1.8em; }
  h2 { color: #f1f5f9; font-size: 1.4em; }
  h3 { color: #94a3b8; font-size: 1.1em; }
  h4 { color: #60a5fa; }
  strong { color: #f1f5f9; }
  em { color: #cbd5e1; }
  a { color: #60a5fa; }

  /* ---- Código ---- */
  code {
    color: #60a5fa;
    background: #1e293b;
    padding: 2px 6px;
    border-radius: 4px;
    font-size: 0.9em;
  }
  pre {
    background: #1e293b;
    border: 1px solid #334155;
    border-radius: 8px;
    padding: 16px 20px;
    font-size: 0.8em;
    color: #e2e8f0;
  }
  pre code {
    background: none;
    padding: 0;
    color: #e2e8f0;
  }

  /* ---- Tablas ---- */
  table {
    font-size: 0.8em;
    background: #1e293b;
    border-radius: 8px;
    overflow: hidden;
    border-collapse: collapse;
    width: 100%;
  }
  thead { background: #334155; }
  th {
    color: #60a5fa;
    padding: 10px 16px;
    text-align: left;
    border-bottom: 2px solid #3b82f6;
    background: #334155;
  }
  td {
    color: #cbd5e1;
    padding: 10px 16px;
    border-bottom: 1px solid #334155;
    background: #1e293b;
  }
  tr:hover td { background: #263348; }

  /* ---- Blockquote ---- */
  blockquote {
    border-left: 4px solid #3b82f6;
    background: #1e293b;
    padding: 14px 20px;
    border-radius: 0 8px 8px 0;
    margin: 16px 0;
  }
  blockquote p {
    color: #94a3b8;
    font-style: italic;
  }

  /* ---- Listas ---- */
  ul { list-style-type: none; padding-left: 0; }
  ul li::before { content: "▸ "; color: #60a5fa; font-weight: bold; }
  ul li { color: #cbd5e1; line-height: 1.8; }
  ol li { color: #cbd5e1; line-height: 1.8; }

  /* ---- Lead slides ---- */
  section.lead h1 { font-size: 2.5em; }
  section.lead p { color: #64748b; }

  /* ---- Checkpoint ---- */
  section.checkpoint {
    background-color: #052e16;
  }
  section.checkpoint h1 {
    color: #34d399;
    font-size: 2em;
  }
  section.checkpoint p, section.checkpoint li {
    color: #a7f3d0;
  }

  /* ---- Footer ---- */
  footer { color: #475569; font-size: 0.6em; }
---

<!-- _class: lead -->
<!-- note: |
  Bienvenidos al taller. Hoy NO vamos a clonar nada — construimos
  el proyecto DESDE CERO, archivo por archivo.
  El material de trabajo es la GUIA_ALUMNO.md que cada uno tiene
  abierta en su navegador. Todo el código está ahí, completo.
  La presentación les muestra el QUÉ y el POR QUÉ; la guía tiene el CÓMO.
  Decirles: "abrí GUIA_ALUMNO.md en tu navegador y dejalo abierto".
  Timing: 0-5 min
-->

# 🚀 Mi Primera APP

## Construida desde cero en 90 minutos

FastAPI + React + Vite

**Material de trabajo**: `GUIA_ALUMNO.md` (abierta en tu navegador)

---

<!-- _class: lead -->
<!-- note: |
  Explicar el objetivo: app de Tareas (CRUD).
  El foco NO es aprender frameworks: es entender el ciclo HTTP.
  Preguntar: ¿quién hizo alguna vez un fetch? ¿quién sabe qué es REST?
  Timing: 5-10 min
-->

# Objetivo del Taller

Construir una app de **Tareas** con API REST y frontend web.

- 🖥️ **Backend**: API REST con FastAPI en Python — 4 endpoints
- 🌐 **Frontend**: Interfaz web con React — consume la API

> El foco NO es aprender frameworks. Es entender el **ciclo HTTP**.

---

<!-- note: |
  Mostrar el diagrama. Dos procesos independientes que se comunican
  por HTTP. El frontend NO sabe del backend, y viceversa.
  Preguntar: ¿por qué es importante esta separación?
  (Respuesta: pueden escalar y evolucionar por separado)
  Timing: 10-13 min
-->

# Arquitectura

```
┌──────────────────┐      HTTP/JSON       ┌──────────────────┐
│                  │  ◄──────────────►    │                  │
│    Frontend      │    /api/tasks        │    Backend       │
│  React + Vite    │                      │   FastAPI        │
│    :5173         │                      │    :8000         │
└──────────────────┘                      └──────────────────┘
```

Dos procesos independientes que se comunican por **HTTP**.

---

<!-- note: |
  Recorrer la tabla de endpoints.
  GET lee, POST crea, PATCH actualiza parcial, DELETE elimina.
  Esto es CRUD. Preguntar: ¿cuál es idempotente?
  (GET, PATCH, DELETE — hacerlos 2 veces da el mismo resultado)
  Timing: 13-18 min
-->

# La API — 4 Operaciones

| Método  | Ruta                | Qué hace                          |
| ------- | ------------------- | --------------------------------- |
| `GET`   | `/api/tasks`        | Listar todas las tareas            |
| `POST`  | `/api/tasks`        | Crear una tarea nueva              |
| `PATCH` | `/api/tasks/{id}`   | Marcar como hecha / desmarcar      |
| `DELETE`| `/api/tasks/{id}`   | Eliminar una tarea                 |

Esto es un patrón **CRUD** — Create, Read, Update, Delete.

---

<!-- note: |
  PATCH vs PUT — pregunta clásica de entrevista.
  PATCH: actualización parcial, envío solo lo que cambió.
  PUT: reemplazo completo.
  En el toggle solo cambiamos "completed" → PATCH es lo correcto.
  Timing: 18-22 min
-->

# ¿PATCH o PUT?

<div style="display: flex; gap: 40px; text-align: left;">
<div>

### PATCH — Actualización parcial

Enviás SOLO el campo que cambia.

```json
{ "completed": true }
```

</div>
<div>

### PUT — Reemplazo completo

Enviás TODA la tarea.

```json
{
  "id": 1,
  "title": "Comprar leche",
  "completed": true,
  "created_at": "2026-08-04T..."
}
```

</div>
</div>

Usamos **PATCH** porque solo cambiamos un campo.

---

<!-- _class: lead -->
<!-- note: |
  Acá arranca la parte práctica. Darles 3-5 min para verificar
  herramientas y crear la estructura de directorios.
  Si alguien no tiene algo instalado, resolverlo en paralelo.
  Referencia: GUIA_ALUMNO.md Parte A.
  Timing: 22-27 min
-->

# Fase 1 — Setup

Verificar herramientas + estructura de directorios

---

# Verificar Herramientas

Cada comando debe responder una versión:

```bash
python3 --version      # Python 3.12+
uv --version           # gestor de paquetes Python
node --version         # Node.js 18+
pnpm --version         # gestor de paquetes Node
```

> **¿Falta alguna?** Avisá al docente antes de continuar.

---

# Estructura de Directorios

```bash
mkdir -p 01-mi-primera-app/backend
mkdir -p 01-mi-primera-app/frontend/src
mkdir -p 01-mi-primera-app/frontend/public
```

```
01-mi-primera-app/
├── backend/
└── frontend/
    ├── public/
    └── src/
```

> Detalles en `GUIA_ALUMNO.md` — Parte A

---

<!-- _class: lead -->
<!-- note: |
  Fase 2: el backend. Los alumnos van a crear 2 archivos
  (pyproject.toml y main.py) copiando de la guía.
  IMPORTANTE: darles tiempo para copiar, no apurarlos.
  El código completo está en GUIA_ALUMNO.md Parte B.
  Timing: 27-50 min
-->

# Fase 2 — Backend desde cero

2 archivos, ~215 líneas, 1 servidor corriendo

---

# pyproject.toml — El Manifiesto

**Creá `backend/pyproject.toml`** — copiá de la guía Parte B.1

```toml
[project]
name = "mi-primera-app-backend"
version = "0.1.0"
requires-python = ">=3.12"
dependencies = [
    "fastapi>=0.115.0",
    "uvicorn[standard]>=0.30.0",
]
```

**¿Qué es?** El manifiesto del proyecto Python. `uv` lo lee para instalar las dependencias.

---

# main.py — La API Completa

**Creá `backend/main.py`** — copiá de la guía Parte B.2 (~200 líneas)

Estructura del archivo:

| Sección | Qué hace |
|---------|----------|
| **Modelos Pydantic** | `TaskCreate` (entrada) y `Task` (salida) |
| **Almacenamiento** | Lista en memoria (`tasks = []`) |
| **Aplicación** | Instancia de `FastAPI` con título y versión |
| **CORS** | Permite que el frontend hable con el backend |
| **Endpoints** | GET, POST, PATCH, DELETE + health check |
| **Main** | Arranca uvicorn con hot-reload |

> **Tip**: copiá el archivo completo de la guía. No lo escribas de memoria.

---

# Modelos de Datos — Por qué dos

```python
class TaskCreate(BaseModel):
    # Lo que el cliente ENVÍA (solo título)
    title: str = Field(..., min_length=1, max_length=200)

class Task(BaseModel):
    # Lo que el servidor DEVUELVE (con ID y metadata)
    id: int
    title: str
    completed: bool
    created_at: str
```

Separar **entrada** de **salida** es un patrón fundamental. El cliente no necesita enviar el ID — lo genera el servidor.

---

# Instalar y Ejecutar

```bash
cd 01-mi-primera-app/backend
uv sync          # instala las dependencias
uv run main.py   # arranca el servidor
```

Debés ver: `Uvicorn running on http://127.0.0.1:8000`

> ⚠️ **No cierres esta terminal** — el servidor queda corriendo.

---

<!-- _class: checkpoint -->
<!-- note: |
  CHECKPOINT 1 — el momento más importante de la fase.
  NO avanzar hasta que TODOS tengan Swagger andando.
  Recorrer el aula, verificar que cada uno tenga
  localhost:8000/docs cargando.
  Si alguien se atrasó, usar los 5-10 min para que lo resuelva.
  Timing: ~50 min
-->

# ✅ Checkpoint 1 — Swagger

Abrí **http://localhost:8000/docs**

Debés ver la interfaz de Swagger con los 4 endpoints.

**¿No aparece?** Revisá:
- ¿La terminal muestra errores?
- ¿Copiaste `main.py` completo?

**Esperá al docente antes de avanzar.**

---

<!-- _class: lead -->
<!-- note: |
  Fase 3: verificación. La API ya está corriendo.
  Mostrar Swagger en vivo, luego curl, luego Postman/Bruno.
  El objetivo: que entiendan que hay MÚLTIPLES clientes
  que pueden hablar con la misma API.
  Referencia: GUIA_ALUMNO.md Parte C.
  Timing: 50-60 min
-->

# Fase 3 — Verificar la API

La API ya está corriendo. Probémosla con 3 clientes distintos.

---

# Probar con Swagger y curl

**Swagger** (navegador): `http://localhost:8000/docs`

**curl** (terminal):

```bash
# Crear una tarea
curl -X POST http://localhost:8000/api/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "Aprender FastAPI"}'

# Listar
curl http://localhost:8000/api/tasks
```

> La misma API responde a cualquier cliente. Swagger, curl, Postman — todos hablan HTTP.

---

# Probar con Postman / Bruno

1. Creá una Collection "Mi Primera APP"
2. Agregá los 4 requests

| Nombre | Método | URL |
|--------|--------|-----|
| Listar | `GET` | `/api/tasks` |
| Crear | `POST` | `/api/tasks` |
| Toggle | `PATCH` | `/api/tasks/1` |
| Eliminar | `DELETE` | `/api/tasks/1` |

> Postman y Bruno son las herramientas que usa la industria para testear APIs.

---

<!-- _class: lead -->
<!-- note: |
  Fase 4: el frontend, la más larga.
  7 archivos, ~490 líneas, 1 servidor corriendo.
  IMPORTANTE: avisarles que NO usan pnpm create vite —
  escriben todos los archivos a mano, así entienden la estructura.
  Referencia: GUIA_ALUMNO.md Parte D.
  Timing: 60-80 min
-->

# Fase 4 — Frontend desde cero

7 archivos, ~490 líneas, 1 servidor corriendo

---

# Los 7 Archivos del Frontend

**Todos se copian de la guía Parte D, en este orden:**

| # | Archivo | Qué es |
|---|---------|--------|
| 1 | `package.json` | Manifiesto del proyecto (JSON estricto) |
| 2 | `index.html` | El único HTML — React dibuja dentro de `#root` |
| 3 | `vite.config.js` | Configuración de Vite + proxy a :8000 |
| 4 | `src/main.jsx` | Punto de entrada de React |
| 5 | `src/api.js` | Comunicación con el backend (fetch) |
| 6 | `src/App.jsx` | La UI completa |
| 7 | `src/App.css` | Los estilos |

> **¿Por qué a mano y no `pnpm create vite`?** Para que entiendas la estructura de verdad.

---

# package.json — JSON es estricto

**Creá `frontend/package.json`** — copiá de la guía Parte D.1

```json
{
  "name": "mi-primera-app-frontend",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "vite build"
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

> **CUIDADO**: una coma de más o de menos en JSON rompe todo.

---

# index.html y vite.config.js

**Creá `frontend/index.html`** y **`frontend/vite.config.js`** — guía D.2 y D.3

```html
<!-- index.html -->
<div id="root"></div>
<script type="module" src="/src/main.jsx"></script>
```

```javascript
// vite.config.js — el proxy es CLAVE
export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      "/api": { target: "http://localhost:8000" }
    }
  }
})
```

**El proxy**: cuando el frontend hace `fetch("/api/tasks")`, Vite lo redirige a `localhost:8000`. Sin esto, el navegador bloquea la petición por CORS.

---

# main.jsx — El Punto de Entrada

**Creá `frontend/src/main.jsx`** — guía D.4

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

Toma el `<div id="root">` del HTML y monta la app dentro.

---

# api.js — La Capa de Comunicación

**Creá `frontend/src/api.js`** — guía D.5

```javascript
const API_BASE = "/api";

async function request(url, options = {}) {
  const response = await fetch(`${API_BASE}${url}`, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  return response.json();
}

export async function fetchTasks() { return request("/tasks"); }
export async function createTask(title) {
  return request("/tasks", {
    method: "POST",
    body: JSON.stringify({ title }),
  });
}
```

**Separación de responsabilidades**: `App.jsx` solo maneja UI; `api.js` solo habla con el backend.

---

# App.jsx — La UI Completa

**Creá `frontend/src/App.jsx`** — guía D.6 (~160 líneas)

Los 4 conceptos de React que usás:

| Concepto | Uso en la app |
|----------|---------------|
| `useState` | Guarda la lista de tareas y el input |
| `useEffect` | Carga las tareas al montar la app |
| `.map()` | Renderiza cada tarea como un elemento |
| `.filter()` | Elimina la tarea del estado |

> Copiá el archivo completo de la guía.

---

# App.css — Los Estilos

**Creá `frontend/src/App.css`** — guía D.7

```css
.app { max-width: 600px; margin: 40px auto; }
.task-item {
  display: flex;
  justify-content: space-between;
  background: white;
  padding: 12px 16px;
  border-radius: 8px;
}
.task-item.completed .task-title {
  text-decoration: line-through;
  color: #999;
}
```

> El archivo completo tiene más clases: formulario, botones, errores, estados.

---

# Instalar y Ejecutar

```bash
cd 01-mi-primera-app/frontend
pnpm install    # instala React, Vite y el plugin
pnpm dev        # arranca el dev server
```

Debés ver: `➜ Local: http://localhost:5173/`

> ⚠️ **No cierres esta terminal** — el frontend queda corriendo.

---

<!-- _class: checkpoint -->
<!-- note: |
  CHECKPOINT 2 — todos deben tener la app andando en :5173.
  Recorrer el aula, verificar que cada uno vea la interfaz con el input.
  Si alguien tiene errores, revisar consola de pnpm dev y del navegador.
  Los errores más comunes: typo en package.json, archivo mal ubicado.
  Timing: ~80 min
-->

# ✅ Checkpoint 2 — Frontend andando

Abrí **http://localhost:5173**

Debés ver la app con el input para agregar tareas.

**¿Aparece la página de Vite pero sin tu app?** Revisá:
- ¿Creaste los archivos en las rutas correctas?
- ¿La terminal de `pnpm dev` muestra errores?

**Esperá al docente antes de avanzar.**

---

<!-- _class: lead -->
<!-- note: |
  Fase 5: la integración — el momento más lindo.
  Ambos servidores corriendo, la app consume la API.
  Dar 5 min para la verificación completa.
  Referencia: GUIA_ALUMNO.md Parte E.
  Timing: 80-90 min
-->

# Fase 5 — Integración

Los dos servidores trabajando juntos

---

# Verificar la Integración

Con ambos servidores corriendo:

1. Escribí "Comprar leche" y click en **Agregar**
2. La tarea aparece en la lista
3. Marcala como completada — se tacha
4. Eliminala con el botón ×

**Bonus**: creá una tarea en Swagger y refrescá el frontend — aparece ahí.

> **¿Funcionó?** Construiste una app fullstack desde cero. 🎉

---

# Cierre — El Ciclo de Vida

| #  | Fase              | Qué hicimos hoy                    |
| -- | ----------------- | ---------------------------------- |
| 1  | **Requisitos**    | Definimos la API (4 endpoints)     |
| 2  | **Diseño**        | Arquitectura client-server         |
| 3  | **Implementación**| 9 archivos creados desde cero      |
| 4  | **Testing**       | Swagger, curl, Postman, frontend   |
| 5  | Deployment        | *(Futuro)* Docker + hosting        |
| 6  | Mantenimiento     | *(Futuro)* Features + fixes        |

> El software no es solo código: es requisitos → diseño → código → testing → deploy → mantenimiento.

---

# Ejercicios para Llevar a Casa

<div style="display: flex; gap: 30px; text-align: left;">
<div>

### 🟢 Comprensión
1. ¿Cuántos endpoints tiene la API?
2. Modificá el health check.
3. Eliminá `created_at` del modelo.

</div>
<div>

### 🟡 Aplicación
4. Agregá campo `priority`.
5. Agregá endpoint de estadísticas.
6. Creá filtros en el frontend.

</div>
</div>

### 🔴 Análisis
7. Investigá PATCH vs PUT.
8. Almacenamiento JSON en vez de memoria.
9. Autenticación con JWT.

---

<!-- _class: lead -->
<!-- note: |
  Cierre. Repasar lo logrado: 9 archivos creados a mano,
  2 servidores, 1 app funcionando.
  Recordarles que la GUIA_ALUMNO.md y el repo quedan disponibles.
  Próximo módulo: profundizamos HTTP y arquitectura.
-->

# 🎓 ¡Listo!

Construiste tu primera app fullstack **desde cero** en 90 minutos.

| Backend | Frontend | Swagger |
| ------- | -------- | ------- |
| `uv run main.py` | `pnpm dev` | `localhost:8000/docs` |

> *La Universidad te da el mapa. El recorrido lo hacés vos.*
