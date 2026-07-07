# 📘 Fastify — Notas Académicas

> **Curso**: Desarrollo Web — Backend
> **Tema**: Introducción a Fastify
> **Nivel**: 4to año — Ingeniería de Software
> **Framework**: Fastify 5.x

---

## 1. ¿Qué es Fastify?

Fastify es un **framework web para Node.js** enfocado en rendimiento, baja sobrecarga y una experiencia de desarrollo productiva.

| Atributo | Descripción |
|---|---|
| **Creadores** | Matteo Collina y Tomas Della Vedova |
| **Lanzamiento** | 2017 |
| **Licencia** | MIT |
| **Repositorio** | https://github.com/fastify/fastify |
| **Documentación** | https://fastify.dev/ |

### Filosofía de diseño

1. **Rendimiento como objetivo principal**
   - Hasta 2-3x más rápido que Express en benchmarks
   - Serialización optimizada con schemas JSON
   - Overhead mínimo en el core

2. **Basado en esquemas (schema-first)**
   - JSON Schema para validación de entrada/salida
   - Serialización optimizada cuando se define el schema de respuesta
   - Validación automática sin código imperativo

3. **Arquitectura de plugins como ciudadanos de primera clase**
   - Todo es un plugin (rutas, middleware, decorators)
   - Encapsulación de contexto (herencia de alcance)
   - Sistema de plugins inspirado en el patrón de módulos de Node.js

4. **Developer Experience**
   - Logger nativo con Pino (logs JSON estructurados)
   - TypeScript support de primera clase
   - Documentación autogenerada con Swagger (plugin oficial)
   - Sistema de hooks (before, after, onSend, onError)

### Stack tecnológico subyacente

```
Fastify
  ├── find-my-way (router de alta performance)
  │     └── Basado en radix tree (árbol compacto)
  ├── tiny-lru (caché LRU para schema lookup)
  ├── secure-json-parse (JSON parsing seguro)
  ├── avvio (bootstrapper, manejo de plugins)
  ├── light-my-request (simulación de requests para testing)
  └── Pino (logger estructurado)
```

> 📌 **Concepto clave**: Fastify NO es "otro Express". Tiene una arquitectura fundamentalmente diferente basada en el patrón **encapsulación de plugins** y **validación por schemas**.

---

## 2. Conceptos Fundamentales

### 2.1 Sistema de Plugins y Encapsulación

En Fastify, **TODO es un plugin** — las rutas, la configuración, los decorators.

```typescript
import Fastify from "fastify";

const app = Fastify();

// Registrar un plugin (una función que recibe la instancia)
app.register(async function meuPlugin(instance, opts) {
  instance.get("/ruta-dentro-del-plugin", async () => {
    return { desde: "el plugin" };
  });
});
```

La encapsulación significa que:
- Lo que se declara dentro de un plugin **no escapa** al contexto padre
- Los plugins hijos heredan el contexto del padre, pero no al revés
- Esto evita colisiones de nombres y efectos secundarios

> 🧠 **Analogía**: Piensa en los plugins como funciones con scope léxico. Lo que declaras dentro queda dentro, a menos que lo exportes explícitamente.

### 2.2 Schema Serialization vs Validación Imperativa

Express típico:
```javascript
app.post("/user", (req, res) => {
  const { name, age } = req.body;
  if (!name || typeof name !== "string") {
    return res.status(400).json({ error: "name inválido" });
  }
  if (typeof age !== "number" || age < 0) {
    return res.status(400).json({ error: "age inválido" });
  }
  // ... lógica de negocio mezclada con validación
});
```

Fastify:
```typescript
import Fastify from "fastify";

const app = Fastify();

const schema = {
  body: {
    type: "object",
    required: ["name", "age"],
    properties: {
      name: { type: "string" },
      age: { type: "number", minimum: 0 },
    },
  },
};

app.post("/user", { schema }, async (request) => {
  // Si llegamos acá, los datos YA están validados
  // request.body tiene el tipo inferido del schema
  const { name, age } = request.body;
  // ... solo lógica de negocio
});
```

**Ventajas del approach schema-first:**
- Validación automática (sin código imperativo)
- Serialización optimizada (Fastify compila el schema a una función)
- Documentación autogenerada (OpenAPI vía plugin)
- Tipos inferidos automáticamente

### 2.3 Logger Nativo (Pino)

Fastify incluye logger por defecto. No es un middleware externo — es parte del core.

```typescript
const app = Fastify({ logger: true });

app.get("/", async (request, reply) => {
  request.log.info("Procesando petición GET /");
  // request.log tiene bindings del request (id, método, url)
  return { hola: "mundo" };
});
```

Pino produce logs JSON estructurados, ideales para:
- Sistemas de logging centralizado (ELK, Datadog, Grafana Loki)
- Procesamiento automático
- Búsqueda y filtrado

### 2.4 Hooks (Ciclo de Vida)

Fastify expone hooks en distintas etapas del ciclo de vida de una petición:

```
Request → onRequest → preParsing → preValidation → preHandler
         → handler → preSerialization → onSend → Response
```

Ejemplo de hook de autenticación:
```typescript
app.addHook("preHandler", async (request, reply) => {
  const token = request.headers.authorization;
  if (!token) {
    reply.status(401).send({ error: "No autorizado" });
  }
});
```

---

## 3. Análisis del Código — Hola Mundo

```typescript
import Fastify from "fastify";
```

Importamos la función `Fastify` (convención: el export por defecto de Fastify usa PascalCase).

```typescript
const app = Fastify({
  logger: true,
});
```

Creamos la instancia con `logger: true`. Esto activa Pino, que mostrará logs estructurados en la terminal. Cada request generará un log con su método, url, status code y duración.

```typescript
app.get("/", async () => {
  return { message: "¡Hola, mundo desde Fastify!" };
});
```

Registramos una ruta GET en `/`. El handler es `async` — en Fastify, los handlers SIEMPRE deben ser async o retornar una promesa. El objeto retornado se serializa automáticamente a JSON.

> 🧠 ¿Por qué `async` aunque no haya operaciones asincrónicas?
> - Consistencia: si después agregamos una DB call, no cambia la firma
> - Fastify optimiza el manejo de promesas
> - Manejo de errores consistente (las promesas rechazadas se capturan)

```typescript
app.get("/health", async () => {
  return { status: "ok", service: "fastify-hello" };
});
```

Endpoint de health check — estándar de la industria para monitoreo.

```typescript
const start = async (): Promise<void> => {
  try {
    const port = 3000;
    const address = await app.listen({ port });
    app.log.info(`Servidor escuchando en ${address}`);
  } catch (err) {
    app.log.error(err);
    process.exit(1);
  }
};

start();
```

Función autoinvocada que inicia el servidor. El `try/catch` captura errores de inicio (puerto ocupado, permisos, etc.) y termina el proceso con código de error.

### 3.1 Flujo de una petición

```
Cliente                              Fastify
  │                                      │
  │  GET / HTTP/1.1                      │
  │──────────────────────────────────────>│
  │                                      │
  │                         1. find-my-way matchea la ruta
  │                           (radix tree) → handler registrado
  │                                      │
  │                         2. Ejecuta hooks preHandler
  │                                      │
  │                         3. Ejecuta handler
  │                           return { message: "..." }
  │                                      │
  │                         4. Serializa a JSON
  │                           (usa schema si está definido,
  │                            sino JSON.stringify nativo)
  │                                      │
  │                         5. reply.send() implícito
  │                                      │
  │  200 OK                               │
  │  Content-Type: application/json      │
  │  {"message": "¡Hola, mundo..."}      │
  │<──────────────────────────────────────│
  │                                      │
  │                         6. Pino log:
  │  {"req":..., "res":..., "responseTime": 2}
```

---

## 4. Ejercicios Propuestos

### 🟢 Nivel 1 — Comprensión

1. Ejecutar la aplicación y probar ambos endpoints con `curl` o el navegador.
2. Revisar los logs de Pino en la terminal. ¿Qué información captura cada request?
3. Cambiar `logger: true` a `logger: false`. ¿Qué cambia en la salida? ¿Conviene en producción?

### 🟡 Nivel 2 — Aplicación

1. Agregar un endpoint `GET /version` que retorne `{ "version": "0.1.0" }`.
2. Agregar un endpoint `GET /saludo/:nombre` que use un parámetro de ruta y retorne `{ "message": "¡Hola, {nombre}!" }`.
   - *Ayuda: Fastify usa `:param` en la ruta y `request.params`*
3. Agregar un hook `preHandler` que loguee "Petición recibida" antes de cada handler.

### 🔴 Nivel 3 — Análisis

1. Definir un schema JSON para el endpoint `/saludo/:nombre` que valide que `nombre` sea un string de al menos 2 caracteres.
2. Investigar: ¿cómo implementa Fastify el schema-compiled serialization? Revisar `fast-json-stringify`.
3. Comparar el rendimiento de este servidor con uno equivalente en Express. ¿Dónde está la diferencia?

---

## 5. Buenas Prácticas Demostradas

| Práctica | ¿Cómo se aplica? |
|---|---|
| **Separación de concerns** | Endpoints de negocio vs monitoreo |
| **Logging estructurado** | Pino activado desde la configuración |
| **Código async consistente** | Todos los handlers son async |
| **Error handling** | try/catch en `start()`, captura errores de inicio |
| **Configuración explícita** | Fastify configurado con opciones al crearse |
| **Tipado fuerte** | TypeScript strict mode con Fastify |

---

## 6. Comparativa: Fastify vs Express

| Aspecto | Express | Fastify |
|---|---|---|
| **Router** | Array lineal de middlewares | Radix tree (find-my-way) |
| **Validación** | Manual (código imperativo) | JSON Schema (declarativo) |
| **Logger** | No incluido (morgan, winston) | Pino integrado |
| **Plugins** | app.use() | Sistema con encapsulación |
| **Serialización** | JSON.stringify | Schema-compiled (fast-json-stringify) |
| **TypeScript** | Tipados comunitarios | Tipados oficiales |
| **Rendimiento** | ~15k req/s | ~30k+ req/s |
| **Hooks** | Middleware secuencial | Ciclo de vida formal |

> 📌 Ambos son válidos. Express es más simple y tiene un ecosistema más grande. Fastify es más estructurado y rendidor. La elección depende del contexto.

---

## 7. Preguntas de Autoevaluación

1. ¿Qué ventaja tiene el sistema de plugins encapsulados de Fastify sobre el middleware global de Express?
2. ¿Por qué la serialización basada en schemas es más rápida que `JSON.stringify()`?
3. ¿Qué es un radix tree y por qué es más eficiente que un array de rutas?
4. Si no definimos un schema en Fastify, ¿qué pasa con la validación y serialización?
5. ¿En qué casos conviene usar Fastify en lugar de Express? ¿Y al revés?

---

## 8. Referencias

- [Fastify Official Docs](https://fastify.dev/)
- [Fastify GitHub](https://github.com/fastify/fastify)
- [find-my-way (router)](https://github.com/delvedor/find-my-way)
- [Pino (logger)](https://getpino.io/)
- [JSON Schema](https://json-schema.org/)
- [fast-json-stringify](https://github.com/fastify/fast-json-stringify)
- [avvio (plugin bootstrapper)](https://github.com/fastify/avvio)

---

> **📌 Resumen para llevar**: Fastify no compite con Express en el mismo plano. Express es un framework minimalista y flexible. Fastify es un framework estructurado con opiniones fuertes sobre cómo deben hacerse las cosas: schemas, plugins encapsulados, logging nativo, y rendimiento como ciudadano de primera clase. Entender esto es entender cuándo usar cada uno.
