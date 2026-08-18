/**
 * Tipos del contrato de la API.
 *
 * ESTE ARCHIVO ES LA LECCIÓN DE TYPESCRIPT:
 * refleja, en forma de tipos, el JSON que devuelve/recibe el backend.
 *
 *   Task       → lo que devuelve la API (id, title, completed, created_at)
 *   TaskCreate → lo que mandamos al crear (solo title)
 *   TaskUpdate → lo que mandamos al actualizar (campos opcionales)
 *
 * Antes (módulos 01/02) el frontend era JavaScript y confiábamos en
 * que el JSON tuviera la forma correcta. Ahora el compilador de
 * TypeScript VERIFICA que usemos bien cada campo. Si el backend cambia
 * el contrato, acá saltan los errores ANTES de ejecutar nada.
 */

export interface Task {
  id: number;
  title: string;
  completed: boolean;
  created_at: string;
}

export interface TaskCreate {
  title: string;
}

export interface TaskUpdate {
  title?: string;
  completed?: boolean;
}
