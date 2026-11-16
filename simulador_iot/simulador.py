"""Simula un dispositivo IoT que inserta métricas de salud en MongoDB.

Uso: python simulador.py <paciente_id>
"""
import os
import random
import sys
import time
from datetime import datetime, timezone

from pymongo import MongoClient

MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27018")
SEGUNDOS_ENTRE_METRICAS = 2
RANGOS = {
    "pulso": (55, 130),
    "presion_sistolica": (100, 160),
    "presion_diastolica": (60, 100),
}


def generar_metrica(paciente_id: int) -> dict:
    tipo = random.choice(list(RANGOS))
    minimo, maximo = RANGOS[tipo]
    return {
        "paciente_id": paciente_id,
        "tipo": tipo,
        "valor": round(random.uniform(minimo, maximo), 1),
        "timestamp": datetime.now(timezone.utc),
    }


def main() -> None:
    paciente_id = int(sys.argv[1])
    metricas = MongoClient(MONGO_URL)["sgmedica"]["metricas_salud"]
    while True:
        metrica = generar_metrica(paciente_id)
        print(f"Paciente {paciente_id}: {metrica['tipo']} = {metrica['valor']}", flush=True)
        metricas.insert_one(metrica)
        time.sleep(SEGUNDOS_ENTRE_METRICAS)


if __name__ == "__main__":
    main()
