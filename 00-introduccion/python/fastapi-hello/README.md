# 🐍 FastAPI — Hola Mundo

> **Materia**: Desarrollo de Software — Backend  
> **Framework**: FastAPI (Python 3.12+)

Ejemplo mínimo de API REST con FastAPI, documentación Swagger automática y health check.

---

## ⚙️ Requisitos

- Python 3.12 o superior
- pip (o pip3)

> ⚠️ Si el firewall Fortigate bloquea pip, configurá el proxy:
> ```bash
> pip install -r requirements.txt --proxy http://proxy.frtn.utn.edu.ar:8080
> ```

---

## 🚀 Cómo ejecutar

```bash
# 1. Entrar al directorio
cd 00-introduccion/python/fastapi-hello

# 2. (Recomendado) Crear y activar virtualenv
python -m venv .venv
source .venv/bin/activate    # Linux/Mac
# .venv\Scripts\activate     # Windows

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Iniciar servidor (con hot-reload)
uvicorn main:app --reload --port 8000
```

---

## 🔗 Endpoints

| Método | Ruta | Descripción |
|--------|------|-------------|
| `GET` | `/` | Mensaje de bienvenida |
| `GET` | `/health` | Health check del servicio |

### Probar con curl

```bash
curl http://localhost:8000/
# → {"message":"¡Hola, mundo desde FastAPI!"}

curl http://localhost:8000/health
# → {"status":"ok","service":"fastapi-hello"}
```

---

## 📖 Documentación interactiva

Con el servidor corriendo, abrí en el navegador:

| Herramienta | URL |
|-------------|-----|
| **Swagger UI** | http://localhost:8000/docs |
| **ReDoc** | http://localhost:8000/redoc |
| **OpenAPI spec (JSON)** | http://localhost:8000/openapi.json |

FastAPI genera **Swagger UI y ReDoc automáticamente**, sin necesidad de plugins adicionales.

---

## 📁 Estructura

```
fastapi-hello/
├── main.py              # Código del servidor
├── requirements.txt     # Dependencias
├── NOTAS_ACADEMICAS.md  # Material de estudio completo
└── README.md            # Esta guía rápida
```

---

## 📚 Más información

- [Documentación oficial de FastAPI](https://fastapi.tiangolo.com/)
- [Notas académicas](./NOTAS_ACADEMICAS.md) — explicación conceptual detallada
