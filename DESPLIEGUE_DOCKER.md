# Despliegue en Docker

Todo SGMEDICA se levanta con un solo comando.

## Contenedores

| Servicio | Imagen | Puerto | Función |
|---|---|---|---|
| `postgres` | `postgres:16` | 5432 | Usuarios, citas y expedientes |
| `mongo` | `mongo:7` | 27018 | Métricas IoT |
| `redis` | `redis:7` | 6379 | Canal de métricas |
| `backend` | `backend/Dockerfile` | 8000 | API REST y GraphQL |
| `alertas` | `alertas/Dockerfile` | 8001 | Alertas y WebSocket |
| `frontend` | `frontend/Dockerfile` | 5173 | Interfaz en React |

## Cómo se hizo

- **Un `Dockerfile` por servicio propio:** instala las dependencias, copia el código y arranca el servidor.
- **Red interna:** dentro de Docker cada contenedor se alcanza por su nombre. Por eso el backend se conecta a `postgres` y no a `localhost`.
- **Variables de entorno:** `docker-compose.yml` les pasa a los servicios las direcciones de las bases
- **Orden de arranque:** el backend espera a que PostgreSQL esté listo (`healthcheck`).
- **Volúmenes:** los datos de PostgreSQL y MongoDB no se pierden al apagar los contenedores.

## Comandos

```bash
cp .env.example .env
docker compose up -d --build
docker compose ps
docker compose down
```

El simulador se corre aparte, porque recibe el id del paciente:

```bash
backend/.venv/Scripts/python simulador_iot/simulador.py <paciente_id>
```

## Verificación

Con todo en contenedores se probó el registro y login, la consulta GraphQL con métricas de MongoDB, las alertas en tiempo real por Redis y WebSocket, y el frontend.
