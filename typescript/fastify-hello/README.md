# ⚡ Fastify — Hola Mundo

> **Materia**: Desarrollo de Software — Backend  
> **Framework**: Fastify 5.x (TypeScript / Node.js)

Ejemplo mínimo de API REST con Fastify, schemas JSON, documentación Swagger automática y health check.

---

## ⚙️ Requisitos

- Node.js 18 LTS o superior (recomendada 22 LTS)
- **pnpm** (npm está bloqueado por el firewall Fortigate)

> ⚠️ **¿No tenés pnpm?** Seguí la **[Guía de Setup desde Cero](./GUIA_SETUP_PASO_A_PASO.md)** que te enseña a instalarlo con corepack y configurar el proxy de la UTN.

---

## 🚀 Cómo ejecutar

```bash
# 1. Entrar al directorio
cd typescript/fastify-hello

# 2. Instalar dependencias
pnpm install

# 3. Iniciar servidor (con hot-reload)
pnpm dev
```

> Hot-reload con `node --watch` nativo — **no necesita nodemon**. Al guardar un archivo, el servidor se reinicia solo.

---

## 🔗 Endpoints

| Método | Ruta | Descripción |
|--------|------|-------------|
| `GET` | `/` | Mensaje de bienvenida |
| `GET` | `/health` | Health check del servicio |

### Probar con curl

```bash
curl http://localhost:3000/
# → {"message":"¡Hola, mundo desde Fastify!"}

curl http://localhost:3000/health
# → {"status":"ok","service":"fastify-hello"}
```

---

## 📖 Documentación interactiva

Con el servidor corriendo, abrí en el navegador:

| Herramienta | URL |
|-------------|-----|
| **Swagger UI** | http://localhost:3000/docs |
| **OpenAPI spec (JSON)** | http://localhost:3000/docs/json |

Fastify genera el spec OpenAPI a partir de los **schemas JSON** definidos en cada ruta. Sin schemas, Swagger no muestra nada útil — por eso cada endpoint tiene su schema.

---

## 📦 Scripts disponibles

| Script | Comando | Descripción |
|--------|---------|-------------|
| `dev` | `node --import tsx/esm --watch src/index.ts` | Desarrollo con hot-reload |
| `start` | `node --import tsx/esm src/index.ts` | Producción |
| `typecheck` | `tsc --noEmit` | Verificar tipos TypeScript |
| `clean` | `rm -rf node_modules dist` | Limpiar dependencias |

---

## 📁 Estructura

```
fastify-hello/
├── src/
│   └── index.ts              # Código del servidor
├── package.json              # Dependencias y scripts
├── tsconfig.json             # Configuración de TypeScript
├── .npmrc                    # Configuración de pnpm
├── NOTAS_ACADEMICAS.md       # Material de estudio completo
├── GUIA_SETUP_PASO_A_PASO.md # Setup desde cero con pnpm
└── README.md                 # Esta guía rápida
```

---

## 📚 Más información

- [Documentación oficial de Fastify](https://fastify.dev/)
- [Guía de setup desde cero](./GUIA_SETUP_PASO_A_PASO.md) — para crear el proyecto desde `mkdir`
- [Notas académicas](./NOTAS_ACADEMICAS.md) — explicación conceptual detallada
