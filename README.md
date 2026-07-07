# 🎓 Desarrollo Web — Backend

> **Materia**: Desarrollo Web  
> **Carrera**: Ingeniería de Software — 4to año  
> **Universidad**: UTN Facultad Regional La Plata

---

## ⚠️ AVISO IMPORTANTE — Naturaleza del Repositorio

**ESTE REPOSITORIO ES DE CARÁCTER EXCLUSIVAMENTE ACADÉMICO Y COMPLEMENTARIO.**

El material aquí contenido **NO es obligatorio** para la aprobación de la materia. No hay entregas que evaluar, ni puntos que sumar, ni notas que dependan de esto.

El **único objetivo** es **formar competencias profesionales** en desarrollo backend. Está pensado para aquellos estudiantes que:

- Quieran ir más allá del contenido mínimo de la cursada
- Busquen desarrollar habilidades que las empresas demandan hoy
- Entiendan que la Universidad marca el camino, pero el **profesional se construye a sí mismo**
- Tengan como **objetivo personal** adquirir herramientas nuevas para su perfil profesional

> 🧠 *"La Universidad te da el mapa. El recorrido lo hacés vos."*

---

## 📋 Descripción

Este repositorio contiene el material práctico del módulo de **Backend** de la materia Desarrollo Web. Acá vas a encontrar ejemplos, laboratorios, notas académicas y proyectos centrados en **dos frameworks modernos**:

| Framework | Lenguaje | Filosofía |
|---|---|---|
| **FastAPI** | Python 3.12+ | Type hints, validación automática, async nativo, documentación OpenAPI automática |
| **Fastify** | TypeScript / Node.js | Schema-first, alto rendimiento, plugins encapsulados, logging nativo |

La idea NO es "aprender dos frameworks". La idea es **aprender los conceptos que están detrás de todo framework backend** — y ver cómo se materializan en dos ecosistemas diferentes.

---

## 🧠 Competencias a Desarrollar

| Competencia | ¿Qué implica? |
|---|---|
| **HTTP y diseño de APIs REST** | Entender el protocolo, diseñar recursos, usar códigos de estado correctamente |
| **Arquitectura en capas** | Separar responsabilidades: Controller → Service → Repository |
| **Validación y serialización** | Garantizar que los datos que entran y salen sean correctos |
| **Persistencia de datos** | Modelar, migrar y consultar bases de datos relacionales |
| **Autenticación y autorización** | JWT, RBAC, protección de rutas, hashing de contraseñas |
| **Testing** | Unitario, integración, mocks — código no testeado es código que no funciona |
| **DevOps básico** | Docker, CI/CD, logging, configuración por entorno |

---

## 📁 Estructura del Repositorio

```
backend/
├── python/
│   ├── type_hints.py                    # Introducción a type hints (base de FastAPI)
│   └── fastapi-hello/
│       ├── main.py                      # Hola Mundo + health check
│       ├── requirements.txt
│       └── NOTAS_ACADEMICAS.md          # Material de estudio completo
│
└── typescript/
│   └── fastify-hello/
│       ├── src/index.ts                 # Hola Mundo + health check
│       ├── package.json
│       ├── tsconfig.json
│       ├── .npmrc
│       └── NOTAS_ACADEMICAS.md          # Material de estudio completo
```

Cada proyecto es **autocontenido** — tiene sus propias dependencias, configuración y notas. Esto permite estudiarlos de forma independiente.

---

## 🚀 Cómo Empezar

### FastAPI

```bash
cd python/fastapi-hello

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar servidor (con hot-reload)
uvicorn main:app --reload --port 8000

# Probar
curl http://localhost:8000/
curl http://localhost:8000/health

# Documentación interactiva
# Abrir en navegador: http://localhost:8000/docs
```

### Fastify

```bash
cd typescript/fastify-hello

# Instalar dependencias
pnpm install

# Ejecutar servidor (con hot-reload)
pnpm dev

# Probar
curl http://localhost:3000/
curl http://localhost:3000/health

# Type check
pnpm typecheck
```

---

## 📚 Material Académico

Cada proyecto incluye un archivo `NOTAS_ACADEMICAS.md` con:

1. **Introducción al framework** — contexto, creador, filosofía, stack tecnológico
2. **Conceptos fundamentales** — cómo funciona por debajo (ASGI, schemas, plugins, etc.)
3. **Análisis línea por línea** del código de ejemplo
4. **Ejercicios progresivos** en 3 niveles de dificultad:
   - 🟢 **Comprensión** — entender qué hace cada parte
   - 🟡 **Aplicación** — modificar y extender el código
   - 🔴 **Análisis** — investigar cómo funciona internamente
5. **Buenas prácticas** demostradas en el código
6. **Preguntas de autoevaluación** para verificar comprensión
7. **Referencias oficiales** para profundizar

---

## 🎯 Para el Estudiante

Este material está diseñado para **autogestión del aprendizaje**. La propuesta es simple:

1. **Leé las notas académicas** antes de ejecutar código
2. **Ejecutá los ejemplos** y experimentá modificándolos
3. **Hacé los ejercicios** — en especial los nivel 🟡 y 🔴
4. **Investigá** — usá las referencias para ir más profundo
5. **Preguntá** — en clase, en el foro, con tus compañeros

No importa si avanzás lento. Importa que **cada concepto lo entiendas de verdad**. No se trata de cuántos frameworks conocés, sino de **cuántos problemas podés resolver**.

---

## 🏗️ Lo Que Viene

El repositorio va a crecer módulo a módulo. El plan a futuro incluye:

- [ ] Laboratorios de HTTP raw con `curl`
- [ ] Servidor HTTP desde cero (sin frameworks)
- [ ] Arquitectura en capas completa (Controller → Service → Repository)
- [ ] Persistencia con PostgreSQL (migraciones, queries, conexiones)
- [ ] Autenticación JWT + RBAC
- [ ] Testing automatizado (unitario + integración)
- [ ] Dockerización y CI/CD
- [ ] Proyecto integrador: API de Gestión de Proyectos y Tareas

---

## 📖 Licencia

Este material es de uso educativo y libre distribución. Hecho con ❤️ para la comunidad de la UTN FRLP.

---

> **📌 Recordatorio final**: Este repositorio no te va a dar una nota. Te va a dar **herramientas**. Lo que hagas con ellas depende de vos. La diferencia entre un ingeniero que sabe y uno que realmente puede está en las horas de práctica que nadie te va a pedir — pero que se notan en cada entrevista técnica, en cada código que escribís, en cada problema que resolvés.
>
> **Ponete las pilas. El mercado no espera.**
