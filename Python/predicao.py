import os  # Biblioteca para manipulação de diretórios e arquivos no sistema operacional
import pandas as pd  # Biblioteca para manipulação de dados em DataFrames
import numpy as np  # Biblioteca para operações matemáticas e manipulação de arrays
from sklearn.preprocessing import MinMaxScaler  # Função para normalizar dados entre 0 e 1
from sklearn.model_selection import train_test_split  # Função para dividir dados em treino e teste
from tensorflow.keras.models import Sequential  # Modelo sequencial do Keras para redes neurais
from tensorflow.keras.layers import SimpleRNN, LSTM, Dense  # Camadas de RNN, LSTM e densa (totalmente conectada) do Keras
import xgboost as xgb  # Biblioteca XGBoost para regressão com boosting de árvores
from sklearn.metrics import mean_squared_error  # Função de erro quadrático médio para avaliação do modelo
import matplotlib.pyplot as plt  # Biblioteca para visualização de dados (gráficos)
from datetime import datetime  # Biblioteca para manipulação de datas

# Lista de símbolos das ações que serão utilizadas como features e alvo (PETR4)
acoes = ['PETR3', 'PETR4', 'PRIO3', 'ENAT3', 'RRRP3', 'CSAN3', 'VBBR3', 'UGPA3']

# Definir o caminho relativo baseado no diretório atual
caminho_relativo = os.path.join(os.getcwd(), 'IC-Machine-Learning', 'Planilhas')

# Obter a data atual para o nome do arquivo
data_atual = datetime.today().strftime('%Y-%m-%d')

# Nome correto do arquivo Excel, que será acessado com base na data de criação
nome_arquivo_excel = f'{caminho_relativo}/historico_acoes_petroleo_{data_atual}.xlsx'

# Carregar dados de todas as ações e criar um DataFrame combinado
dfs = []  # Lista vazia para armazenar DataFrames de cada ação
for acao in acoes:
    df = pd.read_excel(nome_arquivo_excel, sheet_name=acao)  # Ler cada aba (ação) da planilha Excel
    df['Acao'] = acao  # Adicionar uma coluna para identificar de qual ação os dados pertencem
    dfs.append(df)  # Adicionar o DataFrame da ação à lista

# Concatenar todos os DataFrames em um único DataFrame
data = pd.concat(dfs)

# Filtrar apenas as colunas de interesse e pivotar os dados para que cada ação tenha suas colunas
data_pivot = data.pivot_table(index='Data', columns='Acao', values=['Open', 'High', 'Low', 'Volume', 'Close'])

# Preencher valores ausentes com interpolação ou valores anteriores
data_pivot.fillna(method='ffill', inplace=True)

# Separar a coluna 'Close' da PETR4 como alvo (target) e usar as outras como features
features = data_pivot.drop(('Close', 'PETR4'), axis=1).values  # Remover a coluna 'Close' de PETR4 das features
target = data_pivot[('Close', 'PETR4')].values  # Definir a coluna 'Close' de PETR4 como o alvo a ser previsto

# Normalizar os dados de features e target para a faixa de 0 a 1
scaler = MinMaxScaler(feature_range=(0, 1))  # Criar um normalizador
features_scaled = scaler.fit_transform(features)  # Normalizar as features
target_scaled = scaler.fit_transform(target.reshape(-1, 1))  # Normalizar o target

# Dividir os dados em treino e teste, sem embaralhar (shuffle=False) para manter a sequência temporal
X_train, X_test, y_train, y_test = train_test_split(features_scaled, target_scaled, test_size=0.2, shuffle=False)

# Modelo RNN
rnn_model = Sequential()  # Inicializar o modelo sequencial
rnn_model.add(SimpleRNN(50, activation='relu', input_shape=(X_train.shape[1], 1)))  # Adicionar uma camada RNN com 50 neurônios
rnn_model.add(Dense(1))  # Adicionar uma camada densa para prever um valor único

rnn_model.compile(optimizer='adam', loss='mean_squared_error')  # Compilar o modelo usando Adam e MSE como função de perda
rnn_model.fit(X_train, y_train, epochs=50, batch_size=32)  # Treinar o modelo com 50 épocas e batch size de 32

# Fazer previsões com o modelo RNN
rnn_predictions = rnn_model.predict(X_test)

# Modelo LSTM
lstm_model = Sequential()  # Inicializar o modelo sequencial
lstm_model.add(LSTM(50, activation='relu', input_shape=(X_train.shape[1], 1)))  # Adicionar uma camada LSTM com 50 neurônios
lstm_model.add(Dense(1))  # Adicionar uma camada densa para prever um valor único

lstm_model.compile(optimizer='adam', loss='mean_squared_error')  # Compilar o modelo usando Adam e MSE como função de perda
lstm_model.fit(X_train, y_train, epochs=50, batch_size=32)  # Treinar o modelo com 50 épocas e batch size de 32

# Fazer previsões com o modelo LSTM
lstm_predictions = lstm_model.predict(X_test)

# Modelo XGBoost
xgb_model = xgb.XGBRegressor(objective='reg:squarederror', n_estimators=1000)  # Criar o modelo XGBoost com 1000 árvores
xgb_model.fit(X_train, y_train)  # Treinar o modelo XGBoost

# Fazer previsões com o modelo XGBoost
xgb_predictions = xgb_model.predict(X_test)

# Função para avaliar o desempenho dos modelos usando o RMSE
def evaluate_model(predictions, y_test):
    rmse = np.sqrt(mean_squared_error(y_test, predictions))  # Calcular o RMSE
    return rmse

# Avaliar o RMSE de cada modelo
print('RNN RMSE:', evaluate_model(rnn_predictions, y_test))
print('LSTM RMSE:', evaluate_model(lstm_predictions, y_test))
print('XGBoost RMSE:', evaluate_model(xgb_predictions, y_test))

# Gráfico das previsões dos três modelos comparados com os valores reais
plt.plot(y_test, label='Real')  # Plotar os valores reais
plt.plot(rnn_predictions, label='RNN Predictions')  # Plotar as previsões do RNN
plt.plot(lstm_predictions, label='LSTM Predictions')  # Plotar as previsões do LSTM
plt.plot(xgb_predictions, label='XGBoost Predictions')  # Plotar as previsões do XGBoost
plt.legend()  # Adicionar a legenda
plt.show()  # Exibir o gráfico
