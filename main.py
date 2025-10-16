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

# Cria tabela sensor_vibracao
cur.execute("""
CREATE TABLE IF NOT EXISTS sensor_vibracao (
    id SERIAL PRIMARY KEY,
    leitura FLOAT NOT NULL,
    data_criacao TIMESTAMP NOT NULL
)
""")
conn.commit()

# Cria tabela sensor_corrente_1
cur.execute("""
CREATE TABLE IF NOT EXISTS sensor_corrente_1 (
    id SERIAL PRIMARY KEY,
    leitura FLOAT NOT NULL,
    data_criacao TIMESTAMP NOT NULL
)
""")
conn.commit()

# Modelo de dados do ESP32
class Dados(BaseModel):
    leitura_sensor: float

# Rota raiz
@app.get("/")
def raiz():
    return {"mensagem": "API do ESP32 está online 🚀"}


# Receber Sensor de vibração
@app.post("/enviar_sensor_vibracao")
def receber_vibracao(payload: Dados):
    try:
        cur.execute(
            "INSERT INTO sensor_vibracao (leitura, data_criacao) VALUES (%s, %s)",
            (payload.leitura_sensor, datetime.now())
        )
        conn.commit()
        return {"status": "ok"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Receber Sensor de corrente
@app.post("/enviar_sensor_corrente")
def receber_corrente(payload: Dados):
    try:
        cur.execute(
            "INSERT INTO sensor_corrente_1 (leitura, data_criacao) VALUES (%s, %s)",
            (payload.leitura_sensor, datetime.now())
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


# 🔹 Bloco para rodar corretamente no Railway
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))  # Railway define a porta automaticamente
    uvicorn.run("main:app", host="0.0.0.0", port=port)