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
lst_commodities = ['CL=F', 'GC=F', 'SI=F'] # Petroleo Bruto, Ouro, Prata

def cria_dw(df_integrado):
    os.makedirs('data/dw', exist_ok=True)
    conn = sql.connect(caminho_db)
    df_integrado.to_sql('commodities', conn, if_exists='replace', index=False)
    conn.close()
    print(f"Data Warehouse criado em {caminho_db}")


if __name__ == "__main__":
    # Extract
    df_concatenados = buscar_todos_dados_comodities(lst_commodities)
    # Transform
    df_tratados = tratar_dados_extraidos(df_concatenados)
    df_movimentacao = processar_dados_movimentacao(caminho_arquivo)
    df_finais = integrar_dados(df_tratados, df_movimentacao)
    logger.info(df_finais)
    # Load
    cria_dw(df_finais)
    logger.info("--- %s seconds ---" % round((time.time() - start_time),2))