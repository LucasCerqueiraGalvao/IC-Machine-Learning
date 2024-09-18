import os
from yahooquery import Ticker
import pandas as pd
import warnings

# Suprimir avisos futuros
warnings.simplefilter(action='ignore', category=FutureWarning)

# Definir o símbolo do ticker
ticker_symbol = 'PETR4.SA'

# Criar uma instância do objeto Ticker
ticker = Ticker(ticker_symbol)

# Criar um dicionário para armazenar os dados
dados = {}

# Informações gerais
dados['price'] = ticker.price
dados['summary_detail'] = ticker.summary_detail
dados['financial_data'] = ticker.financial_data
dados['quote_type'] = ticker.quote_type
dados['key_stats'] = ticker.key_stats
dados['summary_profile'] = ticker.summary_profile
dados['calendar_events'] = ticker.calendar_events
dados['esg_scores'] = ticker.esg_scores
dados['asset_profile'] = ticker.asset_profile

# Dados financeiros
dados['income_statement'] = ticker.income_statement()
dados['balance_sheet'] = ticker.balance_sheet()
dados['cash_flow'] = ticker.cash_flow()
dados['financials'] = ticker.all_financial_data()

# Histórico de preços
history_data = ticker.history(period='max').reset_index()
dados['history'] = history_data

# Dividendos e Splits
if 'dividends' in history_data.columns:
    dados['dividends'] = history_data[['date', 'dividends']][history_data['dividends'] != 0]
else:
    dados['dividends'] = pd.DataFrame(columns=['date', 'dividends'])

if 'splits' in history_data.columns:
    dados['splits'] = history_data[['date', 'splits']][history_data['splits'] != 0]
else:
    dados['splits'] = pd.DataFrame(columns=['date', 'splits'])

# Recomendações de analistas
try:
    dados['recommendation_trend'] = ticker.recommendation_trend
except AttributeError:
    dados['recommendation_trend'] = pd.DataFrame()

try:
    dados['analyst_trend_details'] = ticker.analyst_trend_details
except AttributeError:
    dados['analyst_trend_details'] = pd.DataFrame()

try:
    dados['recommendations'] = ticker.recommendations
except AttributeError:
    dados['recommendations'] = pd.DataFrame()

# Notícias
try:
    dados['news'] = ticker.news()
except AttributeError:
    dados['news'] = pd.DataFrame()

# Definir o caminho e o nome do arquivo
caminho = r'C:\Users\Lenovo\Documents\Obsidian\IC-Machine-Learning\Planilhas'
nome_arquivo = 'dados_PETR4_2024.09.17.xlsx'
caminho_completo = os.path.join(caminho, nome_arquivo)

# Verificar se o diretório existe; caso contrário, criar
if not os.path.exists(caminho):
    os.makedirs(caminho)

# Criar um objeto ExcelWriter para salvar múltiplos DataFrames em diferentes abas
with pd.ExcelWriter(caminho_completo, engine='xlsxwriter') as writer:
    for chave, valor in dados.items():
        # Verificar o tipo de dado e converter para DataFrame
        if isinstance(valor, pd.DataFrame):
            df = valor
        elif isinstance(valor, dict):
            df = pd.DataFrame.from_dict(valor, orient='index')
        elif isinstance(valor, list):
            df = pd.DataFrame(valor)
        else:
            df = pd.DataFrame([valor])

        # Resetar o índice para melhor visualização
        df.reset_index(inplace=True, drop=True)

        # Remover timezone das colunas datetime
        for col in df.columns:
            if pd.api.types.is_datetime64tz_dtype(df[col]):
                df[col] = df[col].dt.tz_localize(None)

        # Remover caracteres inválidos do nome da aba
        nome_aba = chave[:31]  # Limite de 31 caracteres para nomes de abas no Excel

        # Salvar o DataFrame na aba correspondente
        df.to_excel(writer, sheet_name=nome_aba, index=False)

print(f'Dados salvos com sucesso em {caminho_completo}')
