"""
Capa de datos (Repository) — el acceso a la base.

La ÚNICA capa que habla con la base a través del ORM. Acá viven las
consultas (listar, crear, actualizar, borrar). Nada de HTTP, nada de
reglas de negocio: solo leer y escribir la entidad Task.
"""
