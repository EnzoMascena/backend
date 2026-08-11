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
    padding: 36px 56px;
    background-color: #0f172a;
    color: #e2e8f0;
  }
  h1 { color: #f8fafc; font-size: 1.55em; }
  h2 { color: #f1f5f9; font-size: 1.25em; }
  h3 { color: #94a3b8; font-size: 1em; }
  h4 { color: #93c5fd; }
  strong { color: #f1f5f9; }
  em { color: #cbd5e1; }
  a { color: #93c5fd; }

  /* ---- Slides densas: reducimos todo un escalón ---- */
  section.smaller { font-size: 0.88em; }
  section.smaller h1 { font-size: 1.4em; }
  section.smaller h2 { font-size: 1.15em; }

  /* ---- Código ---- */
  code {
    color: #93c5fd;
    background: #1e293b;
    padding: 2px 6px;
    border-radius: 4px;
    font-size: 0.85em;
  }
  pre {
    background: #1e293b;
    border: 1px solid #334155;
    border-radius: 8px;
    padding: 10px 16px;
    font-size: 0.7em;
    line-height: 1.45;
    color: #e2e8f0;
  }
  pre code {
    background: none;
    padding: 0;
    color: #e2e8f0;
  }

  /* ---- Resaltado sintáctico (paleta clara sobre fondo oscuro) ----
     Marp usa prettylights (tema claro) que pinta tokens en colores
     OSCUROS sobre el fondo oscuro -> ilegible. Forzamos paleta clara. */
  pre code :is(.hljs-keyword, .hljs-doctag, .hljs-template-tag, .hljs-template-variable, .hljs-variable.language_, .hljs-selector-tag) { color: #f472b6 !important; }
  pre code :is(.hljs-string, .hljs-regexp, .hljs-meta .hljs-string) { color: #86efac !important; }
  pre code :is(.hljs-title, .hljs-title.function_, .hljs-title.class_, .hljs-name, .hljs-quote, .hljs-selector-pseudo) { color: #7dd3fc !important; }
  pre code :is(.hljs-attr, .hljs-attribute, .hljs-literal, .hljs-meta, .hljs-selector-attr, .hljs-selector-class, .hljs-selector-id, .hljs-variable) { color: #93c5fd !important; }
  pre code :is(.hljs-number, .hljs-symbol) { color: #fcd34d !important; }
  pre code :is(.hljs-operator, .hljs-params, .hljs-subst, .hljs-type) { color: #cbd5e1 !important; }
  pre code :is(.hljs-comment, .hljs-code, .hljs-formula) { color: #94a3b8 !important; font-style: italic; }
  pre code :is(.hljs-section, .hljs-bullet) { color: #f0abfc !important; font-weight: 700; }
  pre code .hljs-built_in { color: #fca5a5 !important; }

  /* ---- Tablas ---- */
  table {
    font-size: 0.72em;
    background: #1e293b;
    border-radius: 8px;
    overflow: hidden;
    border-collapse: collapse;
    width: 100%;
  }
  thead { background: #334155; }
  th {
    color: #93c5fd;
    padding: 6px 12px;
    text-align: left;
    border-bottom: 2px solid #3b82f6;
    background: #334155;
  }
  td {
    color: #cbd5e1;
    padding: 6px 12px;
    border-bottom: 1px solid #334155;
    background: #1e293b;
  }
  tr:hover td { background: #263348; }

  /* ---- Blockquote ---- */
  blockquote {
    border-left: 4px solid #3b82f6;
    background: #1e293b;
    padding: 8px 14px;
    border-radius: 0 8px 8px 0;
    margin: 8px 0;
  }
  blockquote p {
    color: #94a3b8;
    font-style: italic;
  }

  /* ---- Listas ---- */
  ul { list-style-type: none; padding-left: 0; }
  ul li::before { content: "▸ "; color: #93c5fd; font-weight: bold; }
  ul li { color: #cbd5e1; line-height: 1.5; }
  ol li { color: #cbd5e1; line-height: 1.5; }

  /* ---- Lead slides ---- */
  section.lead h1 { font-size: 2.2em; }
  section.lead p { color: #94a3b8; }

  /* ---- Checkpoint ---- */
  section.checkpoint {
    background-color: #052e16;
  }
  section.checkpoint h1 {
    color: #34d399;
    font-size: 1.7em;
  }
  section.checkpoint p, section.checkpoint li {
    color: #a7f3d0;
  }

  /* ---- Footer ---- */
  footer { color: #64748b; font-size: 0.6em; }
---

<!-- _class: lead -->
<!-- note: |
  Bienvenidos a la clase 02. Hoy la MISMA app de la clase 01, pero con
  una diferencia que lo cambia todo: los datos van a sobrevivir.
  Material de trabajo: GUIA_ALUMNO.md abierta en el navegador.
  Decir: "abrí la guía y dejála abierta — la presentación muestra el
  QUÉ y el POR QUÉ, la guía tiene el CÓMO".
  Timing: 0-5 min
-->

# Persistencia con PostgreSQL

### Clase 02 — Desarrollo de Software 2026

La misma API de Tareas... pero los datos ya no se pierden

---

<!-- note: |
  Demo: creá 2-3 tareas en el backend del módulo 01 (o mostrá el GET),
  matá el servidor con Ctrl+C, volvé a levantarlo y listá.
  La lista está VACÍA. Eso es el problema que resolvemos hoy.
  Timing: 5-10 min
-->

## El problema: los datos mueren al reiniciar

**Módulo 01** → `tasks: list[dict]` vive en la memoria del proceso

```
uv run main.py     →  tareas: ["Aprender HTTP", "Hacer React"]
Ctrl+C             →  💀 el proceso muere
uv run main.py     →  tareas: []  ← TODO PERDIDO
```

> Los datos que no sobreviven al reinicio **no son datos de verdad**.
> Son una demo. Hoy los hacemos reales.

---

<!-- note: |
  Demo de Docker en el proyector. Explicar los 4 conceptos con la
  analogía del módulo prefabricado. No entrar en compose, ni volúmenes,
  ni redes — solo lo mínimo para tener postgres corriendo.
  Timing: 10-25 min
-->

<!-- _class: smaller -->

## Mini intro a Docker — ¿cómo conseguimos postgres?

**Imagen** = el molde. Postgres ya instalado y configurado.
**Contenedor** = una instancia corriendo de ese molde.

```bash
docker run -d --name pg-clase02 \
  -e POSTGRES_PASSWORD=postgres \
  -p 5432:5432 \
  postgres:16-alpine

docker ps                       # ver contenedores corriendo
docker exec -it pg-clase02 psql -U postgres   # entrar a psql
```

| Concepto | Analogía |
|----------|----------|
| Imagen | Módulo prefabricado: viene con TODO adentro |
| Contenedor | El módulo enchufado y funcionando |
| `-p 5432:5432` | La puerta de entrada (puerto local → puerto del contenedor) |

> Los alumnos no instalan nada: van directo a **Supabase** (mismo postgres, cero instalación)

---

<!-- note: |
  Aclarar que los alumnos en este momento están creando su proyecto
  Supabase en paralelo. Mientras el docente hace la demo con Docker,
  los alumnos copian su connection string del dashboard.
  El mensaje clave: el código NO sabe ni le importa dónde corre postgres.
  Timing: 25-35 min
-->

## Alumnos: Supabase free tier (2 minutos)

1. Crear cuenta en **supabase.com** (plan Free, sin tarjeta)
2. Crear proyecto → **Settings → Database → Connection string**
3. Copiar la URL del **pooler** (puerto 6543)

```
postgresql://postgres.TU_REF:TU_PASSWORD@aws-0-REGION.pooler.supabase.com:6543/postgres
```

> 🧨 **Gotcha profesional**: el free tier pausa el proyecto tras 7 días de inactividad. Los datos **no se pierden** — se reactiva con un click. Esa es la diferencia entre un free tier y producción.

---

<!-- note: |
  Slide de SQL. Mostrar la tabla como una planilla. Escribir los 4
  comandos básicos EN VIVO en psql (docente) y/o SQL Editor (alumnos).
  No profundizar: es la primera vez que ven SQL. El foco es que
  entiendan que postgres es un PROGRAMA que guarda FILAS.
  Timing: 35-45 min
-->

<!-- _class: smaller -->

## SQL en 10 minutos — la tabla es una planilla

```sql
CREATE TABLE IF NOT EXISTS tasks (
    id          INTEGER     GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    title       TEXT        NOT NULL,
    completed   BOOLEAN     NOT NULL DEFAULT FALSE,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
```

| Comando | Qué hace | En nuestras palabras |
|---------|----------|----------------------|
| `CREATE TABLE` | Define el molde | "La estructura de la planilla" |
| `INSERT` | Agrega una fila | "Una tarea nueva" |
| `SELECT` | Lee filas | "Listar las tareas" |
| `UPDATE` | Modifica filas | "Marcar como hecha" |
| `DELETE` | Borra filas | "Eliminar la tarea" |

> `DEFAULT NOW()` → **la base** genera `created_at`, no el código Python.
> `IDENTITY` → **la base** genera el `id`, no Python. La base manda.

---

<!-- note: |
  Explicar la anatomy de la URL pieza por pieza. Esto es el concepto
  central de la clase: una conexión es una URL. Después el pool:
  analogía del estacionamiento con guardia.
  Timing: 45-55 min
-->

## La conexión — una URL lo dice todo

```
postgresql://  USUARIO  :  CONTRASEÑA  @  HOST  :  PUERTO  /  BDD
^protocolo    ^usuario     ^clave        ^dónde      ^puerta  ^nombre
```

```python
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/postgres")

pool = ConnectionPool(conninfo=DATABASE_URL, min_size=1, max_size=10, open=False)
```

**¿Por qué un pool?** Abrir una conexión cuesta (handshake TCP + auth + SSL).
El pool mantiene conexiones abiertas y las **reutiliza**:
un estacionamiento con guardia — el auto no fabrica su lugar, el guardia le asigna uno.

---

<!-- note: |
  Antes de la demo de código, un momento de claridad sobre el `with`.
  Decir: "este patrón se repite en los 4 endpoints — aprendelo UNA vez
  y se aplica siempre". Mostrar dónde vive el pool en el código.
  Timing: 55-60 min
-->

<!-- _class: smaller -->

## Migrar la API — el patrón que se repite

```python
with pool.connection() as conn:
    conn.row_factory = dict_row          # fila → {"columna": valor}
    with conn.cursor() as cur:
        cur.execute("... SQL ...", (params,))
        row = cur.fetchone()
```

| Pieza | Para qué |
|-------|----------|
| `with pool.connection()` | Pedir conexión prestada → **commit automático** al salir |
| `dict_row` | Leer columnas por nombre: `row["title"]` |
| `%s` | **Placeholder** — nunca concatenar strings en SQL (inyección) |
| `RETURNING` | Postgres devuelve la fila afectada → sin segunda consulta |

---

<!-- note: |
  Mostrar el código REAL de un endpoint (POST) y su versión módulo 01
  al lado. La diferencia: la lista se reemplaza por SQL.
  Timing: 60-70 min
-->

<!-- _class: smaller -->

## El mismo endpoint, otro motor

**Módulo 01** — Python hacía todo:

```python
task = {"id": next_id, "title": body.title.strip(),
        "completed": False, "created_at": datetime.now(timezone.utc).isoformat()}
tasks.append(task)
```

**Módulo 02** — la base hace todo:

```python
cur.execute("INSERT INTO tasks (title) VALUES (%s) "
            "RETURNING id, title, completed, created_at", (body.title.strip(),))
row = cur.fetchone()
```

> El **toggle** también es SQL ahora: `UPDATE tasks SET completed = NOT completed WHERE id = %s`
> Y el "no existe" es `WHERE id = %s` devolviendo 0 filas → **404**

---

<!-- _class: checkpoint -->
<!-- note: |
  Checkpoint 1: cada alumno debe tener el server arriba y el health
  devolviendo db: "conectada". Recorrer el aula y desbloquear.
  Los síntomas clásicos: URL mal copiada, puerto del pooler, password.
  Timing: 70-75 min
-->

## ✅ Checkpoint 1 — BBDD conectada

```bash
curl http://localhost:8000/api/health
```

```json
{ "status": "Funciona", "service": "02-...", "db": "conectada", "tasks_count": 0 }
```

- Server arriba, pool abierto, postgres responde
- Swagger en `http://localhost:8000/docs`
- Si falla → el problema es la `DATABASE_URL`

---

<!-- note: |
  El momento estrella. Antes de mostrar el código: "¿qué pasa si
  reinicio?" — la clase responde "se pierden" — "hoy no".
  Crear tareas, matar server, levantar, listar, MOSTRAR que están.
  Después: levantar el frontend del módulo 01 SIN TOCARLO.
  "El frontend no sabe que cambiamos el motor. Eso es un contrato."
  Timing: 75-85 min
-->

<!-- _class: smaller -->

## El momento de la clase

**1. Crear tareas** → **2. Matar el servidor** → **3. Levantarlo** → **4. Listar**

```bash
curl -X POST http://localhost:8000/api/tasks -H "Content-Type: application/json" \
  -d '{"title": "Aprender SQL"}'
# Ctrl+C → uv run main.py → curl http://localhost:8000/api/tasks
```

**La tarea sigue ahí.** Eso es persistencia.

**Y ahora la frutilla:** el frontend de la clase 01, **sin tocar una línea**:

```bash
cd ../01-mi-primera-app/frontend && pnpm dev
```

Las tareas aparecen... y sobreviven al reinicio del backend.

> El frontend no sabe ni le importa si debajo hay una lista o PostgreSQL.
> **La API es un contrato** entre dos sistemas.

---

<!-- _class: checkpoint -->
<!-- note: |
  Checkpoint 2: persistencia demostrada + Postman con la collection del
  módulo 02 (request "7. PERSISTENCIA"). Recorrer el aula.
  Timing: 85-90 min
-->

## ✅ Checkpoint 2 — Persistencia demostrada

- [ ] Reinicié el servidor y las tareas siguen
- [ ] El frontend del Módulo 01 funciona contra el backend nuevo
- [ ] Postman: collection `02-persistencia-postgresql` → flujo feliz + persistencia
- [ ] Casos límite: 422 y 404 idénticos al Módulo 01

---

<!-- note: |
  Recapitular con la tabla resumen. Dejar los ejercicios como tarea.
  Cerrar con la idea: hoy aprendieron a NO perder datos. El próximo
  módulo: TypeScript en el frontend.
  Timing: 90 min
-->

<!-- _class: smaller -->

## Resumen

| | Módulo 01 | Módulo 02 |
|---|---|---|
| Dónde viven los datos | Lista en memoria | **PostgreSQL** |
| ¿Sobreviven al reinicio? | ❌ | ✅ |
| ¿Quién genera `id` y `created_at`? | Python | **La base** |
| ¿Quién valida? | Pydantic | Pydantic (la base valida en el próximo nivel) |
| Frontend | React JS | **El mismo, sin cambios** |

### Ejercicios 🟢 🟡 🔴 → en `GUIA_ALUMNO.md`

- 🟢 Explicá `SELECT 1` del health check
- 🟡 Agregá `priority` end-to-end (schema → modelo → endpoint)
- 🔴 **Inyección SQL**: probá `"); DROP TABLE tasks; --` y explicá por qué `%s` te protege

---

<!-- _class: lead -->
<!-- note: |
  Cierre. Agradecer, recordar commitear el código de la clase
  (backend/) y que la GUIA_ALUMNO queda para la próxima.
  Timing: 90 min
-->

# Hoy los datos se volvieron reales

### Clase 03 (próxima): React con TypeScript

> *"La Universidad te da el mapa. El recorrido lo hacés vos."*
