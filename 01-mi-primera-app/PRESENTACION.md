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
    font-size: 0.82em;
    color: #e2e8f0;
  }
  pre code {
    background: none;
    padding: 0;
    color: #e2e8f0;
  }

  /* ---- Tablas ---- */
  table {
    font-size: 0.82em;
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

  /* ---- Footer ---- */
  footer { color: #475569; font-size: 0.6em; }

  /* ---- Diagrames / ASCII art ---- */
  pre:has(code) { background: #1e293b; }
---

<!-- _class: lead -->
<!-- note: |
  Bienvenidos al taller "Mi Primera APP". Este es el primer módulo práctico
  donde van a construir una app fullstack de principio a fin.
  El objetivo es que entiendan el ciclo HTTP completo: backend, frontend,
  y cómo se comunican. NO es un curso de frameworks.
-->

# 🚀 Mi Primera APP

## API REST + Frontend en 90 minutos

FastAPI + React + Vite

Desarrollo de Software 2026 — UTN FRLP

---

<!-- note: |
  Explicar que van a construir una API de Tareas (To-Do List).
  Es un CRUD clásico: Crear, Leer, Actualizar, Eliminar.
  El foco está en entender el protocolo HTTP, no en aprender FastAPI o React.
  Preguntar: ¿Quién hizo alguna vez un fetch a una API? ¿Quién sabe qué es REST?
-->

# Objetivo del Taller

Construir una app de **Tareas** con API REST y frontend web.

- 🖥️ **Backend**: API REST con FastAPI en Python — 4 endpoints
- 🌐 **Frontend**: Interfaz web con React — consume la API

> El foco NO es aprender frameworks. Es entender el **ciclo HTTP**.

---

<!-- note: |
  Mostrar el diagrama de arquitectura. Explicar que son DOS procesos
  independientes que se comunican por HTTP. El frontend NO sabe nada
  del backend y viceversa. Solo se comunican por HTTP/JSON.
  Preguntar: ¿Por qué es importante esta separación?
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

El frontend hace `fetch`, el backend responde con `JSON`.

---

<!-- note: |
  Mostrar la tabla de los 4 endpoints. Explicar cada uno:
  - GET: lee datos (no modifica nada)
  - POST: crea un recurso nuevo
  - PATCH: actualiza parcialmente
  - DELETE: elimina
  Esto es un patrón CRUD. Preguntar: ¿Cuál de estos es idempotente?
  (GET, PATCH y DELETE son idempotentes — hacerlo 2 veces da el mismo resultado)
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
  Esta es una pregunta que aparece mucho en entrevistas técnicas.
  PATCH = actualización parcial (solo envío lo que cambió).
  PUT = reemplazo completo (envío todo el recurso).
  Ejemplo: si tengo {id:1, title:"Comprar", completed:false, created_at:"..."}
  con PATCH solo envío {"completed": true}.
  Con PUT tendría que enviar TODO el objeto.
  FastAPI maneja ambos, pero para toggle, PATCH es más correcto.
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
  Acá arrancamos la parte práctica. Los estudiantes van a instalar las
  herramientas. Darles 5-10 minutos para que instalen todo.
  Si alguien tiene problemas, resolver en paralelo.
-->

# Fase 1 — Instalación de Herramientas

---

<!-- note: |
  Explicar cada herramienta y por qué la necesitamos.
  Python: lenguaje del backend.
  uv: reemplaza pip, es 100x más rápido.
  Node.js: runtime de JavaScript para el frontend.
  pnpm: gestor de paquetes Node (npm está bloqueado por el firewall de la UTN).
  Dar tiempo para que instalen. Los que ya tengan algo, que verifiquen versiones.
-->

# Instalación de Herramientas

| Herramienta     | Para qué                  | Verificar          |
| --------------- | ------------------------- | ------------------ |
| **Python 3.12+**| Lenguaje del backend      | `python3 --version`|
| **uv**          | Gestor de paquetes Python | `uv --version`     |
| **Node.js 22**  | Runtime de JavaScript     | `node --version`   |
| **pnpm**        | Gestor de paquetes Node   | `pnpm --version`   |

Ver `README.md` para instrucciones detalladas por SO.

---

<!-- note: |
  uv es relativamente nuevo. Explicar que reemplaza pip+venv+pip-tools.
  La ventaja principal es la velocidad (~100ms vs ~30s de pip).
  Mostrar el comando de instalación para cada SO.
  Si alguien tiene problemas con curl, puede descargar el binario directo
  desde https://github.com/astral-sh/uv/releases
-->

# uv — El gestor de paquetes Python

uv reemplaza `pip`, `venv` y `pip-tools` con **un solo comando**.

```bash
# Instalar uv (Linux / macOS)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Crear proyecto
uv init mi-backend
cd mi-backend

# Agregar dependencias
uv add fastapi "uvicorn[standard]"

# Ejecutar
uv run main.py
```

**~100ms** vs los ~30s de pip 🏎️

---

<!-- _class: lead -->
<!-- note: |
  Arrancamos con el backend. Los estudiantes van a crear el proyecto
  y levantar el servidor. Darles 10 minutos para que tengan el backend
  corriendo. Verificar que todos tengan Swagger funcionando.
-->

# Fase 2 — Crear el Backend

---

<!-- note: |
  Guíar paso a paso:
  1. cd al directorio
  2. uv sync (instala dependencias)
  3. uv run main.py (levanta servidor)
  Verificar que aparezca "Uvicorn running on http://127.0.0.1:8000"
  Si alguien tiene error, revisar que Python 3.12+ esté instalado.
-->

# Crear el Backend

```bash
# Entrar al directorio
cd 01-mi-primera-app/backend

# Instalar dependencias
uv sync

# Ejecutar el servidor
uv run main.py
```

El servidor arranca en `http://localhost:8000`

> ⚠️ No cierres esta terminal — necesitás el servidor corriendo.

---

<!-- note: |
  Explicar el concepto de Pydantic: validación automática de datos.
  TaskCreate = lo que el cliente envía (solo título).
  Task = lo que el servidor devuelve (con ID y metadata).
  ¿Por qué dos modelos? Porque el cliente no debería enviar el ID
  ni la fecha — eso lo genera el servidor.
  Mostrar que si mandás un title vacío, Pydantic devuelve error 422.
-->

# El Código — Modelos de Datos

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

**¿Por qué dos modelos?**

Separar entrada de salida es un patrón fundamental. El cliente no necesita enviar el ID — lo genera el servidor.

---

<!-- note: |
  Explicar cada endpoint brevemente.
  - @app.get: decorator que dice "este handle responde GET"
  - status_code=201: es el código correcto para "recurso creado"
  - find_task: busca en la lista, devuelve None si no existe
  - raise HTTPException: FastAPI convierte esto en respuesta HTTP con error
  Preguntar: ¿Qué pasa si hago POST dos veces con el mismo título?
  (Se crean dos tareas — no hay uniqueness constraint)
-->

# El Código — Endpoints

```python
@app.get("/api/tasks")
def list_tasks():
    return tasks

@app.post("/api/tasks", status_code=201)
def create_task(body: TaskCreate):
    task = {"id": next_id, "title": body.title, "completed": False}
    tasks.append(task)
    return task

@app.patch("/api/tasks/{task_id}")
def toggle_task(task_id: int):
    task = find_task(task_id)
    task["completed"] = not task["completed"]
    return task
```

---

<!-- _class: lead -->
<!-- note: |
  Acá es donde la magia de FastAPI brilla. Swagger se genera
  automáticamente del código. Abrir http://localhost:8000/docs
  y mostrar la interfaz interactiva. Probar cada endpoint en vivo.
-->

# Fase 3 — Verificar la API

---

<!-- note: |
  Tres formas de probar:
  1. Swagger: la más visual, ideal para principiantes
  2. Postman/Bruno: herramientas profesionales, las que usan en la industria
  3. curl: el más básico, viene en todos los SO
  Mostrar Swagger en vivo. Crear una tarea, listar, toggle, eliminar.
  Preguntar: ¿Qué diferencia ven entre Swagger y Postman?
  (Swagger es más rápido para testing rápido, Postman tiene más features
  como collections, environments, scripts pre-request)
-->

# Verificar la API

Tres formas de probar que funciona:

### 📖 Swagger UI
`http://localhost:8000/docs` — Interfaz interactiva para probar cada endpoint.

### 🔧 Postman / Bruno
Herramientas externas para testing de APIs.

### 💻 curl

```bash
curl -X POST http://localhost:8000/api/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "Hola"}'
```

---

<!-- note: |
  Mostrar Swagger en vivo. Hacer un recorrido por la interfaz:
  - Los endpoints aparecen listados
  - Click en "Try it out"
  - Enviar request
  - Ver la respuesta
  Explicar que esto se genera automáticamente de los type hints y
  Pydantic models. Sin configuración extra.
  Probar crear, listar, toggle y eliminar.
-->

# Swagger UI — La Magia de FastAPI

Abrí `http://localhost:8000/docs` y probá:

```bash
# Crear tarea
POST /api/tasks
{ "title": "Aprender FastAPI" }

# Listar tareas
GET /api/tasks

# Toggle (marcar completada)
PATCH /api/tasks/1

# Eliminar
DELETE /api/tasks/1
```

> Swagger genera la documentación automáticamente a partir del código.

---

<!-- _class: lead -->
<!-- note: |
  Arrancamos con el frontend. Los estudiantes van a crear el proyecto
  React con Vite. Darles 10 minutos para que tengan el frontend
  corriendo. Verificar que todos vean la página de Vite.
-->

# Fase 4 — Crear el Frontend

---

<!-- note: |
  pnpm create vite . --template react crea el proyecto en el directorio actual.
  Si no funciona con el punto, usar un nombre temporal y mover archivos.
  pnpm install instala las dependencias.
  pnpm dev levanta el dev server en :5173.
  Verificar que todos vean "Vite + React" en el navegador.
-->

# Crear el Frontend

```bash
# Crear proyecto React con Vite
cd 01-mi-primera-app/frontend
pnpm create vite . --template react

# Instalar dependencias
pnpm install

# Ejecutar
pnpm dev
```

El frontend arranca en `http://localhost:5173`

> Con **ambos servidores corriendo**, abrí la app en el navegador.

---

<!-- note: |
  Explicar el proxy de Vite. Es un concepto importante:
  En desarrollo, el frontend (:5173) y backend (:8000) están en puertos
  diferentes. Sin proxy, el navegador bloquearía los fetch por CORS.
  El proxy redirige /api/* al backend, evitando el problema.
  En producción NO existe el proxy — se usa nginx o similar.
  Preguntar: ¿Qué pasaría si no tuviéramos el proxy?
  (Error CORS en el navegador)
-->

# El Proxy de Vite

```javascript
// vite.config.js
export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      "/api": {
        target: "http://localhost:8000",
        changeOrigin: true,
      }
    }
  }
})
```

**¿Qué hace?**

Cuando el frontend hace `fetch("/api/tasks")`, Vite lo redirige a `localhost:8000/api/tasks`.

El frontend no sabe que el backend está en otro puerto. Simplifica todo.

---

<!-- note: |
  Explicar la separación de responsabilidades.
  api.js es la ÚNICA capa que habla con el backend.
  Si mañana cambiamos la URL base, o agregamos auth, o cambiamos a axios,
  todo se cambia en UN solo lugar.
  El componente App.jsx no se entera — solo llama a fetchTasks(), createTask(), etc.
  Esto es el principio DRY (Don't Repeat Yourself) y Single Responsibility.
-->

# La Capa de Comunicación

```javascript
// api.js — Toda la comunicación con el backend

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

**Separación de responsabilidades**: el componente solo maneja UI, el servicio solo maneja HTTP.

---

<!-- note: |
  Repasar los conceptos clave de React para este taller.
  useState: guarda datos que cambian (la lista de tareas).
  useEffect: ejecuta código al montar (cargar tareas del backend).
  JSX: HTML dentro de JavaScript.
  Eventos: onClick, onChange, onSubmit.
  No profundizar mucho — es un taller de 90 minutos.
  Si preguntan por más, decir que lo veremos en módulos futuros.
-->

# React — Lo que necesitás saber

<div style="display: flex; gap: 30px; text-align: left;">
<div>

### useState
Guarda datos que cambian.
Ej: la lista de tareas.

### useEffect
Ejecuta código al montar.
Ej: cargar tareas al iniciar.

</div>
<div>

### JSX
HTML dentro de JavaScript.
Lo que ves en pantalla.

### Eventos
onClick, onChange, onSubmit.
El usuario interactúa.

</div>
</div>

---

<!-- note: |
  Este diagrama es clave para entender React.
  El flujo es: Estado → Render → UI.
  Cuando el estado cambia (setTasks), React re-renderiza el componente.
  El .map() convierte el array de tareas en elementos JSX.
  Explicar que React NO muta el estado — crea nuevos arrays.
  setTasks([...tasks, newTask]) crea un array nuevo.
  tasks.push(newTask) sería mutación (MAL).
-->

# React — El Flujo de Datos

```
Componente (App.jsx)
       │
       ▼  useState
  Estado (tasks[])
       │
       ▼  .map()
  UI Renderizada
```

React re-renderiza cuando el estado cambia.

Actualizás el estado → la UI se actualiza sola.

---

<!-- _class: lead -->
<!-- note: |
  Acá verificamos que todo funcione junto. Los estudiantes deben tener
  ambos servidores corriendo. Darles 5 minutos para probar la integración.
  Si funciona, ¡ya tienen su primera app fullstack!
-->

# Fase 5 — Verificar la Integración

---

<!-- note: |
  Guiar la verificación paso a paso:
  1. Abrir localhost:5173
  2. Agregar una tarea
  3. Verificar que aparece en la lista
  4. Marcar como completada
  5. Eliminar
  Si funciona, felicitarlos. Es su primera app fullstack.
  Si no funciona, revisar: ¿está corriendo el backend?
  ¿Está el proxy configurado? ¿Hay errores en la consola del navegador?
-->

# Verificar la Integración

Con ambos servidores corriendo:

1. Abrí `http://localhost:5173`
2. Escribí una tarea y hacé click en "Agregar"
3. Verificá que aparece en la lista
4. Marcala como completada (checkbox)
5. Eliminala (botón ×)

**¿Funcionó?** ¡Felicidades! Tu primera app fullstack. 🎉

---

<!-- note: |
  Cerrar con una visión general del ciclo de vida del software.
  Lo que hicimos hoy cubre las primeras 4 fases.
  En módulos futuros cubriremos deployment y mantenimiento.
  La idea es que entiendan que software no es solo código —
  es requisitos, diseño, implementación, testing, deploy, mantenimiento.
  Un ingeniero que solo sabe codear no es un ingeniero completo.
-->

# El Ciclo de Vida del Software

Lo que hicimos hoy cubre las primeras 4 fases:

| #  | Fase              | Qué hicimos                              |
| -- | ----------------- | ---------------------------------------- |
| 1  | **Requisitos**    | Definimos qué hace la app (4 endpoints)  |
| 2  | **Diseño**        | Arquitectura client-server, modelos      |
| 3  | **Implementación**| Escribimos el código                     |
| 4  | **Testing**       | Swagger, Postman, curl                   |
| 5  | Deployment        | *(Futuro)* Docker + hosting              |
| 6  | Mantenimiento     | *(Futuro)* Features + fixes              |

---

<!-- note: |
  Dar los ejercicios para quien quiera seguir practicando.
  Los nivel 🟢 son para reforzar lo visto en clase.
  Los nivel 🟡 requieren investigar un poco más.
  Los nivel 🔴 son para los más avanzados — pueden llevar días.
  Recomendar que empiecen por los 🟢 y avancen a su ritmo.
-->

# Ejercicios para Llevar a Casa

<div style="display: flex; gap: 30px; text-align: left;">
<div>

### 🟢 Comprensión
1. Abrí Swagger y contá cuántos endpoints hay.
2. Modificá el health check y recargá.
3. Eliminá `created_at` del modelo.

</div>
<div>

### 🟡 Aplicación
4. Agregá campo `priority` (baja/media/alta).
5. Agregá endpoint de estadísticas.
6. Creá filtros en el frontend.

</div>
</div>

### 🔴 Análisis
7. Investigá PATCH vs PUT.
8. Reemplazá almacenamiento en memoria por JSON.
9. Agregá autenticación con JWT.

---

<!-- _class: lead -->
<!-- note: |
  Cerrar la clase. Repasar lo que hicimos:
  - Instalamos herramientas (uv, pnpm)
  - Creamos una API REST con FastAPI
  - Verificamos con Swagger y Postman
  - Creamos un frontend con React
  - Integramos ambos
  Recordatorio: este material está en el repo. Pueden revisarlo cuando quieran.
  Próximo módulo: profundizaremos en HTTP y arquitectura.
  Despedida con la frase del repo.
-->

# 🎓 ¡Listo!

Construiste tu primera app fullstack en 90 minutos.

| Backend | Frontend | Swagger |
| ------- | -------- | ------- |
| `uv run main.py` | `pnpm dev` | `localhost:8000/docs` |

> *La Universidad te da el mapa. El recorrido lo hacés vos.*
