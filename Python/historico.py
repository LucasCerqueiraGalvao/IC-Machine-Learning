import os
from yahooquery import Ticker
import pandas as pd
import warnings

# Suprimir avisos futuros que não impactam a execução
warnings.simplefilter(action='ignore', category=FutureWarning)
warnings.simplefilter(action='ignore', category=DeprecationWarning)

# Definir o símbolo do ticker
ticker_symbol = 'PETR4.SA'

# Criar uma instância do objeto Ticker
ticker = Ticker(ticker_symbol)

# Obter o histórico de preços máximo disponível
history_data = ticker.history(period='max').reset_index()

# Definir o caminho e o nome do arquivo
caminho = r'C:\Users\Lenovo\Documents\Obsidian\IC-Machine-Learning\Planilhas'
nome_arquivo = 'history_PETR4_2024.09.17.csv'
caminho_completo = os.path.join(caminho, nome_arquivo)

# Verificar se o diretório existe; caso contrário, criar
os.makedirs(caminho, exist_ok=True)

# Salvar o DataFrame em um arquivo CSV
history_data.to_csv(caminho_completo, index=False, encoding='utf-8')

print(f'Histórico de preços salvo com sucesso em {caminho_completo}')
