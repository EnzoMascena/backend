-- ============================================================
-- Esquema de la base de datos — Módulo 02: Persistencia
-- ============================================================
-- Este archivo define la ESTRUCTURA de los datos (el "molde").
-- PostgreSQL lo ejecuta UNA sola vez por proyecto.
--
-- ¿Por qué "IF NOT EXISTS"?
-- Para poder ejecutarlo varias veces sin que rompa.
-- Así es IDEMPOTENTE: si la tabla ya existe, no hace nada.
--
-- ¿Cómo se ejecuta?
--   Docker (demo):  docker exec -i pg-clase02 psql -U postgres < schema.sql
--   Supabase:       SQL Editor del dashboard → pegar el contenido → Run
-- ============================================================

CREATE TABLE IF NOT EXISTS tasks (
    -- id: número único por fila. IDENTITY = PostgreSQL elige el
    -- próximo número automáticamente (1, 2, 3...). Es la clave
    -- primaria (PRIMARY KEY): identifica a la tarea sin ambigüedad.
    id          INTEGER     GENERATED ALWAYS AS IDENTITY PRIMARY KEY,

    -- title: el texto de la tarea. NOT NULL = no puede faltar.
    -- TEXT permite cualquier longitud (la validación de 1..200
    -- caracteres la hace Pydantic en la API, como en el Módulo 01).
    title       TEXT        NOT NULL,

    -- completed: estado de la tarea. DEFAULT FALSE = al crear,
    -- una tarea arranca sin completar. No hace falta decir
    -- "completed: false" en el INSERT: la base lo decide sola.
    completed   BOOLEAN     NOT NULL DEFAULT FALSE,

    -- created_at: cuándo se creó. TIMESTAMPTZ = timestamp CON zona
    -- horaria (la "T" de postgres + "Z" de UTC).
    -- DEFAULT NOW() = la base pone la fecha, no el código Python.
    -- ¿Quién genera el dato? LA FUENTE DE VERDAD: la base.
    created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
