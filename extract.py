import yfinance as yf
import pandas as pd

commodities = ['CL=F', 'GC=F', 'SI=F'] # Petroleo Bruto, Ouro, Prata

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
    concatena todos od precos das ações
    """
    todos_dados = []
    for simbolo in commodities:
        dados_de_commodities = buscar_dados_comodities(simbolo)
        todos_dados.append(dados_de_commodities)
    return pd.concat(todos_dados)

if __name__ == "__main__":
    buscar_de_todas_as_commodities = buscar_todos_dados_comodities(commodities)
    