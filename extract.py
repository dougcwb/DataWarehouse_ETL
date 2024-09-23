import yfinance as yf
import pandas as pd
from faker import Faker
import csv
from datetime import date,timedelta
import random

fake = Faker()
quantidade_nomes = 50

commodities = ['CL=F', 'GC=F', 'SI=F'] # Petroleo Bruto, Ouro, Prata

def gerar_dados_comodities():
    """
    Gerar os preços das ações
    """

    movimentacao = [
        [
            fake.date_between(
                start_date=date.today() - timedelta(days=5), 
                end_date=date.today()).strftime('%Y-%m-%d'),    # date
            random.choice(commodities),                         # symbol
            random.choice(['Sell','Buy']),                      # action
            random.randrange(5, 50)                             # quantity
        ] for _ in range(quantidade_nomes)]

    with open("data/external/movimentacao_commodities.csv", "w", encoding="UTF-8", newline="") as csv_file:
        cabecalho = ['date','symbol','action','quantity']
        writer = csv.writer(csv_file, delimiter=',')
        writer.writerow(cabecalho)
        #writer = csv.DictWriter(csv_file, fieldnames=cabecalho)
        #writer.writeheader()

        #csv_writer = csv.writer(csv_file)
        writer.writerows(movimentacao)


def buscar_dados_comodities(simbolo,periodo='5d',intervalo='1d'):
    """
    Recebe parametro e retorna os preços das ações
    """
    ticker = yf.Ticker(simbolo)
    dados = ticker.history(period=periodo, interval=intervalo)
    dados['simbolo'] = simbolo
    return dados

def buscar_todos_dados_comodities(commodities):
    """
    concatena todos os precos das ações
    """
    todos_dados = []
    for simbolo in commodities:
        dados_de_commodities = buscar_dados_comodities(simbolo)
        todos_dados.append(dados_de_commodities)
    return pd.concat(todos_dados)

if __name__ == "__main__":
    gerar_dados_comodities()
    buscar_de_todas_as_commodities = buscar_todos_dados_comodities(commodities)
    
    print(buscar_de_todas_as_commodities)