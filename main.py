from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime
import os
import psycopg2
from psycopg2.extras import RealDictCursor

app = FastAPI(title="API ESP32 FastAPI + PostgreSQL")

# Variável de ambiente que o Railway já cria
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL não encontrada nas variáveis de ambiente!")

# Conexão com PostgreSQL
try:
    conn = psycopg2.connect(DATABASE_URL, sslmode='require', cursor_factory=RealDictCursor)
    cur = conn.cursor()
except Exception as e:
    raise RuntimeError(f"Erro ao conectar ao banco: {e}")

# Criar tabela caso não exista
cur.execute("""
CREATE TABLE IF NOT EXISTS leituras (
    id SERIAL PRIMARY KEY,
    sensor1 FLOAT NOT NULL,
    sensor2 FLOAT NOT NULL,
    timestamp TIMESTAMP NOT NULL
)
""")
conn.commit()

# Modelo de dados do ESP32
class Dados(BaseModel):
    sensor1: float
    sensor2: float

# Rota raiz
@app.get("/")
def raiz():
    return {"mensagem": "API do ESP32 está online 🚀"}

# Receber dados do ESP32
@app.post("/dados")
def receber_dados(dados: Dados):
    try:
        cur.execute(
            "INSERT INTO leituras (sensor1, sensor2, timestamp) VALUES (%s, %s, %s)",
            (dados.sensor1, dados.sensor2, datetime.now())
        )
        conn.commit()
        return {"status": "ok"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Retornar histórico (últimas 50 leituras)
@app.get("/historico")
def listar_dados():
    try:
        cur.execute("SELECT * FROM leituras ORDER BY id DESC LIMIT 50")
        rows = cur.fetchall()
        return rows
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
