#%%
import os
import yfinance as yf
import pandas as pd

# Definir o símbolo do ticker
ticker_symbol = 'PETR4.SA'

# Obter o histórico de preços usando yfinance
ticker = yf.Ticker(ticker_symbol)
history_data = ticker.history(period='max').reset_index()

# Verificar os dados
print(history_data.head())

# Converter colunas numéricas para float
numeric_columns = ['Open', 'High', 'Low', 'Close', 'Volume', 'Dividends', 'Stock Splits']
history_data[numeric_columns] = history_data[numeric_columns].astype(float)

# Definir o caminho e o nome do arquivo
caminho = r'C:\Users\Lenovo\Documents\Obsidian\IC-Machine-Learning\Planilhas'
nome_arquivo = 'history_PETR4_2024.09.17.csv'
caminho_completo = os.path.join(caminho, nome_arquivo)

# Criar o diretório, se não existir
os.makedirs(caminho, exist_ok=True)

# Salvar o DataFrame em um arquivo CSV com separadores apropriados
history_data.to_csv(caminho_completo, index=False, sep=';', decimal=',', encoding='utf-8')

print(f'Histórico de preços salvo com sucesso em {caminho_completo}')

#%%

# Carregar o CSV recém-criado
df = pd.read_csv(caminho_completo, sep=';', decimal=',')

# Ajustar a coluna de datas (primeira coluna) para manter apenas a parte antes do espaço
df['Date'] = df['Date'].str.split(' ').str[0]

# Definir o novo caminho para salvar o arquivo Excel
nome_arquivo_excel = 'history_PETR4_2024.09.17.xlsx'
caminho_excel = os.path.join(caminho, nome_arquivo_excel)

# Salvar o DataFrame ajustado em formato Excel
df.to_excel(caminho_excel, index=False)

# Apagar o arquivo CSV original
if os.path.exists(caminho_completo):
    os.remove(caminho_completo)
    print(f'Arquivo CSV {caminho_completo} foi excluído.')

# Confirmar que o Excel foi salvo
print(f'DataFrame ajustado e salvo como Excel em {caminho_excel}')

#%%





