/**
 * Capa de comunicación con la API (el "cliente HTTP").
 *
 * Acá viven las llamadas al backend. Cada función devuelve una Promise
 * TIPADA: `listTasks()` devuelve `Promise<Task[]>`, no "cualquier cosa".
 *
 * En el Módulo 01/02 esto era api.js sin tipos. Ahora TypeScript nos
 * garantiza que la respuesta tenga la forma que esperamos.
 */

import type { Task, TaskCreate, TaskUpdate } from "./types";

const BASE_URL = "/api/tasks";

/** Helper que hace el fetch y devuelve el JSON tipado. */
async function request<T>(url: string, options?: RequestInit): Promise<T> {
  const response = await fetch(url, options);
  if (!response.ok) {
    throw new Error(`Error ${response.status}`);
  }
  return (await response.json()) as T;
}

export function listTasks(): Promise<Task[]> {
  return request<Task[]>(BASE_URL);
}

export function getTask(id: number): Promise<Task> {
  return request<Task>(`${BASE_URL}/${id}`);
}

export function createTask(input: TaskCreate): Promise<Task> {
  return request<Task>(BASE_URL, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(input),
  });
}

export function updateTask(id: number, input: TaskUpdate): Promise<Task> {
  return request<Task>(`${BASE_URL}/${id}`, {
    method: "PATCH",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(input),
  });
}

export function deleteTask(id: number): Promise<{ ok: boolean }> {
  return request<{ ok: boolean }>(`${BASE_URL}/${id}`, {
    method: "DELETE",
  });
}
