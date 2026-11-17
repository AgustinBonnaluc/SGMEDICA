FROM python:3.11-slim

WORKDIR /codigo

# Las dependencias van primero: Docker las reutiliza si no cambian
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
