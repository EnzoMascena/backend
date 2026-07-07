/**
 * Módulo principal de la API Hola Mundo con Fastify.
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
 *   $ pnpm run dev       # Desarrollo con hot-reload (tsx watch)
 *   $ pnpm start         # Producción
 */

import Fastify from "fastify";

// ---------------------------------------------------------------------------
// Instancia de la aplicación
// ---------------------------------------------------------------------------
// Fastify() recibe un objeto de configuración.
// El logger está habilitado: usa Pino por debajo, produce logs JSON
// estructurados ideales para producción.
const app = Fastify({
  logger: true,
});

// ---------------------------------------------------------------------------
// Endpoint raíz
// ---------------------------------------------------------------------------
// .get() es el método para registrar una ruta GET.
// El primer parámetro es la ruta (path).
// El segundo es el manejador (handler), que puede ser async.
//
// Fastify infiere automáticamente:
//   - El tipo de retorno como JSON (objeto → Content-Type: application/json)
//   - Valida automáticamente si se define un schema JSON
//   - Serializa la respuesta con el serializador por defecto o custom
app.get("/", async () => {
  /**
   * Endpoint raíz.
   * Retorna un mensaje de bienvenida.
   *
   * Demuestra:
   * - Ruta GET más simple posible
   * - Retorno de objeto (Fastify lo serializa a JSON)
   * - Manejo async (incluso sin operaciones async, es buena práctica
   *   mantener consistencia para futuras modificaciones)
   */
  return { message: "¡Hola, mundo desde Fastify!" };
});

// ---------------------------------------------------------------------------
// Endpoint de salud
// ---------------------------------------------------------------------------
// Los health checks son un estándar en APIs productivas.
// Herramientas como Kubernetes, Docker y balanceadores de carga
// los usan para verificar disponibilidad del servicio.
app.get("/health", async () => {
  /**
   * Health check de la API.
   * Retorna el estado del servicio.
   *
   * Separar monitoreo de lógica de negocio es una buena práctica
   * de arquitectura.
   */
  return { status: "ok", service: "fastify-hello" };
});

// ---------------------------------------------------------------------------
// Inicio del servidor
// ---------------------------------------------------------------------------
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
