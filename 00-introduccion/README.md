# Módulo 00 — Introducción al Backend

> **Materia**: Desarrollo de Software
> **Carrera**: Ingeniería de Software — 4to año
> **Universidad**: UTN Facultad Regional La Plata

---

## Objetivo del Módulo

Presentar los dos frameworks que vamos a usar a lo largo del cursado — **FastAPI** (Python) y **Fastify** (TypeScript) — a través de un ejemplo mínimo: un servidor con dos endpoints y documentación Swagger automática.

El punto no es "aprender dos frameworks". El punto es **entender los conceptos que están detrás de todo framework backend** y ver cómo se materializan en dos ecosistemas diferentes.

---

## Qué vas a encontrar acá

| Contenido | Descripción |
|-----------|-------------|
| **`python/fastapi-hello/`** | Hola Mundo con FastAPI — type hints, Pydantic, Swagger automático |
| **`typescript/fastify-hello/`** | Hola Mundo con Fastify — schemas JSON, plugins, hot-reload |
| **`PRESENTACION_BACKEND.*`** | Presentación del módulo backend (HTML, MD, PDF) |

---

## Frameworks

| Framework | Lenguaje | Filosofía |
|-----------|----------|-----------|
| **FastAPI** | Python 3.12+ | Type hints, validación automática, async nativo, documentación OpenAPI automática |
| **Fastify** | TypeScript / Node.js | Schema-first, alto rendimiento, plugins encapsulados, logging nativo |

---

## Competencias que se desarrollan en este módulo

- **HTTP y diseño de APIs REST** — entender el protocolo, diseñar recursos, usar códigos de estado correctamente
- **Documentación automática** — Swagger UI y OpenAPI generados a partir del código
- **Validación de datos** — garantizar que los datos que entran y salen sean correctos
- **Setup de entorno** — virtualenv, pnpm, hot-reload, configuración de proxy

---

## Cómo usar este material

1. **Leé las notas académicas** (`NOTAS_ACADEMICAS.md`) antes de ejecutar código
2. **Ejecutá los ejemplos** y experimentá modificándolos
3. **Hacé los ejercicios** — en especial los nivel 🟡 y 🔴
4. **Investigá** — usá las referencias para ir más profundo

### FastAPI

```bash
cd python/fastapi-hello
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

### Fastify

```bash
cd typescript/fastify-hello
pnpm install
pnpm dev
```

> ⚠️ npm está bloqueado por el firewall Fortigate de la UTN. Todos los ejemplos usan **pnpm**.
> Si es tu primera vez, seguí la [Guía de Setup desde Cero](./typescript/fastify-hello/GUIA_SETUP_PASO_A_PASO.md).

---

## Estructura

```
00-introduccion/
├── README.md                              # Este archivo
├── PRESENTACION_BACKEND.html              # Presentación (HTML)
├── PRESENTACION_BACKEND.md                # Presentación (Markdown)
├── PRESENTACION_BACKEND.pdf               # Presentación (PDF)
│
├── python/
│   ├── type_hints.py                      # Introducción a type hints (base de FastAPI)
│   └── fastapi-hello/
│       ├── main.py                        # Hola Mundo + health check
│       ├── requirements.txt
│       ├── NOTAS_ACADEMICAS.md            # Material de estudio completo
│       └── README.md                      # Guía rápida
│
└── typescript/
    └── fastify-hello/
        ├── src/index.ts                   # Hola Mundo + health check
        ├── package.json
        ├── tsconfig.json
        ├── .npmrc
        ├── NOTAS_ACADEMICAS.md            # Material de estudio completo
        ├── GUIA_SETUP_PASO_A_PASO.md      # Setup desde cero con pnpm
        └── README.md                      # Guía rápida
```

---

## Referencias

- [FastAPI — Documentación oficial](https://fastapi.tiangolo.com/)
- [Fastify — Documentación oficial](https://fastify.dev/)
- [TypeScript — Documentación oficial](https://www.typescriptlang.org/docs/)
- [Python — Documentación oficial](https://docs.python.org/3/)
