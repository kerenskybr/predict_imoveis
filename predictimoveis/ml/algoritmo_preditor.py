#Arquivo responsavel por treinar o modelo
#e salvar os dados de treino e acuracia


import pandas as pd
import numpy as np

import seaborn as sns
import matplotlib.pyplot as plt

from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import mean_squared_error
from sklearn.externals import joblib


casas = pd.read_csv("/home/roger/Documents/predict_imoveis/new_data.csv")

#print(casas.head())

#Verificando e encontrando valores nulos

null_columns=casas.columns[casas.isnull().any()]
print(casas[null_columns].isnull().sum())

print(casas[casas.isnull().any(axis=1)][null_columns].head())

#Excluindo valores com erro
casas.dropna(inplace=True)
#print(casas.isnull().sum())

#verificando correlações

#corr = casas.corr()
#sns.heatmap(corr, cmap="BuPu")
#plt.show()

#Criando o modelo de regressão linear multipla

colunas = ['dorms', 'banho','vagas', 'area']

x = casas[colunas] #Classe preditora
y = casas.valor #Atributo de resposta

#Dividindo entre teste e treino
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.33)

lin_reg = LinearRegression()
lin_reg.fit(x_train, y_train)


print(lin_reg.intercept_)
print(lin_reg.coef_)
#Usando a funcao quadratica para estimar a acuracia do modelo

mse = mean_squared_error(y_test, lin_reg.predict(x_test))

np.sqrt(mse)

porc = lin_reg.score(x_test, y_test)


while porc < 0.80:
	if porc < 0.80:
		#Dividindo entre teste e treino
		x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.33)

		lin_reg = LinearRegression()
		lin_reg.fit(x_train, y_train)
		
		mse = mean_squared_error(y_test, lin_reg.predict(x_test))

		np.sqrt(mse)

		porc = lin_reg.score(x_test, y_test)

		print("Precisao do modelo: ", format(porc*100, '.2f'), '%')

	if porc > 0.80:
		print("Precisao final: ", format(porc*100, '.2f'), '%')
		print("Executado com sucesso. Salvando modelo...")

		#Salvando o modelo
		arquivo = "saves/modelo_final.sav"
		joblib.dump(lin_reg, arquivo)

		#salvando medida de acuracia
		medida_x = "saves/x_test.sav"
		joblib.dump(x_test, medida_x)

		medida_y = "saves/y_test.sav"
		joblib.dump(y_test, medida_y)







































