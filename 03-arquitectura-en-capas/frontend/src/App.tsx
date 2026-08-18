import { useEffect, useState } from "react";
import "./App.css";
import type { Task } from "./types";
import { createTask, deleteTask, listTasks, updateTask } from "./api";

export default function App() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [title, setTitle] = useState("");
  const [editingId, setEditingId] = useState<number | null>(null);
  const [editingTitle, setEditingTitle] = useState("");
  const [error, setError] = useState<string | null>(null);

  async function load() {
    try {
      setTasks(await listTasks());
      setError(null);
    } catch {
      setError("No se pudo conectar con el backend");
    }
  }

  useEffect(() => {
    void load();
  }, []);

  async function handleSubmit(event: React.FormEvent) {
    event.preventDefault();
    const trimmed = title.trim();
    if (!trimmed) return;
    await createTask({ title: trimmed });
    setTitle("");
    await load();
  }

  async function handleToggle(task: Task) {
    await updateTask(task.id, { completed: !task.completed });
    await load();
  }

  async function handleDelete(id: number) {
    await deleteTask(id);
    await load();
  }

  function startEditing(task: Task) {
    setEditingId(task.id);
    setEditingTitle(task.title);
  }

  async function saveEdit(id: number) {
    const trimmed = editingTitle.trim();
    if (!trimmed) return;
    await updateTask(id, { title: trimmed });
    setEditingId(null);
    await load();
  }

  const completedCount = tasks.filter((task) => task.completed).length;

  return (
    <main className="app">
      <h1>Mis Tareas</h1>

      <form onSubmit={handleSubmit} className="new-task">
        <input
          value={title}
          onChange={(event) => setTitle(event.target.value)}
          placeholder="¿Qué hay que hacer?"
        />
        <button type="submit" disabled={!title.trim()}>
          Agregar
        </button>
      </form>

      {error && <p className="error">{error}</p>}

      {tasks.length === 0 && !error ? (
        <p className="empty">No hay tareas. ¡Agregá una!</p>
      ) : (
        <ul className="task-list">
          {tasks.map((task) => (
            <li key={task.id} className={task.completed ? "done" : ""}>
              <input
                type="checkbox"
                checked={task.completed}
                onChange={() => handleToggle(task)}
              />
              {editingId === task.id ? (
                <>
                  <input
                    className="edit-input"
                    value={editingTitle}
                    onChange={(event) => setEditingTitle(event.target.value)}
                    autoFocus
                  />
                  <button onClick={() => saveEdit(task.id)}>Guardar</button>
                </>
              ) : (
                <>
                  <span className="title">{task.title}</span>
                  <button onClick={() => startEditing(task)}>Editar</button>
                </>
              )}
              <button
                className="delete"
                aria-label="Eliminar"
                onClick={() => handleDelete(task.id)}
              >
                ×
              </button>
            </li>
          ))}
        </ul>
      )}

      <p className="counter">
        {completedCount} de {tasks.length} completadas
      </p>
    </main>
  );
}
