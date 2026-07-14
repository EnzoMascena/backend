# 🛠️ Guía de Setup — Fastify desde Cero

> **Objetivo**: Que puedas crear un proyecto Fastify desde `mkdir` hasta tener el servidor corriendo, usando **pnpm** porque npm está bloqueado por el firewall Fortigate de la UTN.
>
> **Materia**: Desarrollo Web — Backend | **Carrera**: Ingeniería de Software — 4to año

---

## Índice

1. [Verificar prerrequisitos](#1-verificar-prerrequisitos)
2. [Instalar pnpm](#2-instalar-pnpm)
3. [Configurar pnpm para el entorno corporativo](#3-configurar-pnpm-para-el-entorno-corporativo)
4. [Crear el proyecto desde cero](#4-crear-el-proyecto-desde-cero)
5. [Configurar TypeScript](#5-configurar-typescript)
6. [Instalar dependencias](#6-instalar-dependencias)
7. [Escribir el código](#7-escribir-el-código)
8. [Agregar scripts al package.json](#8-agregar-scripts-al-packagejson)
9. [Ejecutar y verificar](#9-ejecutar-y-verificar)
10. [Troubleshooting](#10-troubleshooting)

---

## 1. Verificar prerrequisitos

Antes de arrancar, asegurate de tener esto instalado:

```bash
# Node.js (versión 18 LTS o superior — recomendada 22 LTS)
node --version   # → v18.x.x o v20.x.x o v22.x.x

# Git
git --version    # → git x.x.x
```

> ⚠️ **Si no tenés Node.js**: Descargalo desde [nodejs.org](https://nodejs.org/) (versión LTS). El instalador incluye `npm` y `corepack`. Necesitás Node.js para correr JavaScript fuera del navegador — es el motor de ejecución de Fastify.

```bash
# Verificá que corepack esté disponible (viene con Node.js desde v16.13)
corepack --version   # → 0.x.x
```

`corepack` es la herramienta que viene con Node.js para gestionar package managers (pnpm, yarn, npm) sin necesidad de instalarlos por separado.

---

## 2. Instalar pnpm

Como `npm` está bloqueado por el firewall Fortigate, necesitamos instalar `pnpm` por otro medio. Tenés **3 opciones**, en orden de prioridad:

### Opción recomendada: corepack (la más limpia)

```bash
# Habilitar corepack (solo una vez)
corepack enable

# Instalar la última versión de pnpm
corepack prepare pnpm@latest --activate

# Verificar
pnpm --version   # → 9.x.x
```

Si `corepack` está bloqueado por la red (descarga el binario del registry), pasá a la siguiente opción.

### Opción alternativa: script de instalación standalone

```bash
# Usar el instalador oficial de pnpm vía curl
curl -fsSL https://get.pnpm.io/install.sh | sh -

# Si curl también está bloqueado, descargalo desde una máquina
# con internet y pasalo por USB / disco compartido
```

> 💡 **Tip**: Si ni curl funciona, descargá el script desde tu casa o desde el celular y pasalo por cable / USB.

### Opción de emergencia: package manager del sistema

```bash
# En Linux (Debian/Ubuntu) — puede tener versión anterior
sudo apt install pnpm

# En macOS (Homebrew)
brew install pnpm

# En Windows (Scoop)
scoop install pnpm
```

---

## 3. Configurar pnpm para el entorno corporativo

Si la red de la facultad usa **proxy** (común con Fortigate), configurá pnpm para que funcione:

### 3.1 Configurar proxy de pnpm

```bash
# Reemplazá proxy.frtn.utn.edu.ar:8080 con los datos de tu proxy
# (preguntale a tu profe o al área de sistemas)
pnpm config set proxy http://proxy.frtn.utn.edu.ar:8080
pnpm config set https-proxy http://proxy.frtn.utn.edu.ar:8080
```

### 3.2 Probar conectividad

```bash
# Probar que pnpm puede llegar al registry
pnpm ping
```

> ⚠️ **Si no sabés el proxy**: Abrí Chrome/Edge, andá a Configuración → Proxy. Las settings del sistema te muestran la dirección. O preguntale a un compañero que ya lo tenga funcionando.

### 3.3 Saltear el proxy si estás en tu casa

Cuando estés en tu casa, no necesitás proxy. pnpm usa las variables de entorno estándar:

```bash
# Desactivar proxy temporalmente
pnpm config delete proxy
pnpm config delete https-proxy
```

> 💡 **Pro tip**: Si alternás entre casa y facultad, creá un archivo `.env` con scripts para switchear rápido. O simplemente recordá correr los `config set` cuando estés en la UTN.

---

## 4. Crear el proyecto desde cero

Ahora sí, creamos todo desde `mkdir`.

### 4.1 Crear la estructura de directorios

```bash
# Crear la carpeta del proyecto
mkdir -p ~/Documentos/desa_soft_2026/backend/typescript/fastify-hello

# Entrar al proyecto
cd ~/Documentos/desa_soft_2026/backend/typescript/fastify-hello

# Crear carpeta para el código fuente
mkdir src
```

Tu estructura debería verse así:

```
fastify-hello/
└── src/
```

### 4.2 Inicializar package.json con pnpm

```bash
pnpm init
```

Esto te va a hacer unas preguntas. Respondé:

| Campo | Valor |
|-------|-------|
| name | `fastify-hello` |
| version | `0.1.0` |
| description | `API Hola Mundo con Fastify - Curso de Desarrollo Web (Backend)` |
| entry point | dejalo vacío (vamos a usar scripts custom) |
| test command | dejalo vacío |
| git repository | dejalo vacío |
| keywords | `fastify, api, curso, backend` |
| author | tu nombre |
| license | `MIT` |

> 💡 Si querés esquivar las preguntas: `pnpm init -y` crea todo con valores por defecto. Después editás a mano.

### 4.3 Agregar type: module al package.json

Fastify usa módulos ES (`import`/`export`). Necesitamos decírselo a Node.js.

Editá `package.json` y agregá `"type": "module"` después de `"description"`:

```json
{
  "name": "fastify-hello",
  "version": "0.1.0",
  "description": "API Hola Mundo con Fastify - Curso de Desarrollo Web (Backend)",
  "type": "module",
  // ... resto
}
```

> 📌 **¿Por qué?**: Sin `"type": "module"`, Node.js usa CommonJS (`require()`). Nosotros vamos a escribir `import` de ES Modules. Esta línea le dice a Node.js que todo el proyecto usa ES Modules.

---

## 5. Configurar TypeScript

### 5.1 Crear tsconfig.json

TypeScript necesita un archivo de configuración para saber cómo compilar. Usamos el estándar de Fastify.

Creá `tsconfig.json` en la raíz del proyecto:

```bash
touch tsconfig.json
```

Copiá esto:

```json
{
  "compilerOptions": {
    /* Lenguaje y Entorno */
    "target": "ES2024",
    "lib": ["ES2024"],

    /* Sistema de Módulos */
    "module": "NodeNext",
    "moduleResolution": "NodeNext",

    /* Salida — no la usamos, pero TypeScript la necesita declarada */
    "outDir": "./dist",
    "rootDir": "./src",

    /* Tipado Estricto — Fastify lo recomienda */
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "noImplicitOverride": true,

    /* Interoperabilidad */
    "esModuleInterop": true,
    "forceConsistentCasingInFileNames": true,
    "skipLibCheck": true
  },
  "include": ["src/**/*.ts"],
  "exclude": ["node_modules", "dist"]
}
```

**Campo por campo (lo que importa entender):**

| Opción | ¿Qué hace? |
|--------|-----------|
| `target: ES2024` | Compila a la versión más moderna de JavaScript |
| `module: NodeNext` | Usa el sistema de módulos de Node.js nativo |
| `moduleResolution: NodeNext` | Resuelve imports como Node.js |
| `strict: true` | Activa TODAS las validaciones estrictas de TypeScript |
| `esModuleInterop: true` | Permite importar módulos CommonJS desde ES Modules |

> 📌 **Concepto**: `tsconfig.json` le dice a TypeScript cómo entender tu código. No compilamos a un archivo JS — usamos `tsx` para ejecutar TypeScript directamente. Pero TypeScript necesita esta configuración para el type checking.

### 5.2 Crear .npmrc

Este archivo configura pnpm para el proyecto. Ayuda a evitar problemas con dependencias nativas (como `esbuild`, que usa `tsx` internamente).

Creá `.npmrc`:

```bash
touch .npmrc
```

Contenido:

```ini
# -------------------------------------------------------------------
# Configuración de pnpm para el proyecto
# -------------------------------------------------------------------
# ignore-scripts: evita que pnpm ejecute scripts de build de
# dependencias (como esbuild). Las dependencias ya funcionan sin
# scripts post-install.
# -------------------------------------------------------------------
ignore-scripts=true

# package-manager-strict: desactiva la validación estricta del
# package manager. Sin esto, pnpm requiere que package.json tenga
# el campo "packageManager" definido.
# -------------------------------------------------------------------
package-manager-strict=false
```

> ⚠️ **Cuándo sacar `ignore-scripts=true`**: Si alguna dependencia necesita compilar código nativo (ej: `better-sqlite3`), vas a necesitar sacar esta línea. Para este proyecto Hola Mundo, dejalo así nomás.

---

## 6. Instalar dependencias

### 6.1 Dependencias de producción

Fastify es el framework web. Los plugins de Swagger son para documentación automática:

```bash
pnpm add fastify @fastify/swagger @fastify/swagger-ui
```

| Paquete | ¿Para qué? |
|---------|-----------|
| `fastify` | Framework web en sí |
| `@fastify/swagger` | Genera la especificación OpenAPI 3.0 a partir de los schemas de tus rutas |
| `@fastify/swagger-ui` | Sirve la interfaz visual de Swagger (UI interactiva para probar endpoints) |

### 6.2 Dependencias de desarrollo

TypeScript, los tipos de Node.js, y `tsx` (para ejecutar TypeScript sin compilar):

```bash
pnpm add -D typescript @types/node tsx
```

> 💡 **¿Qué instalamos acá?**
>
> | Paquete | ¿Para qué? |
> |---------|-----------|
> | `typescript` | El compilador de TypeScript (type checking) |
> | `@types/node` | Tipos de Node.js (para que TypeScript conozca `process`, `Buffer`, etc.) |
> | `tsx` | Ejecuta TypeScript directamente (como `node --import tsx`) |

### 6.3 Verificar que se instaló todo

```bash
# Listar dependencias instaladas
pnpm ls --depth=0
```

Deberías ver algo como:

```
dependencies:
fastify 5.x.x
@fastify/swagger 9.x.x
@fastify/swagger-ui 6.x.x

devDependencies:
@types/node 22.x.x
tsx 4.x.x
typescript 5.x.x
```

---

## 7. Escribir el código

### 7.1 Crear el archivo principal

```bash
touch src/index.ts
```

### 7.2 Escribir el servidor Hola Mundo + Swagger

```typescript
/**
 * Módulo principal de la API Hola Mundo con Fastify + Swagger.
 *
 * Fastify es un framework web para Node.js enfocado en:
 *   - Rendimiento (hasta 2x más rápido que Express)
 *   - Baja sobrecarga (overhead mínimo)
 *   - Sistema de plugins (herencia de contexto)
 *   - Validación basada en esquemas JSON (JSON Schema)
 *   - Serialización optimizada con schemas
 *   - Logger nativo (Pino)
 *
 * Para ejecutar:
 *   $ pnpm run dev       # Desarrollo con hot-reload (node --watch + tsx)
 *   $ pnpm start         # Producción
 *
 * Swagger UI:
 *   Abrir http://localhost:3000/docs en el navegador.
 */

import Fastify from "fastify";
import fastifySwagger from "@fastify/swagger";
import fastifySwaggerUi from "@fastify/swagger-ui";

// ---------------------------------------------------------------------------
// Instancia de la aplicación
// ---------------------------------------------------------------------------
// Fastify() recibe un objeto de configuración.
// El logger está habilitado: usa Pino por debajo, produce logs JSON
// estructurados ideales para producción.
const app = Fastify({
  logger: true,
});

// ===========================================================================
// Plugins (registrados ANTES que las rutas — requisito de @fastify/swagger)
// ===========================================================================

// ---------------------------------------------------------------------------
// Plugin: @fastify/swagger — Genera la especificación OpenAPI
// ---------------------------------------------------------------------------
// Escanea las rutas registradas y construye la documentación OpenAPI 3.0
// automáticamente. Si las rutas tienen definido un schema JSON, Swagger
// lo usa para documentar parámetros, bodies, responses, etc.
//
// El await es necesario para que Fastify procese el plugin antes de
// registrar las rutas. Sin await, las rutas pueden no aparecer en el spec.
await app.register(fastifySwagger, {
  openapi: {
    openapi: "3.0.3",
    info: {
      title: "Fastify Hola Mundo",
      description:
        "API de ejemplo para el curso Desarrollo Web — Backend (UTN FRLP)",
      version: "0.1.0",
    },
    servers: [
      { url: "http://localhost:3000", description: "Desarrollo" },
    ],
  },
});

// ---------------------------------------------------------------------------
// Plugin: @fastify/swagger-ui — Sirve la interfaz visual de Swagger
// ---------------------------------------------------------------------------
// Expone la documentación generada en una interfaz web interactiva.
// Swagger UI queda disponible en http://localhost:3000/docs
await app.register(fastifySwaggerUi, {
  routePrefix: "/docs",
});

// ===========================================================================
// Rutas
// ===========================================================================

// ---------------------------------------------------------------------------
// Endpoint raíz
// ---------------------------------------------------------------------------
// .get() registra una ruta GET.
// El segundo parámetro es el objeto de configuración de la ruta (opcional).
// El tercero es el handler.
//
// Acá usamos el parámetro de configuración (objeto con "schema") para
// documentar la respuesta con JSON Schema. Swagger lo va a leer y mostrar
// en la UI.
app.get(
  "/",
  {
    schema: {
      summary: "Mensaje de bienvenida",
      description: "Retorna un saludo de la API",
      response: {
        200: {
          type: "object",
          properties: {
            message: { type: "string", description: "Mensaje de saludo" },
          },
        },
      },
    },
  },
  async () => {
    /**
     * Endpoint raíz.
     * Retorna un mensaje de bienvenida.
     *
     * Demuestra:
     * - Ruta GET más simple posible
     * - Retorno de objeto (Fastify lo serializa a JSON)
     * - Schema de respuesta documentado (Swagger lo refleja)
     */
    return { message: "¡Hola, mundo desde Fastify!" };
  },
);

// ---------------------------------------------------------------------------
// Endpoint de salud
// ---------------------------------------------------------------------------
// Los health checks son un estándar en APIs productivas.
// Herramientas como Kubernetes, Docker y balanceadores de carga
// los usan para verificar disponibilidad del servicio.
app.get(
  "/health",
  {
    schema: {
      summary: "Health check",
      description: "Verifica que el servicio esté operativo",
      response: {
        200: {
          type: "object",
          properties: {
            status: { type: "string", description: "Estado del servicio" },
            service: { type: "string", description: "Nombre del servicio" },
          },
        },
      },
    },
  },
  async () => {
    /**
     * Health check de la API.
     * Retorna el estado del servicio.
     *
     * Separar monitoreo de lógica de negocio es una buena práctica
     * de arquitectura.
     */
    return { status: "ok", service: "fastify-hello" };
  },
);

// ===========================================================================
// Inicio del servidor
// ===========================================================================
// Envolvemos en una función async porque listen() devuelve una promesa.
// Si usáramos await en el scope global, TypeScript en modo ESM lo permite,
// pero hacerlo en una función async es más explícito y portable.
const start = async (): Promise<void> => {
  try {
    const port = 3000;
    const address = await app.listen({ port });
    app.log.info(`Servidor escuchando en ${address}`);
  } catch (err) {
    // Fastify loguea el error automáticamente y terminamos el proceso
    // con código de error para que el orquestador (Docker, PM2, etc.)
    // pueda reiniciar el servicio.
    app.log.error(err);
    process.exit(1);
  }
};

start();
```

---

## 8. Agregar scripts al package.json

Ahora editamos `package.json` para agregar los scripts que nos permiten ejecutar el proyecto fácilmente.

Buscá la sección `"scripts"` y reemplazala por esto:

```json
{
  "scripts": {
    "dev": "node --import tsx/esm --watch src/index.ts",
    "start": "node --import tsx/esm src/index.ts",
    "typecheck": "tsc --noEmit",
    "clean": "rm -rf node_modules dist"
  }
}
```

**Explicación de cada script:**

| Script | Comando | ¿Qué hace? |
|--------|---------|-----------|
| `dev` | `node --import tsx/esm --watch src/index.ts` | Ejecuta en modo desarrollo con **hot-reload** (detecta cambios y reinicia automáticamente) |
| `start` | `node --import tsx/esm src/index.ts` | Ejecuta en modo producción (sin watch) |
| `typecheck` | `tsc --noEmit` | Verifica tipos sin generar archivos JS |
| `clean` | `rm -rf node_modules dist` | Limpia dependencias y build |

> 📌 **¿Qué es `--import tsx/esm`?**: `tsx` es un paquete que permite ejecutar TypeScript directamente. La flag `--import` le dice a Node.js que cargue `tsx/esm` antes de ejecutar el código. Esto "engancha" el loader de TypeScript en el pipeline de módulos de Node.js. El flag `--watch` reinicia el proceso cuando detecta cambios en los archivos.

---

## 9. Ejecutar y verificar

### 9.1 Arrancar el servidor

```bash
pnpm dev
```

Vas a ver algo como:

```
[18:35:42] → src/index.ts
[18:35:42] ✔ starting...
{"level":30,"time":1719340542000,"pid":12345,"hostname":"tu-pc","msg":"Server listening at http://[::1]:3000"}
{"level":30,"time":1719340542000,"pid":12345,"hostname":"tu-pc","msg":"Servidor escuchando en http://[::1]:3000"}
```

> 🎉 **El servidor está corriendo** en `http://localhost:3000`.

### 9.2 Probar los endpoints

Desde otra terminal (o manteniendo el servidor abierto y usando otra terminal):

```bash
# Endpoint raíz
curl http://localhost:3000/
# → {"message":"¡Hola, mundo desde Fastify!"}

# Health check
curl http://localhost:3000/health
# → {"status":"ok","service":"fastify-hello"}
```

También podés abrir `http://localhost:3000/` en tu navegador.

### 9.3 Explorar Swagger UI

Abrí en el navegador: **http://localhost:3000/docs**

Vas a ver la interfaz de Swagger con:

- Los dos endpoints (`/` y `/health`) listados
- Sus descripciones y summaries
- El schema de respuesta de cada uno (tipo de dato, propiedades)
- Un botón **"Try it out"** para ejecutar requests desde el navegador

> 📌 **¿Qué estás viendo?**: Swagger UI es una interfaz interactiva generada **automáticamente** a partir del schema que definiste en cada ruta. No escribiste HTML, CSS ni JS para la documentación — Fastify + Swagger la generan solos.
>
> Además, Swagger expone la especificación en JSON crudo en `http://localhost:3000/docs/json`. Este JSON es el estándar **OpenAPI 3.0** y podés importarlo en herramientas como Postman, Insomnia, o generadores de clients HTTP.

---

> ⚠️ **¿Y nodemon?** — No lo necesitás. El comando `pnpm dev` ya usa `node --import tsx/esm --watch`. El flag `--watch` de Node.js (disponible desde Node 18) reinicia el servidor automáticamente cuando detecta cambios en los archivos. Agregar `nodemon` sería duplicar funcionalidad:
>
> | Herramienta | Mecanismo | ¿Qué hace? |
> |-------------|-----------|-----------|
> | `node --watch` | Nativo de Node.js | Mira archivos, reinicia el proceso al detectar cambios |
> | `tsx` | Loader de TypeScript | Transpila .ts a .js al vuelo sin generar archivos |
> | `nodemon` | Utilidad externa | Mira archivos y ejecuta un comando al detectar cambios |
>
> Con `node --import tsx/esm --watch src/index.ts` tenés **TypeScript + hot-reload en un solo comando**, sin agregar dependencias al pedo. Si en el futuro necesitás un control más fino del watch (ignorar carpetas, delay, etc.), `tsx` tiene su propio modo watch: `tsx watch src/index.ts`.

### 9.4 Verificar types

```bash
pnpm typecheck
```

Si no hay errores de tipos, no muestra nada (exit code 0). Si hay errores, los lista en pantalla.

### 9.5 Detener el servidor

```bash
Ctrl + C
```

---

## 10. Troubleshooting

### 🔴 `pnpm: command not found`

corepack no se instaló bien o no está en el PATH.

```bash
# Probar de nuevo con corepack
corepack enable
corepack prepare pnpm@latest --activate

# Si no funciona, usar la ruta directa:
# En Linux/Mac: el script standalone instala en ~/.local/share/pnpm/pnpm
export PATH="$HOME/.local/share/pnpm:$PATH"

# Agregalo a tu ~/.bashrc o ~/.zshrc para que persista:
echo 'export PATH="$HOME/.local/share/pnpm:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

### 🔴 `ERR_PNPM_UNSUPPORTED_ENGINE`

Tu versión de Node.js es muy vieja. Actualizala a 18 LTS o superior.

```bash
node --version
# Si es < 18, descargá la última LTS de nodejs.org
```

### 🔴 Error de conexión al instalar dependencias

El firewall está bloqueando el registry. Probá:

```bash
# 1. Configurar proxy (si estás en la UTN)
pnpm config set proxy http://proxy.frtn.utn.edu.ar:8080
pnpm config set https-proxy http://proxy.frtn.utn.edu.ar:8080

# 2. O usar un mirror (alternativa al registry oficial)
pnpm config set registry https://registry.npmmirror.com

# 3. O desactivar SSL (NO RECOMENDADO, solo como último recurso)
pnpm config set strict-ssl false
```

### 🔴 EACCES: permission denied

Problema de permisos al instalar pnpm globalmente con corepack.

```bash
# En Linux/Mac: no uses sudo con pnpm. En su lugar:
# Configurá el prefix de Node.js para tu usuario
mkdir -p ~/.npm-global
pnpm config set prefix ~/.npm-global
export PATH="$HOME/.npm-global/bin:$PATH"
```

### 🔴 `port 3000 already in use`

Otro proceso está usando el puerto 3000.

```bash
# Encontrar el proceso
lsof -i :3000

# Matarlo (reemplazar PID con el número que muestra lsof)
kill -9 <PID>

# O cambiá el puerto en src/index.ts a 3001
```

### 🔴 Swagger UI no muestra las rutas (paths vacíos)

El spec OpenAPI aparece con `"paths": {}` vacío.

```bash
# Causa más común: falta el await en app.register(fastifySwagger, ...)
# Sin await, Fastify no termina de procesar el plugin antes de que
# las rutas se registren, y Swagger no las detecta.
#
# Solución: asegurate de que el registro del plugin tenga await:
await app.register(fastifySwagger, { ... });   # ← necesario
# app.register(fastifySwagger, { ... });        # ← sin await, falla
```

Los plugins de Fastify que necesitan interceptar el registro de rutas (como Swagger) **requieren `await`** para funcionar correctamente.

### 🔴 `ERR_MODULE_NOT_FOUND`

Hay un problema con la resolución de módulos. Verificá que:

```bash
# 1. package.json tenga "type": "module"
grep '"type"' package.json

# 2. tsconfig.json tenga "module": "NodeNext"
grep '"module"' tsconfig.json

# 3. Las dependencias estén instaladas
ls node_modules/fastify
```

---

## Resumen Visual del Proceso

```
1. corepack enable && corepack prepare pnpm@latest --activate
                    │
2. mkdir -p fastify-hello/src && cd fastify-hello
                    │
3. pnpm init        ───→ package.json
                    │
4. Crear archivos:  ───→ tsconfig.json, .npmrc, src/index.ts
                    │
5. pnpm add fastify @fastify/swagger @fastify/swagger-ui
   pnpm add -D typescript @types/node tsx
                    │
6. Editar package.json  ───→ scripts: dev, start, typecheck, clean
                    │
7. pnpm dev          ───→ Servidor corriendo en http://localhost:3000
                    │
8. curl localhost:3000  ───→ {"message":"¡Hola, mundo desde Fastify!"}
                    │
9. http://localhost:3000/docs  ───→ Swagger UI interactiva
```

---

> **📌 Para el estudiante**: Esta guía la vas a usar UNA SOLA VEZ para el primer proyecto. Después, todo el proceso se reduce a 3 pasos: `pnpm install`, `pnpm dev`, código. Pero entender el setup desde cero te da el poder de **no depender de nadie para arrancar un proyecto** — ni de un template, ni de un CLI, ni de una IDE. Eso es ser Ingeniero.

> **📌 Para el profe**: Si encontrás errores o querés agregar la configuración exacta del proxy de la UTN FRLP, actualizá la [sección 3](#3-configurar-pnpm-para-el-entorno-corporativo) y mandá PR. Esta guía vive donde el código — cualquiera puede mejorarla.
