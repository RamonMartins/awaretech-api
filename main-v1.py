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

# Cria tabela sensor_corrente_2
cur.execute("""
CREATE TABLE IF NOT EXISTS sensor_corrente_2 (
    id SERIAL PRIMARY KEY,
    leitura FLOAT NOT NULL,
    data_criacao TIMESTAMP NOT NULL
)
""")
conn.commit()

# Cria tabela sensor_corrente_3
cur.execute("""
CREATE TABLE IF NOT EXISTS sensor_corrente_3 (
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

######################### Requisições POST #############################

# Enviar Sensor de vibração
@app.post("/enviar_sensor_vibracao")
def enviar_vibracao(payload: Dados):
    try:
        cur.execute(
            "INSERT INTO sensor_vibracao (leitura, data_criacao) VALUES (%s, %s)",
            (payload.leitura_sensor, datetime.now())
        )
        conn.commit()
        return {"status": "ok"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Enviar Sensor de corrente 1
@app.post("/enviar_sensor_corrente_1")
def enviar_corrente_1(payload: Dados):
    try:
        cur.execute(
            "INSERT INTO sensor_corrente_1 (leitura, data_criacao) VALUES (%s, %s)",
            (payload.leitura_sensor, datetime.now())
        )
        conn.commit()
        return {"status": "ok"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Enviar Sensor de corrente 2
@app.post("/enviar_sensor_corrente_2")
def enviar_corrente_2(payload: Dados):
    try:
        cur.execute(
            "INSERT INTO sensor_corrente_2 (leitura, data_criacao) VALUES (%s, %s)",
            (payload.leitura_sensor, datetime.now())
        )
        conn.commit()
        return {"status": "ok"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Enviar Sensor de corrente 3
@app.post("/enviar_sensor_corrente_3")
def enviar_corrente_3(payload: Dados):
    try:
        cur.execute(
            "INSERT INTO sensor_corrente_3 (leitura, data_criacao) VALUES (%s, %s)",
            (payload.leitura_sensor, datetime.now())
        )
        conn.commit()
        return {"status": "ok"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

######################### Requisições GET #############################

# Retornar última leitura do Sensor de vibração
@app.get("/ultimo_sensor_vibracao")
def ultimo_vibracao():
    try:
        cur.execute("SELECT * FROM sensor_vibracao ORDER BY id DESC LIMIT 1")
        payload = cur.fetchall()
        return payload
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Retornar histórico do Sensor de vibração (últimas 50 leituras)
@app.get("/historico_sensor_vibracao")
def historico_vibracao():
    try:
        cur.execute("SELECT * FROM sensor_vibracao ORDER BY id DESC LIMIT 50")
        payload = cur.fetchall()
        return payload
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Retornar última leitura do Sensor de corrente 1
@app.get("/ultimo_sensor_corrente_1")
def ultimo_corrente_1():
    try:
        cur.execute("SELECT * FROM sensor_corrente_1 ORDER BY id DESC LIMIT 1")
        payload = cur.fetchall()
        return payload
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Retornar histórico do Sensor de corrente 1 (últimas 50 leituras)
@app.get("/historico_sensor_corrente_1")
def historico_corrente_1():
    try:
        cur.execute("SELECT * FROM sensor_corrente_1 ORDER BY id DESC LIMIT 50")
        payload = cur.fetchall()
        return payload
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Retornar última leitura do Sensor de corrente 2
@app.get("/ultimo_sensor_corrente_2")
def ultimo_corrente_2():
    try:
        cur.execute("SELECT * FROM sensor_corrente_2 ORDER BY id DESC LIMIT 1")
        payload = cur.fetchall()
        return payload
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Retornar histórico do Sensor de corrente 2 (últimas 50 leituras)
@app.get("/historico_sensor_corrente_2")
def historico_corrente_2():
    try:
        cur.execute("SELECT * FROM sensor_corrente_2 ORDER BY id DESC LIMIT 50")
        payload = cur.fetchall()
        return payload
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Retornar última leitura do Sensor de corrente 3
@app.get("/ultimo_sensor_corrente_3")
def ultimo_corrente_3():
    try:
        cur.execute("SELECT * FROM sensor_corrente_3 ORDER BY id DESC LIMIT 1")
        payload = cur.fetchall()
        return payload
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Retornar histórico do Sensor de corrente 3 (últimas 50 leituras)
@app.get("/historico_sensor_corrente_3")
def historico_corrente_3():
    try:
        cur.execute("SELECT * FROM sensor_corrente_3 ORDER BY id DESC LIMIT 50")
        payload = cur.fetchall()
        return payload
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# 🔹 Bloco para rodar corretamente no Railway
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))  # Railway define a porta automaticamente
    uvicorn.run("main:app", host="0.0.0.0", port=port)

