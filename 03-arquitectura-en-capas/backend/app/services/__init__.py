"""
Capa de negocio (Service) — las reglas del dominio.

Acá viven los casos de uso: qué se puede hacer con una tarea y cómo.
El service NO sabe de HTTP (no importa FastAPI ni conoce status codes)
y NO sabe de SQL (no toca la base): le pide al repository lo que
necesita.
"""
