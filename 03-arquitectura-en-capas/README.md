# 🚀 Módulo 03 — Arquitectura en Capas + ORM + TypeScript

> **Empezá acá.** Este documento te dice qué es este módulo, cómo arrancar y
> dónde está cada cosa. Después seguí con `GUIA_ALUMNO.md`.

---

## ¿De qué se trata?

En el Módulo 02 escribiste la API de tareas con **SQL crudo** dentro de un
`main.py` monolítico. Hoy vas a **reorganizarla**:

- **3 capas** → Controller (HTTP) → Service (negocio) → Repository (ORM)
- **ORM (SQLModel)** → en lugar de escribir SQL a mano
- **Frontend TypeScript** → el contrato de la API, como tipos

Vas a **descubrir y desarrollar** el taller en tu propio **fork**, sin que te
den la solución servida.

---

## Cómo empezar (fork → clonar → desarrollar)

### 1. Hacé un fork del repositorio

En GitHub, andá al repo de la materia y clickeá **Fork**. Esto te crea una
**copia propia** del repo, donde vas a trabajar sin miedo a romper nada.

### 2. Cloná TU fork

```bash
git clone https://github.com/TU_USUARIO/backend.git
cd backend/03-arquitectura-en-capas
```

### 3. Leé el material previo (si no lo hiciste)

Abrí [`MATERIAL_PREVIO.md`](./MATERIAL_PREVIO.md). Ahí están los conceptos
(capas, ORM, SQLModel, TypeScript) + la **bibliografía y videos** de cada tema.
Sin esto, el taller va a ser cuesta arriba.

### 4. Entendé qué vas a construir

Leé [`SPEC.md`](./SPEC.md) — es tu **recurso de aprendizaje**: qué construís,
por qué, y qué vas a descubrir en el camino.

### 5. Desarrollá el backend (las 3 capas)

Seguí [`GUIA_ALUMNO.md`](./GUIA_ALUMNO.md). Completás **3 archivos**:

| Archivo | Capa |
|---------|------|
| `backend/app/repositories/task_repository.py` | Repository (ORM) |
| `backend/app/services/task_service.py` | Service (negocio) |
| `backend/app/controllers/task_controller.py` | Controller (HTTP) |

### 6. Conectá el frontend TypeScript

El frontend ya viene **completo** (`frontend/`). Solo lo levantás y verificás
que haga el CRUD contra tu backend.

### 7. Verificá con Postman

Importá la collection de `postman/` y corré el flujo feliz + casos límite.

---

## Qué está completo y qué tenés que completar

| Componente | Estado |
|-----------|--------|
| `backend/app/models/task.py` | ✅ Dado (el modelo SQLModel) |
| `backend/app/database.py` | ✅ Dado (engine + session) |
| `backend/app/dependencies.py` | ✅ Dado (el cableado) |
| `backend/app/main.py` | ✅ Dado (el entrypoint) |
| `backend/app/controllers/health_controller.py` | ✅ Dado (**ejemplo vivo** de controller) |
| `backend/app/repositories/task_repository.py` | 🔓 **Completás vos** |
| `backend/app/services/task_service.py` | 🔓 **Completás vos** |
| `backend/app/controllers/task_controller.py` | 🔓 **Completás vos** |
| `frontend/` | ✅ Dado (completo, se explora) |

---

## Estructura del repo

```
03-arquitectura-en-capas/
├── README.md            # este archivo — empezá acá
├── SPEC.md              # recurso de aprendizaje (qué + por qué)
├── MATERIAL_PREVIO.md   # lectura pre-clase + referencias por tema
├── GUIA_ALUMNO.md       # guía de descubrimiento paso a paso
├── PRESENTACION.md/html/pdf  # (material del docente)
├── backend/
│   ├── app/             # las 3 capas (3 archivos para completar)
│   ├── pyproject.toml   # dependencias (uv)
│   └── .env.example     # plantilla de configuración
├── frontend/            # React + Vite + TypeScript (dado)
└── postman/             # collection con tests
```

---

## Levantar el backend

```bash
cd backend
cp .env.example .env        # completá DATABASE_URL (reusás la del módulo 02)
uv sync                     # instala dependencias
uv run -m app.main          # http://localhost:8000
```

> La tabla `tasks` se crea sola al arrancar (`create_all`). Si reutilizás la
> base del módulo 02, la tabla ya existe y el ORM la mapea tal cual.

## Levantar el frontend

```bash
cd frontend
pnpm install
pnpm dev                    # http://localhost:5173 (proxy → :8000)
```

---

## Regla de oro del taller

> **No busques la solución. Descubrila.** Cuando te trabes, preguntate:
> *"¿esto es HTTP, es negocio, o es datos?"*. Esa pregunta destraba el 90% de
> las dudas.

*"La Universidad te da el mapa. El recorrido lo hacés vos."*
