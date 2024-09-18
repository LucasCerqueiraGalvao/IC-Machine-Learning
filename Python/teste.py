import os
from yahooquery import Ticker
import pandas as pd
import warnings

ticker_symbol = 'PETR4.SA'

# Criar uma instância do objeto Ticker
ticker = Ticker(ticker_symbol)

print (ticker)
