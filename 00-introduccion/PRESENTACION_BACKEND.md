---
marp: true
theme: default
size: 16:9
paginate: true
---

<!-- 
  PRESENTACIÓN: Backend — Conceptos Fundamentales
  Formato: Marp (Markdown Presentation Ecosystem)
  Progresión: 15 diapositivas, 16:9
-->

<!--
note: 👋 PRESENTACIÓN DEL DOCENTE Y CONTEXTO

Esta clase cubre la base conceptual del módulo Backend. Arrancamos desde cero: qué es backend, qué es una API REST, qué es un contrato, y cómo lo materializamos con OpenAPI/Swagger. Cerramos con una introducción a los dos frameworks que vamos a usar: FastAPI (Python) y Fastify (TypeScript).

🗣️ PARA DECIR:
- "Hoy vamos a entender QUÉ es backend y CÓMO se comunica con el frontend"
- "No importa si nunca tocaron una API — arrancamos de cero"
- "Al final de esta clase van a entender qué significa que una API tenga 'documentación' y por qué es parte del código, no un PDF aparte"

⚠️ TIEMPO ESTIMADO: 2-3 min
-->

<style>
/* ──────────── TIPOGRAFÍA ──────────── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800&family=Fira+Code:wght@400;600&display=swap');

:root {
  --verde: #59ec90;
  --verde-oscuro: #1a8f4e;
  --verde-bg: #59ec9018;
  --texto: #1a1a2e;
  --texto-secundario: #444;
  --borde: #ddd;
}

section {
  font-family: 'Inter', sans-serif;
  background: #ffffff;
  color: var(--texto);
  padding: 25px 45px;
}

/* ──────────── TÍTULOS ──────────── */
h1 {
  color: var(--texto);
  font-weight: 800;
  font-size: 2em;
  letter-spacing: -0.02em;
  margin-bottom: 0.1em;
}
h2 {
  color: var(--verde-oscuro);
  font-weight: 700;
  font-size: 1.35em;
  letter-spacing: -0.01em;
  border-bottom: 3px solid #59ec9060;
  padding-bottom: 0.15em;
  margin-bottom: 0.3em;
}
h3 {
  color: var(--verde-oscuro);
  font-weight: 600;
  font-size: 1em;
  margin: 0.2em 0;
}

/* ──────────── TEXTO ──────────── */
p, li {
  font-size: 0.85em;
  line-height: 1.4;
  color: var(--texto-secundario);
  margin: 0.2em 0;
}
strong {
  color: var(--texto);
  font-weight: 700;
}
code {
  font-family: 'Fira Code', monospace;
  background: #f0f0f0;
  color: #c7254e;
  padding: 0.1em 0.3em;
  border-radius: 4px;
  font-size: 0.7em;
}
pre {
  background: #f7f7f7 !important;
  border: 1px solid var(--borde);
  border-radius: 6px;
  padding: 8px 10px;
  margin: 0.3em 0;
}
pre code {
  background: transparent;
  padding: 0;
  font-size: 0.65em;
  color: #333;
  line-height: 1.3;
}

/* ──────────── TABLAS ──────────── */
table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.75em;
}
th {
  background: var(--verde-bg);
  color: var(--verde-oscuro);
  font-weight: 600;
  padding: 5px 8px;
  border: 1px solid var(--borde);
  text-align: left;
}
td {
  padding: 5px 8px;
  border: 1px solid var(--borde);
  color: var(--texto-secundario);
}
tr:nth-child(even) {
  background: #fafafa;
}

/* ──────────── DESTACADOS ──────────── */
blockquote {
  border-left: 3px solid var(--verde);
  background: var(--verde-bg);
  padding: 6px 14px;
  margin: 0.3em 0;
  border-radius: 0 6px 6px 0;
}
blockquote p {
  color: var(--texto-secundario);
  font-style: italic;
  font-size: 0.82em;
}

/* ──────────── UTILITIES ──────────── */
.columns {
  display: flex;
  gap: 18px;
}
.columns > * {
  flex: 1;
}
.big {
  font-size: 1.15em;
  font-weight: 600;
}
.tag {
  display: inline-block;
  background: var(--verde-bg);
  color: var(--verde-oscuro);
  padding: 1px 8px;
  border-radius: 20px;
  font-size: 0.6em;
  font-weight: 600;
  white-space: nowrap;
}
.tag-code {
  background: #f0f0f0;
  color: #c7254e;
}
.emoji-big {
  font-size: 1.8em;
  display: block;
  text-align: center;
  margin-bottom: 5px;
}
</style>

<!-- ================================================================ -->
<!-- SLIDE 1 — PORTADA -->
<!-- ================================================================ -->

# Backend — Conceptos Fundamentales

## API REST · Contrato · OpenAPI · FastAPI · Fastify

<br>

**Desarrollo de Software** — 4° año Ing. de Software  
UTN Facultad Regional La Plata

<!-- _footer: "Prof. Emanuel Rodriguez · 2026" -->

---

<!-- ================================================================ -->
<!-- SLIDE 2 — ¿QUÉ ES BACKEND? -->
<!-- ================================================================ -->

<!--
note: 🧠 CONCEPTO FUNDAMENTAL

Acá plantamos la primera definición sólida de backend. Muchos alumnos vienen de ver solo frontend y piensan que backend es "lo que no se ve". Hay que darles la visión sistémica.

🗣️ PARA DECIR:
- "Backend NO es solo 'la base de datos' — es toda la lógica del servidor"
- "El frontend pide, el backend procesa y responde — esa es la división de responsabilidades"

❓ PREGUNTAR:
- "¿Alguien me da un ejemplo de algo que haga un backend sin que el usuario lo vea?" (buscar: validación de datos, autorización, cálculos, etc.)
- "¿Qué pasa si el backend está caído pero el frontend sigue funcionando?" (nada, la app no sirve)

🔗 RELACIONAR con frontend: mostrar que no son capas aisladas, se comunican via API.
-->

# ¿Qué es Backend?

<br>

<div class="columns">
<div>

<div class="emoji-big">⚙️</div>

### Lógica del servidor

Procesa peticiones, ejecuta reglas de negocio, accede a datos. El usuario **no ve** esta capa.

</div>
<div>

<div class="emoji-big">🔗</div>

### API como interfaz

Expone funcionalidad a través de una **API** (Application Programming Interface). El frontend consume la API, no el backend directamente.

</div>
<div>

<div class="emoji-big">🗄️</div>

### Persistencia + Seguridad

Maneja bases de datos, autenticación, autorización, sesiones, archivos, logs.

</div>
</div>

<br>

> **Analogía**: Si una app web fuera un restaurante...
> - **Frontend** = el menú y el mozo (lo que el cliente ve e interactúa)
> - **Backend** = la cocina (donde procesan los ingredientes y preparan el plato)

---

<!-- ================================================================ -->
<!-- SLIDE 3 — API REST -->
<!-- ================================================================ -->

<!--
note: 🌐 REST — EL ESTÁNDAR DE LAS APIs MODERNAS

REST no es un protocolo ni una tecnología — es un ESTILO ARQUITECTÓNICO. Muchos alumnos confunden REST con CRUD. Aclaremos eso temprano.

🗣️ PARA DECIR:
- "REST no es 'hacer GET/POST/PUT/DELETE' — eso es CRUD. REST es un conjunto de RESTRICCIONES de diseño"
- "La más importante: STATELESS. Cada pedido contiene TODO lo que el servidor necesita para procesarlo"
- "Si guardás sesión en el servidor, NO es REST"

❓ PREGUNTAR:
- "¿Alguien usó alguna vez una API REST?" (seguro que sí, aunque no supieran que era REST)
- "¿Qué diferencia hay entre PUT y PATCH?" (PUT reemplaza TODO, PATCH actualiza parcial)

⚠️ OJO: no profundizar demasiado en REST acá. Alcanza con que entiendan:
  1. Recursos se identifican con URLs
  2. Operaciones se mapean a verbos HTTP
  3. Cada request es independiente (stateless)

🔗 RELACIONAR con: verbos HTTP en el próximo slide.
-->

# API REST

<div class="columns">
<div>

### ¿Qué es REST?

**RE**presentational **S**tate **T**ransfer — estilo de arquitectura para diseñar APIs web. Cada recurso tiene una **URL**, y se opera con **verbos HTTP**.

```
GET    /usuarios        → listar
POST   /usuarios        → crear
GET    /usuarios/:id    → obtener uno
PUT    /usuarios/:id    → reemplazar
PATCH  /usuarios/:id    → actualizar parcial
DELETE /usuarios/:id    → eliminar
```

</div>
<div>

### Principios REST

| Principio | ¿Qué significa? |
|-----------|----------------|
| **Stateless** | Cada request tiene toda la info. No hay sesión en el server |
| **Recursos** | Todo es un recurso identificado por URL |
| **Verbose HTTP** | GET, POST, PUT, PATCH, DELETE tienen semántica definida |
| **Respuesta estándar** | Códigos de estado HTTP + body JSON |

</div>
</div>

> 📌 **REST ≠ CRUD**. REST es un estilo arquitectónico. CRUD es un patrón de operaciones. Una API REST bien diseñada va más allá del CRUD.

---

<!-- ================================================================ -->
<!-- SLIDE 4 — VERBOS HTTP + CÓDIGOS DE ESTADO -->
<!-- ================================================================ -->

<!--
note: 📡 VERBOS + ESTADOS — EL IDIOMA DE HTTP

Esta slide es más de referencia. No esperamos que se aprendan todos los códigos de memoria, pero sí que entiendan las FAMILIAS (2xx, 4xx, 5xx).

🗣️ PARA DECIR:
- "Los verbos HTTP son como los VERBOS en un idioma: tienen significado y reglas"
- "GET y HEAD son SEGUROS — no modifican nada. Podés llamarlos mil veces y no pasa nada"
- "PUT y DELETE son IDEMPOTENTES — la 10° vez produce el mismo resultado que la 1°"
- "Los 4xx son ERRORES DEL CLIENTE — mandaste algo mal"
- "Los 5xx son ERRORES DEL SERVIDOR — se rompió algo del lado nuestro (no del usuario)"

❓ PREGUNTAR:
- "POST no es seguro ni idempotente — ¿por qué?" (crea recursos nuevos cada vez, no podés repetirlo sin consecuencias)
- "Si hago DELETE dos veces, ¿qué pasa?" (la primera borra, la segunda devuelve 404 — mismo resultado práctico, idempotente)

⚠️ PUNTO CLAVE: el código de estado NO es opcional. Siempre hay que devolver el código correcto. No todo es 200 OK.

🔗 RELACIONAR con: la práctica de curl que van a hacer después.
-->

# Verbos HTTP y Códigos de Estado

<div class="columns">
<div>

### Verbos

| Verbo | Acción | ¿Idempotente? | ¿Seguro? |
|-------|--------|:---:|:---:|
| `GET` | Obtener recurso | ✅ | ✅ |
| `POST` | Crear recurso | ❌ | ❌ |
| `PUT` | Reemplazar recurso | ✅ | ❌ |
| `PATCH` | Actualizar parcial | ❌ | ❌ |
| `DELETE` | Eliminar recurso | ✅ | ❌ |

> **Idempotente**: múltiples requests idénticos producen el mismo resultado.  
> **Seguro**: no modifica el estado del servidor.

</div>
<div>

### Códigos de Estado

| Rango | Significado | Ejemplos |
|-------|------------|----------|
| **1xx** | Informativo | 101 Switching Protocols |
| **2xx** | Éxito | 200 OK · 201 Created · 204 No Content |
| **3xx** | Redirección | 301 Moved · 304 Not Modified |
| **4xx** | Error del cliente | 400 Bad Request · 401 Unauthorized · 404 Not Found · 409 Conflict |
| **5xx** | Error del servidor | 500 Internal · 503 Service Unavailable |

</div>
</div>

---

<!-- ================================================================ -->
<!-- SLIDE 5 — CONTRATO DE API -->
<!-- ================================================================ -->

<!--
note: 📝 EL CONTRATO — LO QUE MANTIENE A TODOS EN LA MISMA PÁGINA

Este es uno de los conceptos más importantes de la clase y a la vez uno de los más difíciles de entender sin experiencia laboral. Los alumnos vienen de proyectos individuales o grupos chicos donde "el contrato" no existe porque el que hace el frontend es el mismo que hace el backend.

🗣️ PARA DECIR:
- "En un proyecto profesional, frontend y backend los hacen personas DISTINTAS, muchas veces en equipos diferentes"
- "El contrato es el ACUERDO: vos me mandás esto, yo te devuelvo aquello"
- "Sin contrato, el frontend espera un campo 'name' y el backend devuelve 'nombre' — y eso se rompe en producción"

❓ PREGUNTAR:
- "¿Alguna vez les pasó que una API devolvía algo distinto a lo que esperaban?" (seguro que sí)
- "¿Cómo resolverían eso sin un contrato formal?" (llamadas, mails, chats — todo frágil)

💡 MENSAJE CLAVE para que se lleven: el contrato NO es un papel que escriben al principio y se olvida. El contrato VIVE EN EL CÓDIGO y se genera automáticamente. Eso es lo que viene después con Swagger/OpenAPI.

🔗 RELACIONAR con: el slide de OpenAPI que sigue — el contrato se materializa con OpenAPI/Swagger.
-->

# Contrato de API

<div class="columns">
<div>

### ¿Qué es un contrato?

Un **acuerdo formal** entre el cliente (frontend, otra API, app mobile) y el servidor sobre **cómo se comunican**:

```
Cliente                              Servidor
  │                                      │
  │  ¿Qué URLs existen?                  │
  │  ¿Qué métodos aceptan?               │
  │  ¿Qué datos necesito enviar?          │
  │  ¿Qué forma tiene la respuesta?       │
  │  ¿Qué códigos de error puede dar?     │
  │                                      │
```

Sin contrato → **inconsistencias**, **bugs**, **equipos pisándose**.

</div>
<div>

### Sin contrato vs Con contrato

| Sin contrato 😱 | Con contrato ✅ |
|----------------|-----------------|
| "Che, ¿qué me devuelve este endpoint?" | Spec documentada |
| Frontend espera `{name}` y el backend devuelve `{nombre}` | Schemas compartidos |
| "Avisame cuando cambies algo" | Versionado semántico |
| Documentación desactualizada en un PDF | Documentación **autogenerada** |

</div>
</div>

> 💡 **El contrato NO es un documento PDF que escribís al inicio y se desactualiza. El contrato VIVE en el código y se genera automáticamente.**

---

<!-- ================================================================ -->
<!-- SLIDE 6 — OPENAPI / SWAGGER -->
<!-- ================================================================ -->

<!--
note: 📖 OPENAPI — EL ESTÁNDAR, NO LA HERRAMIENTA

Importante: OpenAPI es el ESTÁNDAR (antes Swagger Specification). Swagger es el ECOSISTEMA DE HERRAMIENTAS (Swagger UI, Swagger Editor, etc.).

🗣️ PARA DECIR:
- "OpenAPI es como el idioma español — es el estándar. Swagger UI es como un libro escrito en español — es una herramienta que usa el estándar"
- "Con OpenAPI podés describir tu API en un archivo JSON o YAML, y después cualquier herramienta (Swagger, Postman, Insomnia, generadores de código) puede leerlo"
- "Acá vemos el YAML de ejemplo. No necesitan aprenderlo de memoria — los frameworks lo generan solos"

❓ PREGUNTAR:
- "¿Por qué creen que es importante que OpenAPI sea un ESTÁNDAR y no algo de una sola empresa?" (interoperabilidad, no vendor lock-in)
- "Si cambian de Swagger UI a otra herramienta, ¿el archivo OpenAPI sirve igual?" (sí — por eso es un estándar)

🔗 RELACIONAR con: el próximo slide — Swagger UI en acción, y con la práctica donde van a ver el spec generado automáticamente.
-->

# OpenAPI / Swagger

<div class="columns">
<div>

### ¿Qué es OpenAPI?

Un **estándar abierto** para describir APIs REST usando JSON o YAML. Antes se llamaba Swagger Specification.

```yaml
openapi: 3.0.3
info:
  title: Mi API
  version: 1.0.0
paths:
  /usuarios:
    get:
      summary: Listar usuarios
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/Usuario'
```

</div>
<div>

### Herramientas del ecosistema

| Herramienta | ¿Para qué? |
|-------------|-----------|
| **Swagger UI** | Interfaz web interactiva para probar endpoints |
| **Swagger Editor** | Editor online con preview en vivo |
| **OpenAPI Generator** | Genera clients HTTP en 50+ lenguajes |
| **Swagger Codegen** | Genera server stubs |
| **Postman / Insomnia** | Importan specs OpenAPI |

___

**En este curso**: No escribimos OpenAPI a mano. **Fastify y FastAPI lo generan solos** a partir de schemas.

___

---

<!-- ================================================================ -->
<!-- SLIDE 7 — SWAGGER UI EN ACCIÓN -->
<!-- ================================================================ -->

<!--
note: 🖥️ SWAGGER UI — LA DOCUMENTACIÓN VIVA

Este slide es ideal para MOSTRAR EN VIVO si tienen la API corriendo. Abrí http://localhost:3000/docs y mostrá los endpoints, los schemas, y el botón "Try it out".

🗣️ PARA DECIR:
- "Esto NO es documentación escrita a mano. Cada ruta que definimos con su schema aparece automáticamente"
- "Probá el endpoint /health, hace click en Try it out, y después en Execute — te muestra la request y la response"
- "Esto es magia? No — es el schema que definiste en el código transformado en UI"

❓ PREGUNTAR:
- "¿Qué pasa si cambio el schema pero no actualizo la documentación?" (no hace falta — la doc se regenera sola al reiniciar)
- "¿Cuánto tiempo les llevaría escribir y mantener esta documentación a mano?" (mucho, y siempre se desactualiza)

💡 EJERCICIO PROPONE: que agreguen un campo al schema de /health y vean cómo se refleja automáticamente en Swagger UI.

🔗 RELACIONAR con: la práctica donde van a hacer esto en vivo.
-->

# Swagger UI en acción

<div class="columns">
<div>

### Lo que genera automáticamente

```
Schema de ruta
      │
      ▼
@fastify/swagger / fastapi.FastAPI
      │
      ▼
Spec OpenAPI 3.0 (JSON)
      │
      ▼
Swagger UI (interfaz interactiva)
```

</div>
<div>

### Beneficios concretos

<span class="tag">📋</span> **Documentación viva** — se genera del código  
<span class="tag">🖱️</span> **Try it out** — probá endpoints desde el navegador  
<span class="tag">🧩</span> **Interoperable** — cualquier herramienta consume OpenAPI  
<span class="tag">🔍</span> **Autodescubrible** — entendés toda la API en 5 min

</div>
</div>

> **Ejemplo**: `GET /health` con schema → Swagger genera:
> ```json
> "responses": { "200": { "content": {
>   "application/json": { "schema": {
>     "type": "object",
>     "properties": {
>       "status": { "type": "string" },
>       "service": { "type": "string" }
>     }
>   }}
> }}}
> ```

---

<!-- ================================================================ -->
<!-- SLIDE 8 — FASTAPI (PYTHON) -->
<!-- ================================================================ -->

<!--
note: 🐍 FASTAPI — MODERNO, RÁPIDO, PYTHÓNICO

FastAPI es uno de los frameworks que más creció en los últimos años. Creado por Sebastián Ramírez (colombiano) en 2018. Se destaca por usar type hints de Python para validación automática.

🗣️ PARA DECIR:
- "FastAPI aprovecha los TYPE HINTS de Python — si sabés Python moderno, ya sabés FastAPI en un 70%"
- "Usa Pydantic para validación — un modelo de datos con type hints valida, serializa y documenta automáticamente"
- "Es async nativo — podés usar async/await sin configuración extra"

❓ PREGUNTAR:
- "¿Alguien usó Flask o Django? FastAPI es más moderno que Flask y más liviano que Django"
- "¿Qué ventaja tiene que la validación sea automática vs tener que escribir if/else para cada campo?"

💡 DATO CURIOSO: FastAPI tiene 70k+ estrellas en GitHub. Es uno de los proyectos Python más populares.

🔗 RELACIONAR con: el slide de código que sigue, donde se ve el ejemplo completo.
-->

<div style="display: flex; align-items: center; gap: 10px; margin-bottom: 10px;">
  <span style="font-size: 2.5em;">🐍</span>
  <h1 style="margin: 0;">FastAPI</h1>
</div>

<div class="columns">
<div>

### ¿Qué es?

Framework web moderno para Python (3.8+) basado en **type hints** y **Pydantic**. Creado por Sebastián Ramírez en 2018.

```
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Mi API")

class Usuario(BaseModel):
    nombre: str
    edad: int

@app.post("/usuarios")
def crear_usuario(usuario: Usuario):
    return {"id": 1, **usuario.model_dump()}
```

</div>
<div>

### Stack tecnológico

```
FastAPI
  ├── Starlette (web)
  ├── Pydantic (validación/schemas)
  ├── Uvicorn (servidor ASGI)
  └── OpenAPI autogenerado
```

### Características clave

<span class="tag">✅</span> Validación automática con type hints  
<span class="tag">✅</span> Async nativo  
<span class="tag">✅</span> Documentación Swagger automática  
<span class="tag">✅</span> Tipado completo (editor autocompletado)  
<span class="tag">✅</span> Rendimiento excelente (a la par de Node.js/Go)

</div>
</div>

---

<!-- ================================================================ -->
<!-- SLIDE 9 — FASTAPI: CÓMO SE VE -->
<!-- ================================================================ -->

<!--
note: 💻 FASTAPI — ANÁLISIS DEL CÓDIGO

Acá se ve el ejemplo completo. Es importante que los alumnos NO solo copien el código, sino que entiendan qué hace cada línea.

🗣️ PARA DECIR (señalando líneas):
- "Usuario(BaseModel): este modelo ES el contrato. Con 3 líneas definimos los datos que esperamos"
- "FastAPI(title=...): la configuración mínima para que aparezca en Swagger"
- "usuario: Usuario en el POST — FastAPI infiere que debe leer el body y validarlo contra el modelo. NO necesitamos hacer nada más"
- "status_code=201: el código de estado correcto para creación"

❓ PREGUNTAR:
- "¿Qué pasa si alguien manda un POST a /usuarios con 'edad': 'veinte'?" (FastAPI lo rechaza automáticamente con 422 Unprocessable Entity)
- "¿Dónde está el código que valida? No hay — los type hints de Python y Pydantic lo hacen automágicamente"

💡 DEMO EN VIVO: si pueden, abran FastAPI en /docs y creen un usuario con datos inválidos para mostrar el 422.

🔗 RELACIONAR con: el mismo ejemplo en Fastify — la idea es la misma, cambia la sintaxis.
-->

# FastAPI — Código en acción

```python
from fastapi import FastAPI
from pydantic import BaseModel

class Usuario(BaseModel):
    nombre: str
    email: str
    edad: int

app = FastAPI(title="Usuarios API", version="0.1.0")

@app.get("/")
def raiz():
    return {"message": "Hola desde FastAPI"}

@app.get("/health")
def health():
    return {"status": "ok", "service": "fastapi-hello"}

@app.post("/usuarios", status_code=201)
def crear_usuario(usuario: Usuario):
    return {"id": 1, **usuario.model_dump()}
```

**Lo que pasa automáticamente sin escribir más código:**
<span class="tag">📄</span> Swagger UI en `/docs` &nbsp; <span class="tag">📋</span> ReDoc en `/redoc` &nbsp; <span class="tag">✅</span> Validación de tipos en runtime &nbsp; <span class="tag">🧠</span> Autocompletado en el editor

---

<!-- ================================================================ -->
<!-- SLIDE 10 — FASTIFY (TYPESCRIPT) -->
<!-- ================================================================ -->

<!--
note: ⚡ FASTIFY — RENDIMIENTO Y ESTRUCTURA

Fastify es la alternativa moderna a Express.js. Si vienen de Express, Fastify les va a parecer más opinado y estructurado — y eso es bueno.

🗣️ PARA DECIR:
- "Fastify es a Express como TypeScript es a JavaScript: más estructura, más seguridad, menos sorpresas"
- "El sistema de PLUGINS de Fastify es único — TODO es un plugin, y los plugins tienen scope encapsulado"
- "El router usa un RADIX TREE — eso le da rendimiento 2-3x superior a Express"
- "Viene con PINO como logger nativo — no hay que instalar Morgan ni Winston aparte"

❓ PREGUNTAR:
- "¿Alguien usó Express? Fastify es conceptualmente similar pero más estructurado"
- "¿Por qué creen que tener el logger nativo es mejor que instalarlo aparte?" (menos dependencias, configuración cero, logs consistentes)

💡 CURIOSIDAD TÉCNICA: el router find-my-way de Fastify está basado en el mismo principio que usan los routers de hardware de redes — árboles de prefijos (radix tree).

🔗 RELACIONAR: con el slide de código de Fastify que sigue.
-->

<div style="display: flex; align-items: center; gap: 10px; margin-bottom: 10px;">
  <span style="font-size: 2.5em;">⚡</span>
  <h1 style="margin: 0;">Fastify</h1>
</div>

<div class="columns">
<div>

### ¿Qué es?

Framework web para Node.js enfocado en **rendimiento** y **baja sobrecarga**. Creado por Matteo Collina y Tomas Della Vedova en 2017.

```typescript
import Fastify from "fastify";

const app = Fastify({ logger: true });

app.get("/usuarios/:id", async (request) => {
  const { id } = request.params;
  return { id, nombre: "Ejemplo" };
});

await app.listen({ port: 3000 });
```

</div>
<div>

### Stack tecnológico

```
Fastify
  ├── find-my-way (router radix tree)
  ├── fast-json-stringify (serialización)
  ├── avvio (plugin bootstrapper)
  ├── Pino (logger estructurado)
  └── @fastify/swagger (OpenAPI)
```

### Características clave

<span class="tag">⚡</span> 2-3x más rápido que Express  
<span class="tag">📐</span> Schema-first (JSON Schema)  
<span class="tag">🔌</span> Sistema de plugins encapsulados  
<span class="tag">📝</span> Logger nativo (Pino)  
<span class="tag">📄</span> Swagger autogenerado con schemas

</div>
</div>

---

<!-- ================================================================ -->
<!-- SLIDE 11 — FASTIFY: CÓDIGO EN ACCIÓN -->
<!-- ================================================================ -->

<!--
note: 💻 FASTIFY — ANÁLISIS DEL CÓDIGO

Acá se ve cómo Fastify materializa el mismo concepto que FastAPI, pero con JSON Schema en vez de Pydantic.

🗣️ PARA DECIR:
- "El schema es un objeto JSON común y corriente — no necesitás clases, librerías externas ni herencia"
- "register() con await es CLAVE — sin await, Swagger no detecta las rutas (lo sufrimos en la práctica)"
- "Cada ruta tiene un schema inline con type, properties, etc. Ese schema ES la documentación + validación"
- "El handler es async — Fastify maneja promesas de forma nativa"

❓ PREGUNTAR:
- "¿Ven la diferencia con FastAPI? En FastAPI el schema es un modelo de Python (class Usuario(BaseModel)). Acá es un objeto JSON literal. Misma idea, distinta sintaxis"
- "¿Qué ventaja tiene el schema inline? (todo en un mismo lugar, fácil de leer)"
- "¿Qué desventaja? (puede repetirse — para eso existen las referencias $ref)"

💡 SEÑALAR: la propiedad "summary" en el schema — es lo que Swagger muestra como título del endpoint.

🔗 RELACIONAR: con el slide 13 (El contrato en acción) donde se compara el mismo endpoint en ambos frameworks.
-->

# Fastify — Código en acción

```typescript
import Fastify from "fastify";
import fastifySwagger from "@fastify/swagger";
import fastifySwaggerUi from "@fastify/swagger-ui";

const app = Fastify({ logger: true });

await app.register(fastifySwagger, {
  openapi: { info: { title: "Mi API", version: "0.1.0" } },
});
await app.register(fastifySwaggerUi, { routePrefix: "/docs" });

app.get("/", {
  schema: { summary: "Raíz", response: { 200: {
    type: "object", properties: { message: { type: "string" } },
  }}},
}, async () => ({ message: "Hola desde Fastify" }));

app.get("/health", {
  schema: { summary: "Health check", response: { 200: {
    type: "object", properties: {
      status: { type: "string" }, service: { type: "string" },
    },
  }}},
}, async () => ({ status: "ok", service: "fastify-hello" }));

await app.listen({ port: 3000 });
```

---

<!-- ================================================================ -->
<!-- SLIDE 12 — COMPARATIVA FASTAPI vs FASTIFY -->
<!-- ================================================================ -->

<!--
note: ⚖️ COMPARATIVA — NO SE TRATA DE CUÁL ES "MEJOR"

El objetivo de esta slide NO es decir que uno es mejor que el otro, sino dar criterios para ELEGIR según el contexto.

🗣️ PARA DECIR:
- "No existe el mejor framework. Existe el framework adecuado para TU contexto"
- "Si tu equipo viene de Python, eligen FastAPI. Si viene de TypeScript, eligen Fastify"
- "Si necesitás prototipar rápido y tenés un dataset para exponer: FastAPI es imbatible"
- "Si necesitás máximo rendimiento y tenés un ecosistema Node.js: Fastify es la respuesta"
- "MIREN LA FILA DE SWAGGER: FastAPI lo trae automático, Fastify necesita plugins. No es que uno sea mejor — es filosófico: FastAPI prefiere convención sobre configuración, Fastify prefiere explícito sobre implícito"

❓ PREGUNTAR:
- "¿Con cuál se sienten más cómodos ustedes?" (depende de su background — Python vs TypeScript)
- "Si tuvieran que exponer un modelo de Machine Learning, ¿cuál elegirían?" (FastAPI — ecosistema Python/ML)
- "Si tuvieran que construir una API con muchas rutas y plugins, ¿cuál?" (Fastify — sistema de plugins)
- "¿Y si el equipo sabe los dos?" (cualquiera — elijan por el proyecto, no por el lenguaje)

💡 CLAVE: ambos generan OpenAPI automáticamente. Ambos validan. Ambos documentan. La diferencia es CÓMO se escribe el schema.
-->

# FastAPI vs Fastify

| Aspecto | FastAPI 🐍 | Fastify ⚡ |
|---------|-----------|-----------|
| **Lenguaje** | Python 3.8+ | TypeScript / Node.js |
| **Server** | Uvicorn (ASGI) | Node.js HTTP |
| **Schemas** | Pydantic (type hints) | JSON Schema |
| **Validación** | Automática por tipo | Con schema JSON |
| **Serializer** | Pydantic `.model_dump()` | `fast-json-stringify` |
| **Async** | `async def` nativo | Siempre async |
| **Swagger** | `/docs` automático (sin plugins) | `@fastify/swagger` + `@fastify/swagger-ui` |
| **Rendimiento** | Muy alto (~25k req/s) | Muy alto (~35k req/s) |
| **Ecosistema** | Starlette + Pydantic | Plugin encapsulado |
| **Curva de aprendizaje** | Baja (Python puro) | Media (TypeScript + plugins) |

### ¿Cuándo usar cuál?

<span class="tag">🐍 FastAPI</span> Si el equipo viene de Python, necesitás prototipar rápido, o tu ecosistema incluye ML/data science.

<span class="tag">⚡ Fastify</span> Si el equipo ya usa TypeScript, necesitás máximo rendimiento, o querés un sistema de plugins más estructurado.

---

<!-- ================================================================ -->
<!-- SLIDE 13 — EL CONTRATO EN AMBOS FRAMEWORKS -->
<!-- ================================================================ -->

<!--
note: 🧩 EL CONTRATO VISTO EN AMBOS FRAMEWORKS

Esta slide unifica el concepto: el contrato NO es framework-dependent. Es una IDEA que se materializa distinto según la tecnología.

🗣️ PARA DECIR:
- "Acá vemos el MISMO endpoint en ambos frameworks — crear un usuario"
- "FastAPI: un modelo Pydantic con type hints. Fastify: un objeto JSON Schema"
- "El resultado es el MISMO: validación automática, documentación Swagger, serialización"
- "Lo IMPORTANTE no es la sintaxis — es el CONCEPTO: definís el contrato UNA VEZ y todo lo demás se deriva"

❓ PREGUNTAR:
- "Si supieran Python pero no TypeScript, ¿podrían entender el código de la derecha?" (probablemente sí — la estructura es similar)
- "¿Qué prefieren? ¿Modelos con type hints o schemas JSON?" (gustos personales, ninguno es incorrecto)

💡 MENSAJE PARA LLEVARSE: el principio es TRANSVERSAL. Aprendé el concepto, no la sintaxis de un framework en particular. Cuando entiendas "schema como contrato", podés aplicar la idea en cualquier lenguaje.

🔗 RELACIONAR con: el slide de cierre donde se resume todo.
-->

# El contrato en acción

<div class="columns">
<div>

### FastAPI — Schema como modelo

```python
class Usuario(BaseModel):
    nombre: str
    email: str
    edad: int

@app.post("/usuarios")
def crear(usuario: Usuario):
    ...
```

El **modelo Pydantic** ES el contrato.  
Swagger lo refleja automáticamente.

✅ Sin duplicación  
✅ Un cambio, un lugar  
✅ Validación + doc + spec

</div>
<div>

### Fastify — Schema como objeto

```typescript
const schema = {
  body: {
    type: "object",
    required: ["nombre", "email"],
    properties: {
      nombre: { type: "string" },
      email: { type: "string", format: "email" },
      edad: { type: "integer" },
    },
  },
};

app.post("/usuarios", { schema }, handler);
```

El **schema JSON** ES el contrato.  
Swagger lo refleja automáticamente.

✅ Sin duplicación  
✅ Un cambio, un lugar  
✅ Validación + doc + spec

</div>
</div>

> 🧠 **Idea clave**: En ambos frameworks, **definís el contrato una vez** y de ahí se deriva: validación, documentación, serialización y spec OpenAPI. El contrato NO es un archivo aparte — **ES el código**.

---

<!-- ================================================================ -->
<!-- SLIDE 14 — CIERRE -->
<!-- ================================================================ -->

<!--
note: ✅ CIERRE — RECAPITULACIÓN Y PREGUNTAS

Este es el momento de cerrar la clase y verificar que los conceptos clave quedaron claros.

🗣️ PARA DECIR:
- "Recorrimos un montón: backend, REST, contratos, OpenAPI, FastAPI y Fastify"
- "El hilo conductor es el CONTRATO: definís los datos una vez, y de ahí sale validación + documentación + spec"
- "La frase para llevar: EL SCHEMA ES EL CONTRATO — el contrato genera la documentación — la documentación ES la API"

❓ PREGUNTAR (para verificar comprensión):
1. "¿Cuál es la diferencia entre PUT y PATCH?" (PUT = reemplazo total, PATCH = parcial)
2. "¿Por qué POST no es idempotente?" (cada POST crea un recurso nuevo)
3. "¿Qué genera OpenAPI?" (la especificación de la API en JSON/YAML)
4. "¿Qué hace el schema en Fastify/FastAPI?" (valida, documenta y serializa automáticamente)
5. "¿El contrato se escribe a mano o se genera?" (se genera del código automáticamente)

💡 ACTIVIDAD POST-CLASE:
- "Creen un endpoint nuevo en el proyecto que devuelva la fecha actual"
- "Agreguen un schema de respuesta para que aparezca en Swagger"
- "Verifiquen que el spec OpenAPI se actualice automáticamente"

🔗 RELACIONAR con: la próxima clase donde profundizamos en rutas, parámetros y métodos HTTP.
-->

# Resumen

<div class="columns">
<div>

### Conceptos

<span class="tag">🏗️</span> **Backend** = lógica del servidor, expuesta vía API

<span class="tag">🌐</span> **REST** = estilo arquitectónico con verbos HTTP y recursos

<span class="tag">📝</span> **Contrato** = acuerdo formal entre cliente y servidor

<span class="tag">📖</span> **OpenAPI** = estándar para describir APIs

</div>
<div>

### Frameworks

<span class="tag tag-green">🐍 FastAPI</span> Python, type hints, Pydantic, async nativo

<span class="tag tag-yellow">⚡ Fastify</span> TypeScript, schema-first, plugins encapsulados

### El principio fundamental

> **El schema es el contrato.  
> El contrato genera la documentación.  
> La documentación es la API.**

</div>
</div>

<div style="text-align: center; color: #888; font-size: 0.8em; margin-top: 0.3em;">
Desarrollo de Software — 4° año Ing. de Software · UTN FRLP
</div>

---

<!-- ================================================================ -->
<!-- SLIDE 15 — REFERENCIAS -->
<!-- ================================================================ -->

<!--
note: 📚 REFERENCIAS Y RECURSOS

Slide de cierre. Ideal dejarlo visible mientras los alumnos se van o mientras abren los links.

🗣️ PARA DECIR:
- "Todas las referencias que vieron están acá. Las URLs también están en las NOTAS ACADEMICAS del repositorio"
- "La documentación oficial de Fastify y FastAPI son EXCELENTES — léanlas, no se salteen los tutorials"
- "OpenAPI Specification es el estándar — si entienden eso, entienden cualquier API del mercado"
- "Pydantic y JSON Schema son las bases — entenderlos es entender cómo funciona la validación por debajo"

💡 RECOMENDACIÓN:
- "Empiecen por los tutorials oficiales de FastAPI y Fastify"
- "Después hagan el ejercicios de la guía"
- "Después rompan cosas — modifiquen schemas, agreguen rutas, vean cómo responde Swagger"

🔗 Los links están en el repositorio bajo typescript/fastify-hello/NOTAS_ACADEMICAS.md y python/fastapi-hello/NOTAS_ACADEMICAS.md
-->

# Referencias

| Recurso | URL |
|---------|-----|
| **FastAPI** | https://fastapi.tiangolo.com/ |
| **Fastify** | https://fastify.dev/ |
| **OpenAPI Specification** | https://spec.openapis.org/oas/v3.0.3 |
| **Swagger UI** | https://swagger.io/tools/swagger-ui/ |
| **JSON Schema** | https://json-schema.org/ |
| **Pydantic** | https://docs.pydantic.dev/ |
| **RESTful API Design** | https://restfulapi.net/ |

<div style="text-align: center; color: #888; font-size: 0.75em; margin-top: 0.5em;">
Presentación generada con <strong>Marp</strong> · Markdown Presentation Ecosystem
</div>
