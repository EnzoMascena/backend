# 📘 FastAPI — Notas Académicas

> **Curso**: Desarrollo Web — Backend
> **Tema**: Introducción a FastAPI
> **Nivel**: 4to año — Ingeniería de Software
> **Framework**: FastAPI 0.115+

---

## 1. ¿Qué es FastAPI?

FastAPI es un **framework web moderno para construir APIs con Python 3.8+**.

| Atributo | Descripción |
|---|---|
| **Creador** | Sebastián Ramírez ([@tiangolo](https://github.com/tiangolo)) |
| **Lanzamiento** | 2018 |
| **Licencia** | MIT |
| **Repositorio** | https://github.com/fastapi/fastapi |
| **Documentación** | https://fastapi.tiangolo.com/ |

### Filosofía de diseño

FastAPI se construyó sobre tres pilares fundamentales:

1. **Type hints de Python como ciudadanos de primera clase**
   - No son un "agregado" — son el centro del framework
   - Definen validación, documentación, serialización y tipos

2. **Rendimiento de clase empresarial**
   - Basado en Starlette (ASGI) y Pydantic
   - Comparable con Node.js y Go (según benchmarks)
   - Soporte nativo para async/await

3. **Productividad con cero configuración**
   - Documentación interactiva automática (Swagger UI + ReDoc)
   - Validación automática de parámetros y bodies
   - Editor support completo (autocompletado, type checking)

### Stack tecnológico subyacente

```
FastAPI
  ├── Starlette (servidor ASGI web)
  │     ├── Routing, middleware, WebSocket, Streaming
  │     └── ASGI → Interfaz async estándar para Python web
  └── Pydantic (validación y serialización)
        ├── Modelos basados en type hints
        ├── Validación automática en runtime
        └── Serialización/deserialización JSON
```

> 📌 **Concepto clave**: FastAPI NO es un monolito. Es una capa delgada sobre Starlette y Pydantic. Entender esto es entender el 80% del framework.

---

## 2. Conceptos Fundamentales

### 2.1 ASGI (Asynchronous Server Gateway Interface)

ASGI es el sucesor de WSGI para Python. Es el **contrato** entre servidores web y frameworks.

```
Cliente → Servidor ASGI (Uvicorn) → Aplicación ASGI (FastAPI)
```

- **WSGI** (Web Server Gateway Interface) — síncrono, tradicional (Django, Flask)
- **ASGI** — asíncrono, maneja HTTP, WebSocket, HTTP/2, SSE

Uvicorn es el servidor ASGI que "envuelve" nuestra aplicación FastAPI y la expone al mundo.

### 2.2 Type Hints como Contrato

En FastAPI, los type hints NO son solo documentación — son **contratos que se ejecutan**:

```python
@app.get("/items/{item_id}")
def read_item(item_id: int):  # ← FastAPI valida que item_id sea int automáticamente
    return {"item_id": item_id}
```

Si un cliente envía `GET /items/abc`, FastAPI responde automáticamente con:
```json
{
  "detail": [
    {
      "type": "int_parsing",
      "loc": ["path", "item_id"],
      "msg": "Input should be a valid integer, unable to parse string as an integer"
    }
  ]
}
```

**Sin escribir UNA línea de validación.** Eso es magia — no, eso es **type hints bien aprovechados**.

### 2.3 OpenAPI / Swagger Automático

Cada endpoint que registras genera automáticamente:

- **Schema OpenAPI** (JSON/YAML) — el estándar de la industria para describir APIs
- **Swagger UI** (interactivo) — en `/docs`
- **ReDoc** (documentación limpia) — en `/redoc`

Esto se logra sin configuración extra. FastAPI inspecciona:
- El path y método HTTP
- Los parámetros y sus tipos
- El tipo de retorno
- El docstring de la función
- Los modelos Pydantic usados

### 2.4 Inyección de Dependencias

FastAPI tiene un sistema de **inyección de dependencias** integrado (no necesitas un contenedor DI externo):

```python
from fastapi import Depends

def get_db():
    db = connect()
    try:
        yield db
    finally:
        db.close()

@app.get("/items")
def read_items(db = Depends(get_db)):
    return db.query(Item).all()
```

Ventajas:
- Código más testable (las dependencias se pueden mockear)
- Separación de concerns
- Reutilización de lógica transversal (auth, DB, logging)

---

## 3. Análisis del Código — Hola Mundo

```python
from fastapi import FastAPI
```

Importamos la clase `FastAPI` del paquete `fastapi`. Esta clase es la **aplicación** que configuraremos.

```python
app = FastAPI(
    title="Hola Mundo - FastAPI",
    description="API de ejemplo para el curso de Desarrollo Web - Backend",
    version="0.1.0",
)
```

Creamos una instancia de la aplicación. Los parámetros que le pasamos alimentan la **documentación OpenAPI**. Esto significa que si cambiamos el título, Swagger UI lo refleja automáticamente.

> 🧠 **Pregunta para pensar**: ¿Qué otros parámetros acepta `FastAPI()`? Revisar la documentación.

```python
@app.get("/")
def read_root():
    return {"message": "¡Hola, mundo desde FastAPI!"}
```

El decorador `@app.get("/")` registra una función como manejador del endpoint `GET /`. FastAPI:
1. Asocia el path `/` al método GET
2. Toma el **docstring** de la función para documentación
3. Infiere que el **tipo de retorno** es `dict` y lo serializa a JSON
4. Agrega este endpoint al schema OpenAPI automáticamente

```python
@app.get("/health")
def health_check():
    return {"status": "ok", "service": "fastapi-hello"}
```

Segundo endpoint. `/health` es un **endpoint de monitoreo**. Es buena práctica separar monitoreo de negocio.

### 3.1 Flujo de una petición

```
Cliente                          FastAPI + Uvicorn
  │                                      │
  │  GET / HTTP/1.1                      │
  │──────────────────────────────────────>│
  │                                      │
  │                          Uvicorn recibe la petición
  │                          La convierte al formato ASGI
  │                          La pasa a FastAPI
  │                                      │
  │                          FastAPI matchea la ruta /
  │                          (método GET) → read_root()
  │                                      │
  │                          read_root() ejecuta:
  │                          return {"message": "..."}
  │                                      │
  │                          FastAPI serializa dict → JSON
  │                          Construye respuesta HTTP
  │                                      │
  │  200 OK                               │
  │  Content-Type: application/json       │
  │  {"message": "¡Hola, mundo..."}       │
  │<──────────────────────────────────────│
```

---

## 4. Ejercicios Propuestos

### 🟢 Nivel 1 — Comprensión

1. Ejecutar la aplicación y acceder a `/docs`. Explorar la documentación interactiva. ¿Qué información aparece?
2. Ejecutar la aplicación y acceder a `/redoc`. ¿Qué diferencias ves con Swagger UI?
3. Hacer una petición GET a `/health` con `curl` desde la terminal. ¿Qué responde?

### 🟡 Nivel 2 — Aplicación

1. Agregar un nuevo endpoint `GET /version` que retorne la versión de la API.
2. Modificar el endpoint `/` para que acepte un parámetro `name` en la URL y salude personalizadamente:
   - `GET /?name=Juan` → `{"message": "¡Hola, Juan desde FastAPI!"}`
   - *Ayuda: investigar `fastapi.Query` o el parámetro directo en la función*
3. Agregar logging manual usando el módulo `logging` de Python.

### 🔴 Nivel 3 — Análisis

1. Cambiar el servidor de Uvicorn a Hypercorn. ¿Qué diferencias notas?
2. Agregar un endpoint que reciba datos por POST y los valide con Pydantic.
3. Investigar: ¿cómo hace FastAPI para generar el schema OpenAPI? Leer el código fuente de `fastapi/routing.py`.

---

## 5. Buenas Prácticas Demostradas

| Práctica | ¿Cómo se aplica? |
|---|---|
| **Separación de concerns** | Endpoint de negocio (`/`) vs monitoreo (`/health`) |
| **Documentación desde el código** | Docstrings + type hints generan docs automáticas |
| **Configuración explícita** | Parámetros de `FastAPI()` definen metadata |
| **Código limpio y legible** | Sin configuración boilerplate innecesaria |
| **Tipado como documentación ejecutable** | Type hints validan en runtime |

---

## 6. Preguntas de Autoevaluación

1. ¿Qué diferencia a FastAPI de Flask en términos de validación de datos?
2. ¿Por qué FastAPI puede ser más rápido que Flask? (pista: mirar el stack)
3. ¿Qué es ASGI y por qué es importante para FastAPI?
4. Si no usáramos type hints, ¿FastAPI funcionaría igual? ¿Qué perderíamos?
5. ¿Qué ventajas tiene tener documentación OpenAPI generada automáticamente?

---

## 7. Referencias

- [FastAPI Official Docs](https://fastapi.tiangolo.com/)
- [FastAPI GitHub](https://github.com/fastapi/fastapi)
- [Starlette (servidor ASGI)](https://www.starlette.io/)
- [Pydantic (validación)](https://docs.pydantic.dev/)
- [ASGI Specification](https://asgi.readthedocs.io/)
- [Uvicorn (servidor ASGI)](https://www.uvicorn.org/)

---

> **📌 Resumen para llevar**: FastAPI convierte type hints de Python en un framework web completo. No es magia — es aprovechar al máximo el sistema de tipos de Python para definir **contratos** que se validan, documentan y ejecutan solos. Entender esto es entender FastAPI.
