# Especificación del Software — Mi Primera APP

> **Nombre**: Mi Primera APP — API de Tareas
> **Versión**: 0.1.0
> **Fecha**: Agosto 2026
> **Autor**: Departamento de Desarrollo de Software — UTN FRLP

---

## 1. Introducción

### 1.1 Propósito

Este documento especifica los requisitos, diseño, implementación y plan de testing de una aplicación web de gestión de tareas (To-Do List). La aplicación consta de una API REST en el backend y una interfaz web en el frontend.

### 1.2 Alcance

- API REST con 4 operaciones CRUD (Create, Read, Update, Delete)
- Frontend web interactivo para consumir la API
- Sin persistencia de datos (almacenamiento en memoria)
- Diseñado para taller educativo de 90 minutos

### 1.3 Definiciones

| Término | Definición |
|---------|-----------|
| **API** | Application Programming Interface — contrato de comunicación entre componentes |
| **REST** | Representational State Transfer — estilo arquitectónico para APIs web |
| **CRUD** | Create, Read, Update, Delete — las 4 operaciones básicas de datos |
| **Endpoint** | Punto de acceso de la API (ruta + método HTTP) |
| **JSON** | JavaScript Object Notation — formato de intercambio de datos |
| **CORS** | Cross-Origin Resource Sharing — mecanismo de seguridad del navegador |
| **Pydantic** | Librería de validación de datos para Python |
| **JSX** | JavaScript XML — sintaxis que permite HTML dentro de JavaScript (React) |

---

## 2. Requisitos

### 2.1 Requisitos Funcionales

#### RF-01: Listar tareas

| Campo | Valor |
|-------|-------|
| **ID** | RF-01 |
| **Descripción** | El sistema debe devolver la lista completa de tareas |
| **Método** | `GET` |
| **Ruta** | `/api/tasks` |
| **Entrada** | Ninguna |
| **Salida** | Array de objetos Task |
| **Código HTTP** | 200 OK |

**Ejemplo de respuesta:**
```json
[
  {
    "id": 1,
    "title": "Aprender FastAPI",
    "completed": false,
    "created_at": "2026-08-04T15:30:00+00:00"
  }
]
```

#### RF-02: Crear tarea

| Campo | Valor |
|-------|-------|
| **ID** | RF-02 |
| **Descripción** | El sistema debe crear una tarea nueva con el título proporcionado |
| **Método** | `POST` |
| **Ruta** | `/api/tasks` |
| **Entrada** | JSON con campo `title` (string, 1-200 caracteres, obligatorio) |
| **Salida** | Objeto Task creado |
| **Código HTTP** | 201 Created |
| **Errores** | 422 — Si `title` falta, está vacío o supera 200 caracteres |

**Ejemplo de request:**
```json
POST /api/tasks
Content-Type: application/json

{
  "title": "Comprar leche"
}
```

**Ejemplo de respuesta:**
```json
{
  "id": 1,
  "title": "Comprar leche",
  "completed": false,
  "created_at": "2026-08-04T15:30:00+00:00"
}
```

#### RF-03: Cambiar estado de tarea

| Campo | Valor |
|-------|-------|
| **ID** | RF-03 |
| **Descripción** | El sistema debe alternar el estado `completed` de una tarea |
| **Método** | `PATCH` |
| **Ruta** | `/api/tasks/{task_id}` |
| **Entrada** | `task_id` (path parameter, integer) |
| **Salida** | Objeto Task actualizado |
| **Código HTTP** | 200 OK |
| **Errores** | 404 — Si la tarea con ese ID no existe |

**Justificación de PATCH vs PUT**: Se usa `PATCH` porque estamos modificando un solo campo (`completed`), no reemplazando toda la tarea. `PUT` implica enviar la representación completa del recurso.

#### RF-04: Eliminar tarea

| Campo | Valor |
|-------|-------|
| **ID** | RF-04 |
| **Descripción** | El sistema debe eliminar una tarea por su ID |
| **Método** | `DELETE` |
| **Ruta** | `/api/tasks/{task_id}` |
| **Entrada** | `task_id` (path parameter, integer) |
| **Salida** | `{"ok": true}` |
| **Código HTTP** | 200 OK |
| **Errores** | 404 — Si la tarea con ese ID no existe |

#### RF-05: Health check

| Campo | Valor |
|-------|-------|
| **ID** | RF-05 |
| **Descripción** | El sistema debe exponer un endpoint de verificación de salud |
| **Método** | `GET` |
| **Ruta** | `/api/health` |
| **Salida** | `{"status": "ok", "service": "...", "tasks_count": N}` |

### 2.2 Requisitos No Funcionales

| ID | Requisito | Detalle |
|----|-----------|---------|
| RNF-01 | **Tiempo de respuesta** | < 100ms para cualquier endpoint |
| RNF-02 | **Disponibilidad** | Mientras el servidor esté corriendo (sin persistencia) |
| RNF-03 | **Documentación** | Swagger UI automático en `/docs` |
| RNF-04 | **Compatibilidad** | Backend: Python 3.12+. Frontend: Chrome, Firefox, Safari recientes |
| RNF-05 | **Portabilidad** | Funciona en Linux, macOS y Windows |
| RNF-06 | **Código** | Comentado, con docstrings en español, type hints |

---

## 3. Diseño

### 3.1 Arquitectura

```
┌─────────────────────────────────────────────────────────┐
│                    APLICACIÓN WEB                        │
│                                                         │
│  ┌──────────────┐    HTTP/JSON    ┌──────────────────┐  │
│  │              │  ────────────►  │                  │  │
│  │   Frontend   │  ◄────────────  │    Backend       │  │
│  │              │                 │                  │  │
│  │  React 19    │   /api/tasks    │  FastAPI 0.115+  │  │
│  │  Vite 6      │                 │  Python 3.12+    │  │
│  │  :5173       │                 │  :8000           │  │
│  └──────────────┘                 └──────────────────┘  │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

**Patrón**: Client-Server con comunicación HTTP/JSON.

**Decisiones de diseño**:

1. **API prefix `/api/`**: Permite en producción servir el frontend desde `/` y la API desde `/api/` sin conflictos de rutas.

2. **PATCH para toggle**: Semánticamente correcto — estamos actualizando parcialmente un recurso, no reemplazándolo completo.

3. **Separación api.js / App.jsx**: Patrón de separación de responsabilidades. El componente solo maneja UI; el servicio solo maneja comunicación.

4. **Proxy de Vite**: En desarrollo, el proxy evita problemas de CORS. En producción, se usaría nginx o similar.

### 3.2 Modelo de Datos

#### Task (respuesta)

```
Task {
  id:         integer    // Autoincremental, único
  title:      string     // 1-200 caracteres
  completed:  boolean    // false por defecto
  created_at: string     // ISO 8601 UTC
}
```

#### TaskCreate (entrada)

```
TaskCreate {
  title:      string     // 1-200 caracteres, obligatorio
}
```

### 3.3 Diagrama de Secuencia — Crear Tarea

```
Frontend                 Backend                  Almacén
   │                        │                        │
   │  POST /api/tasks       │                        │
   │  { title: "Hola" }     │                        │
   │  ──────────────────►   │                        │
   │                        │  Validar con Pydantic   │
   │                        │  ──────────────────►   │
   │                        │                        │
   │                        │  Crear task dict       │
   │                        │  ──────────────────►   │
   │                        │                        │
   │                        │  Guardar en lista      │
   │                        │  ──────────────────►   │
   │                        │                        │
   │  201 Created           │                        │
   │  { id: 1, title: ... } │                        │
   │  ◄──────────────────   │                        │
   │                        │                        │
   │  Actualizar UI         │                        │
   │  (agregar a lista)     │                        │
```

### 3.4 Diagrama de Secuencia — Cargar Tareas

```
Frontend                 Backend                  Almacén
   │                        │                        │
   │  GET /api/tasks        │                        │
   │  ──────────────────►   │                        │
   │                        │                        │
   │                        │  Leer lista            │
   │                        │  ──────────────────►   │
   │                        │                        │
   │  200 OK                │                        │
   │  [ { id: 1, ... } ]    │                        │
   │  ◄──────────────────   │                        │
   │                        │                        │
   │  setTasks(data)        │                        │
   │  Renderizar lista      │                        │
```

---

## 4. Especificación de Endpoints

### Resumen

| # | Método | Ruta | Body | Respuesta | Status |
|---|--------|------|------|-----------|--------|
| 1 | `GET` | `/api/tasks` | — | `Task[]` | 200 |
| 2 | `POST` | `/api/tasks` | `TaskCreate` | `Task` | 201 |
| 3 | `PATCH` | `/api/tasks/{task_id}` | — | `Task` | 200 |
| 4 | `DELETE` | `/api/tasks/{task_id}` | — | `{ok: true}` | 200 |
| 5 | `GET` | `/api/health` | — | `HealthStatus` | 200 |

### 4.1 GET /api/tasks

**Descripción**: Devuelve la lista completa de tareas almacenadas en memoria.

**Response Body**:
```json
[
  {
    "id": 1,
    "title": "Aprender FastAPI",
    "completed": false,
    "created_at": "2026-08-04T15:30:00+00:00"
  }
]
```

### 4.2 POST /api/tasks

**Descripción**: Crea una tarea nueva con el título proporcionado.

**Request Body**:
```json
{
  "title": "Comprar leche"
}
```

**Response Body (201)**:
```json
{
  "id": 1,
  "title": "Comprar leche",
  "completed": false,
  "created_at": "2026-08-04T15:30:00+00:00"
}
```

**Errores**:
```json
// 422 — Validation Error
{
  "detail": [
    {
      "type": "string_too_short",
      "loc": ["body", "title"],
      "msg": "String should have at least 1 character",
      "input": "",
      "ctx": { "min_length": 1 }
    }
  ]
}
```

### 4.3 PATCH /api/tasks/{task_id}

**Descripción**: Alterna el estado `completed` de una tarea.

**Path Parameters**:
- `task_id` (integer, requerido): ID de la tarea

**Response Body (200)**:
```json
{
  "id": 1,
  "title": "Aprender FastAPI",
  "completed": true,
  "created_at": "2026-08-04T15:30:00+00:00"
}
```

**Errores**:
```json
// 404 — Not Found
{
  "detail": "Tarea 99 no encontrada"
}
```

### 4.4 DELETE /api/tasks/{task_id}

**Descripción**: Elimina una tarea permanentemente.

**Path Parameters**:
- `task_id` (integer, requerido): ID de la tarea

**Response Body (200)**:
```json
{
  "ok": true
}
```

### 4.5 GET /api/health

**Descripción**: Verifica que el servicio está operativo.

**Response Body (200)**:
```json
{
  "status": "ok",
  "service": "mi-primera-app-backend",
  "tasks_count": 5
}
```

---

## 5. Plan de Testing

### 5.1 Testing de la API (POSTMAN / Bruno / curl)

| # | Test | Input | Esperado | Pass/Fail |
|---|------|-------|----------|-----------|
| T1 | Crear tarea válida | `{"title": "Test"}` | 201 + Task con id | |
| T2 | Crear tarea sin título | `{}` | 422 Error | |
| T3 | Crear tarea título vacío | `{"title": ""}` | 422 Error | |
| T4 | Listar tareas vacío | — | 200 + `[]` | |
| T5 | Listar después de crear | Crear 1 tarea, listar | 200 + array length 1 | |
| T6 | Toggle tarea existente | PATCH /tasks/1 | 200 + completed invertido | |
| T7 | Toggle tarea inexistente | PATCH /tasks/999 | 404 Error | |
| T8 | Eliminar tarea existente | DELETE /tasks/1 | 200 + `{ok: true}` | |
| T9 | Eliminar tarea inexistente | DELETE /tasks/999 | 404 Error | |
| T10 | Health check | GET /api/health | 200 + status ok | |

### 5.2 Testing del Frontend (Manual)

| # | Test | Acción | Esperado | Pass/Fail |
|---|------|--------|----------|-----------|
| F1 | Carga inicial | Abrir localhost:5173 | Página carga sin errores | |
| F2 | Agregar tarea | Escribir título + Enter | Tarea aparece en la lista | |
| F3 | Agregar vacío | No escribir nada + click | Botón deshabilitado | |
| F4 | Completar tarea | Click en checkbox | Tacha el texto | |
| F5 | Descompletar | Click en checkbox de nuevo | Quita la tachadura | |
| F6 | Eliminar tarea | Click en × | Tarea desaparece de la lista | |
| F7 | Contador | Agregar 3, completar 1 | Muestra "1 de 3 completadas" | |
| F8 | Estado vacío | Eliminar todas | Muestra "No hay tareas" | |
| F9 | Backend caído | Apagar backend, recargar front | Muestra error de conexión | |

### 5.3 Testing de Integración

| # | Test | Acción | Esperado | Pass/Fail |
|---|------|--------|----------|-----------|
| I1 | Roundtrip completo | Crear → Listar → Toggle → Eliminar → Listar | Flujo completo sin errores | |
| I2 | Múltiples pestañas | Abrir 2 pestañas, crear en una | La otra no se actualiza (in-memory) | |
| I3 | Reinicio backend | Crear tarea, reiniciar backend, listar | Lista vacía (sin persistencia) | |

---

## 6. Ciclo de Vida del Software (Aplicado a este Proyecto)

### 6.1 Requisitos

¿Qué necesitamos? Una app que permita gestionar tareas con operaciones básicas.
¿Para quién? Estudiantes aprendiendo desarrollo web fullstack.
¿Qué restricciones? 90 minutos, sin DB, herramientas modernas.

### 6.2 Diseño

- **Arquitectura**: Client-Server con dos procesos independientes
- **Backend**: FastAPI (Python) — elegido por simplicidad y documentación automática
- **Frontend**: React (JavaScript) — elegido por popularidad y ecosistema
- **Comunicación**: HTTP/JSON — el estándar de la industria
- **Almacenamiento**: En memoria — para foco en conceptos, no en infraestructura

### 6.3 Implementación

- Backend: `main.py` con ~120 líneas, incluyendo modelos, endpoints y servidor
- Frontend: `App.jsx` + `api.js` + `App.css`, ~250 líneas totales
- Configuración: `pyproject.toml` (uv), `package.json` (pnpm), `vite.config.js`

### 6.4 Testing

- **Unitario**: Validación de modelos Pydantic (automático con FastAPI)
- **API**: 10 casos de prueba con Postman/Bruno/curl
- **Frontend**: 9 casos de prueba manuales
- **Integración**: 3 escenarios end-to-end

### 6.5 Deployment (Futuro)

Para llevar esto a producción se necesitaría:

1. **Base de datos**: Reemplazar lista en memoria por PostgreSQL
2. **Persistencia**: SQLModel o SQLAlchemy para ORM
3. **Auth**: JWT para autenticación de usuarios
4. **Docker**: Containerizar backend y frontend
5. **CI/CD**: GitHub Actions para build y deploy automático
6. **Hosting**: Railway, Render, o VPS con nginx

### 6.6 Mantenimiento (Futuro)

- Agregar filtros y búsqueda de tareas
- Categorías y etiquetas
- Due dates y recordatorios
- Collaboración multi-usuario
- Notificaciones push

---

## 7. Decisiones de Diseño

### ¿Por qué FastAPI y no Express/Django/Flask?

| Framework | Ventaja | Desventaja |
|-----------|---------|------------|
| **FastAPI** | Documentación automática, validación con Pydantic, async nativo | Más nuevo, menos Stack Overflow |
| Express | Ecosistema masivo, mucha documentación | Sin validación automática, boilerplate |
| Django | ORM completo, admin panel | Pesado para una API simple, opinionado |
| Flask | Simple, flexible | Sin async, sin validación automática |

**Decisión**: FastAPI因其 documentación automática (Swagger) y validación de datos, ideal para un taller donde queremos que los estudiantes vean resultados inmediatos.

### ¿Por qué React y no Vue/Angular/Svelte?

| Framework | Ventaja | Desventaja |
|-----------|---------|------------|
| **React** | Ecosistema más grande, más trabajo, Hooks intuitivos | JSX confunde al principio |
| Vue | Curva de aprendizaje menor | Menos trabajo que React |
| Angular | Todo incluido, TypeScript nativo | Muy pesado para un taller |
| SVG/Svelte | Performance, código mínimo | Ecosistema más chico |

**Decisión**: React因其 ecosistema y demanda laboral. Para 90 minutos, un solo componente con useState/useEffect es suficiente.

### ¿Por qué uv y no pip/conda?

**Decisión**: uv es ~100x más rápido que pip, simplifica el setup (un solo comando `uv run`), y es el estándar emergente en Python.

### ¿Por qué pnpm y no npm/yarn?

**Decisión**: En la UTN, npm está bloqueado por el firewall. pnpm es más rápido que npm y yarn, y usa menos disco.

---

## 8. Glossario Técnico

| Término | Definición |
|---------|-----------|
| **ASGI** | Async Server Gateway Interface — protocolo para servidores Python asíncronos |
| **CORS** | Cross-Origin Resource Sharing — política de seguridad del navegador |
| **CRUD** | Create, Read, Update, Delete — operaciones básicas de datos |
| **Fetch API** | Interfaz nativa del navegador para hacer peticiones HTTP |
| **Hot-reload** | Reinicio automático del servidor al guardar cambios |
| **HTTP** | Hypertext Transfer Protocol — protocolo de comunicación web |
| **JSON** | JavaScript Object Notation — formato de datos ligero |
| **JSX** | JavaScript XML — extensión de JavaScript para React |
| **Middleware** | Componente que se ejecuta entre la petición y la respuesta |
| **PATCH** | Método HTTP para actualización parcial de un recurso |
| **POST** | Método HTTP para crear un recurso nuevo |
| **Pydantic** | Librería de validación y serialización de datos para Python |
| **REST** | Representational State Transfer — estilo arquitectónico de APIs |
| **SPA** | Single Page Application — aplicación de una sola página |
| **Swagger** | Herramienta de documentación interactiva de APIs |
| **TypeScript** | JavaScript con tipos estáticos |
| **uv** | Gestor de paquetes Python ultrarrápido |
| **Vite** | Build tool y dev server para前端 moderno |

---

## 9. Referencias

- [RFC 7231 — HTTP/1.1 Semantics and Content](https://tools.ietf.org/html/rfc7231)
- [OpenAPI Specification 3.1](https://spec.openapis.org/oas/latest.html)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Documentation](https://react.dev/)
- [Vite Documentation](https://vite.dev/)
- [uv Documentation](https://docs.astral.sh/uv/)
- [pnpm Documentation](https://pnpm.io/)
