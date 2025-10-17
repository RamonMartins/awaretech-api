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
                    data_criacao TIMESTAMP NOT NULL
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


##### Rota RECEBER última leitura Sensor de vibração 
@app.get("/ultimo_sensor_vibracao")
def ultimo_vibracao():
    return aux_ultima_leitura(tab_sensor_vibracao)

##### Rota RECEBER histórico Sensor de vibração
@app.get("/historico_sensor_vibracao")
def historico_vibracao():
    return aux_historico(tab_sensor_vibracao)


##### Rota RECEBER última leitura Sensor de corrente 1
@app.get("/ultimo_sensor_corrente_1")
def ultimo_corrente_1():
    return aux_ultima_leitura(tab_sensor_corrente_1)

##### Rota RECEBER histórico Sensor de corrente 1
@app.get("/historico_sensor_corrente_1")
def historico_corrente_1():
    return aux_historico(tab_sensor_corrente_1)


##### Rota RECEBER última leitura Sensor de corrente 2
@app.get("/ultimo_sensor_corrente_2")
def ultimo_corrente_2():
    return aux_ultima_leitura(tab_sensor_corrente_2)

##### Rota RECEBER histórico Sensor de corrente 2
@app.get("/historico_sensor_corrente_2")
def historico_corrente_2():
    return aux_historico(tab_sensor_corrente_2)


##### Rota RECEBER última leitura Sensor de corrente 3
@app.get("/ultimo_sensor_corrente_3")
def ultimo_corrente_3():
    return aux_ultima_leitura(tab_sensor_corrente_3)

##### Rota RECEBER histórico Sensor de corrente 3
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
                    (payload.leitura_sensor, datetime.now())
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


######### Rotas DELETE #########

# Função auxiliar para limpar tabela
def aux_limpar_tabela(tabela: str):
    try:
        with psycopg2.connect(DATABASE_URL, sslmode='require', cursor_factory=RealDictCursor) as conn:
            with conn.cursor() as cur:
                cur.execute(f"TRUNCATE TABLE {tabela} RESTART IDENTITY")
                conn.commit()
        return {"status": "ok", "mensagem": f"Tabela {tabela} limpa com sucesso"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


##### Rota LIMPAR Sensor de vibração
@app.delete("/limpar_sensor_vibracao")
def limpar_vibracao():
    return aux_limpar_tabela(tab_sensor_vibracao)

##### Rota LIMPAR Sensor de corrente 1
@app.delete("/limpar_sensor_corrente_1")
def limpar_corrente_1():
    return aux_limpar_tabela(tab_sensor_corrente_1)

##### Rota LIMPAR Sensor de corrente 2
@app.delete("/limpar_sensor_corrente_2")
def limpar_corrente_2():
    return aux_limpar_tabela(tab_sensor_corrente_2)

##### Rota LIMPAR Sensor de corrente 3
@app.delete("/limpar_sensor_corrente_3")
def limpar_corrente_3():
    return aux_limpar_tabela(tab_sensor_corrente_3)

##### Rota LIMPAR todas as tabelas
@app.delete("/limpar_todas_tabelas")
def limpar_todas_tabelas():
    tabelas = [
        tab_sensor_vibracao,
        tab_sensor_corrente_1,
        tab_sensor_corrente_2,
        tab_sensor_corrente_3
    ]
    resultados = {}
    for tabela in tabelas:
        try:
            resultados[tabela] = aux_limpar_tabela(tabela)
        except HTTPException as e:
            resultados[tabela] = {"status": "erro", "mensagem": str(e.detail)}
    return resultados

##### Rota para EXCLUIR todas as tabelas
@app.delete("/excluir_todas_tabelas")
def excluir_todas_tabelas():
    tabelas = [
        tab_sensor_vibracao,
        tab_sensor_corrente_1,
        tab_sensor_corrente_2,
        tab_sensor_corrente_3
    ]
    
    resultados = {}
    try:
        with psycopg2.connect(DATABASE_URL, sslmode='require') as conn:
            with conn.cursor() as cur:
                for tabela in tabelas:
                    try:
                        cur.execute(f"DROP TABLE IF EXISTS {tabela}")
                        resultados[tabela] = {"status": "ok", "mensagem": "Tabela excluída com sucesso"}
                    except Exception as e:
                        resultados[tabela] = {"status": "erro", "mensagem": str(e)}
                conn.commit()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao conectar ao banco: {e}")

    return resultados


# 🔹 Bloco para rodar corretamente no Railway
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))  # Railway define a porta automaticamente
    uvicorn.run("main:app", host="0.0.0.0", port=port)

