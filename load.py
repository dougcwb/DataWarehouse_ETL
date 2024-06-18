import pandas as pd
import sqlite3 as sql
import os 
from loguru import logger
import time

from transform import *
from extract import buscar_todos_dados_comodities

start_time = time.time()
logger.add("data/logs/file_{time}.log")
caminho_db = 'data/dw/commodities_dw.db'
caminho_arquivo = ('data/external/movimentacao_commodities.csv')
commodities = ['CL=F', 'GC=F', 'SI=F'] # Petroleo Bruto, Ouro, Prata

def cria_dw(df_integrado):
    os.makedirs('data/dw', exist_ok=True)
    conn = sql.connect(caminho_db)
    df_integrado.to_sql('commodities', conn, if_exists='replace', index=False)
    conn.close()
    print(f"Data Warehouse criado em {caminho_db}")


if __name__ == "__main__":
    dados_concatenados = buscar_todos_dados_comodities(commodities)
    dados_tratados = tratar_dados_extraidos(dados_concatenados)
    dados_movimentacao = processar_dados_movimentacao(caminho_arquivo)
    dados_finais = integrar_dados(dados_tratados, dados_movimentacao)
    logger.info(dados_finais)
    cria_dw(dados_finais)
    logger.info("--- %s seconds ---" % round((time.time() - start_time),2))