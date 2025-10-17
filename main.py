from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime
import os
import psycopg2
from psycopg2.extras import RealDictCursor
from zoneinfo import ZoneInfo

app = FastAPI(title="API ESP32 FastAPI + PostgreSQL")

# Variável de ambiente que o Railway já cria
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL não encontrada nas variáveis de ambiente!")


###################### Criação das tabelas ######################

# Nome das tabelas
tab_sensor_vibracao = "sensor_vibracao"
tab_sensor_corrente_1 = "sensor_corrente_1"
tab_sensor_corrente_2 = "sensor_corrente_2"
tab_sensor_corrente_3 = "sensor_corrente_3"

# Função auxiliar para criar as tabelas
def aux_criar_tabela(tabela: str):
    try:
        with psycopg2.connect(DATABASE_URL, sslmode='require') as conn:
            with conn.cursor() as cur:
                cur.execute(f"""
                CREATE TABLE IF NOT EXISTS {tabela} (
                    id SERIAL PRIMARY KEY,
                    leitura FLOAT NOT NULL,
                    data_criacao TIMESTAMP WITH TIME ZONE NOT NULL
                )
                """)
                conn.commit()
    except Exception as e:
        raise RuntimeError(f"Erro ao criar tabela {tabela}: {e}")


# Chamadas para criar as tabelas
aux_criar_tabela(tab_sensor_vibracao)
aux_criar_tabela(tab_sensor_corrente_1)
aux_criar_tabela(tab_sensor_corrente_2)
aux_criar_tabela(tab_sensor_corrente_3)


###################### Criação de Rotas ######################

##### Rota raiz
@app.get("/")
def raiz():
    return {"mensagem": "API do ESP32 está online 🚀"}


######### Rotas GET #########

# Função auxiliar para retornar última leitura do Sensor
def aux_ultima_leitura(tabela: str):
    try:
        # Conexão com PostgreSQL
        with psycopg2.connect(DATABASE_URL, sslmode='require', cursor_factory=RealDictCursor) as conn:
            with conn.cursor() as cur:
                # Buscar dados
                cur.execute(f"SELECT * FROM {tabela} ORDER BY id DESC LIMIT 1")
                payload = cur.fetchone()
                if payload is None:
                    return {"mensagem": "nenhum dado encontrado"}
                else:
                    return payload
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Função auxiliar para retornar histórico do Sensor (últimas 50 leituras)
def aux_historico(tabela: str):
    try:
        # Conexão com PostgreSQL
        with psycopg2.connect(DATABASE_URL, sslmode='require', cursor_factory=RealDictCursor) as conn:
            with conn.cursor() as cur:
                # Buscar dados
                cur.execute(f"SELECT * FROM {tabela} ORDER BY id DESC LIMIT 50")
                payload = cur.fetchall()
                if not payload:
                    return {"mensagem": "nenhum dado encontrado"}
                else:
                    return payload
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


##### Rota receber última leitura Sensor de vibração 
@app.get("/ultimo_sensor_vibracao")
def ultimo_vibracao():
    return aux_ultima_leitura(tab_sensor_vibracao)

##### Rota receber histórico Sensor de vibração
@app.get("/historico_sensor_vibracao")
def historico_vibracao():
    return aux_historico(tab_sensor_vibracao)


##### Rota receber última leitura Sensor de corrente 1
@app.get("/ultimo_sensor_corrente_1")
def ultimo_corrente_1():
    return aux_ultima_leitura(tab_sensor_corrente_1)

##### Rota receber histórico Sensor de corrente 1
@app.get("/historico_sensor_corrente_1")
def historico_corrente_1():
    return aux_historico(tab_sensor_corrente_1)


##### Rota receber última leitura Sensor de corrente 2
@app.get("/ultimo_sensor_corrente_2")
def ultimo_corrente_2():
    return aux_ultima_leitura(tab_sensor_corrente_2)

##### Rota receber histórico Sensor de corrente 2
@app.get("/historico_sensor_corrente_2")
def historico_corrente_2():
    return aux_historico(tab_sensor_corrente_2)


##### Rota receber última leitura Sensor de corrente 3
@app.get("/ultimo_sensor_corrente_3")
def ultimo_corrente_3():
    return aux_ultima_leitura(tab_sensor_corrente_3)

##### Rota receber histórico Sensor de corrente 3
@app.get("/historico_sensor_corrente_3")
def historico_corrente_3():
    return aux_historico(tab_sensor_corrente_3)


######### Rotas POST #########

# Modelo de dados do ESP32
class Dados(BaseModel):
    leitura_sensor: float

# Função auxiliar para envio de leituras
def aux_enviar_leitura(tabela: str, payload: Dados):
    try:
        # Conexão com PostgreSQL
        with psycopg2.connect(DATABASE_URL, sslmode='require', cursor_factory=RealDictCursor) as conn:
            with conn.cursor() as cur:
                # Gravar os dados
                cur.execute(
                    f"INSERT INTO {tabela} (leitura, data_criacao) VALUES (%s, %s)",
                    (payload.leitura_sensor, datetime.now(ZoneInfo("America/Sao_Paulo")))
                )
                conn.commit()
        return {"status": "ok"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


##### Rota Enviar Sensor de vibração
@app.post("/enviar_sensor_vibracao")
def enviar_vibracao(payload: Dados):
    return aux_enviar_leitura(tab_sensor_vibracao, payload)

##### Rota Enviar Sensor de corrente 1
@app.post("/enviar_sensor_corrente_1")
def enviar_corrente_1(payload: Dados):
    return aux_enviar_leitura(tab_sensor_corrente_1, payload)

##### Rota Enviar Sensor de corrente 2
@app.post("/enviar_sensor_corrente_2")
def enviar_corrente_2(payload: Dados):
    return aux_enviar_leitura(tab_sensor_corrente_2, payload)

##### Rota Enviar Sensor de corrente 3
@app.post("/enviar_sensor_corrente_3")
def enviar_corrente_3(payload: Dados):
    return aux_enviar_leitura(tab_sensor_corrente_3, payload)


# 🔹 Bloco para rodar corretamente no Railway
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))  # Railway define a porta automaticamente
    uvicorn.run("main:app", host="0.0.0.0", port=port)

