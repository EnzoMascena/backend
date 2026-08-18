"""
Paquete principal de la aplicación — Módulo 03: Arquitectura en Capas.

La MISMA API de Tareas de los módulos 01 y 02, pero organizada en tres
capas con responsabilidades separadas:

    Controller ──► Service ──► Repository ──► PostgreSQL
      (HTTP)        (negocio)     (ORM/SQL)

Cada carpeta de este paquete es UNA capa. La regla de dependencia es
estricta: una capa solo conoce a la que está DEBAJO, nunca hacia arriba
ni en diagonal.
"""
