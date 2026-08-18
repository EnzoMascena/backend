"""
Capa de presentación (Controller) — los endpoints HTTP.

Acá viven las rutas de la API. El controller es un "traductor" entre
HTTP y la capa de negocio: recibe el request, delega en el service y
traduce el resultado a una respuesta HTTP (status codes, JSON).

Es la ÚNICA capa que conoce HTTP. No conoce SQL ni reglas de negocio.
"""
