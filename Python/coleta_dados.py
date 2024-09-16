from yahooquery import Ticker
import pandas as pd

# Obtenção de dados do Yahoo Finance usando o YahooQuery.
petr = Ticker('PETR4.SA')

# Listar diferentes tipos de dados disponíveis para a PETR4
data = {
    'summary_detail': petr.summary_detail,
    'financial_data': petr.financial_data,
    'key_stats': petr.key_stats,
    'price': petr.price,
    'quote_type': petr.quote_type,
    'calendar_events': petr.calendar_events,
    'esg_scores': petr.esg_scores,
    'asset_profile': petr.asset_profile,
    'earnings': petr.earnings,
    'income_statement': petr.income_statement(),
    'balance_sheet': petr.balance_sheet(),
    'cash_flow': petr.cash_flow(),
    'recommendation_trend': petr.recommendation_trend,
    'insider_holders': petr.insider_holders,
    'insider_transactions': petr.insider_transactions,
    'major_holders': petr.major_holders,
    'institution_ownership': petr.institution_ownership,
    'fund_ownership': petr.fund_ownership  # Corrigido aqui
}

# Criando um ExcelWriter para salvar os dados em várias abas
with pd.ExcelWriter('petr_dados_completos.xlsx', engine='openpyxl') as writer:
    for key, df in data.items():
        if isinstance(df, dict):  # Alguns retornam dicionários
            df = pd.DataFrame([df])
        elif not isinstance(df, pd.DataFrame):  # Caso o formato não seja um DataFrame
            df = pd.DataFrame(df)
        df.to_excel(writer, sheet_name=key)

print("Dados salvos no arquivo petr_dados_completos.xlsx")
