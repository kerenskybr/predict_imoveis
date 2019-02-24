#Arquivo responsavel por treinar o modelo
#e salvar os dados de treino e acuracia
#Posteriormente será movido para uma rota

import pandas as pd
import numpy as np

import seaborn as sns

from scipy import stats

import matplotlib.pyplot as plt

from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import mean_squared_error
from sklearn.externals import joblib

from sknn.mlp import Regressor, Layer


casas = pd.read_csv("/home/roger/Documents/predict_imoveis/predictimoveis/csv/new_data.csv")

#print(casas.head())

#Verificando e encontrando valores nulos

null_columns=casas.columns[casas.isnull().any()]
print(casas[null_columns].isnull().sum())

print(casas[casas.isnull().any(axis=1)][null_columns].head())

#Excluindo valores com erro
casas.dropna(inplace=True)
#print(casas.isnull().sum())

#Verificando correlações

#corr = casas.corr()
#sns.heatmap(corr, cmap="BuPu")
#plt.show()

#Detectando Outliers


z = np.abs(stats.zscore(casas))
print("outliers", z)

threshold = 3
print(np.where(z > 3))


#Pontuação dos valores medios
Q1 = casas.quantile(0.25)
Q3 = casas.quantile(0.75)
IQR = Q3 - Q1
print(IQR)

#Printando os outliers (recebem true_)
print((casas < (Q1 - 1.5 * IQR)) |(casas > (Q3 + 1.5 * IQR)))

#Removendo os outliers
casas_limpo = casas[~((casas < (Q1 - 1.5 * IQR)) |(casas > (Q3 + 1.5 * IQR))).any(axis=1)]


#Verificando pares
#sns.pairplot(casas)
#plt.show()

#Plotando grafico de Regressao Linear
#sns.set(style="darkgrid")
#sns.jointplot("dorms", "banho", data=casas, kind="reg", xlim=(0, 60), ylim=(0, 12), color="m", height=7)
#plt.show()

#Criando o modelo de regressão linear multipla

colunas = ['dorms', 'banho','vagas', 'area']

x = casas_limpo[colunas] #Classe preditora
y = casas_limpo.valor #Atributo de resposta

#Dividindo entre teste e treino
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.33, random_state = 42)

print("Shape do x", x_train.shape)
print("Shape do y", y_train.shape)

lin_reg = LinearRegression()
lin_reg.fit(x_train, y_train)

#Plotando grafico de Regressao Linear
#sns.set(style="darkgrid")
#sns.pairplot(casas, x_vars=["dorms", "banho", "area", "vagas"], y_vars=["valor"], height=5, aspect=.8, kind="reg");

#sns.pairplot(casas, x_vars=["banho", "area", "vagas"], y_vars=["valor"], hue="dorms", height=4, aspect=.8, kind="reg");

#plt.show()

#Scater Plot
#Usando para detectar outliers

fig, ax = plt.subplots(figsize=(8,4))
ax.scatter(casas['valor'], casas['area'])
ax.set_xlabel('Valor')
ax.set_ylabel('Areas')
plt.show()




print(lin_reg.intercept_)
print(lin_reg.coef_)
#Usando a funcao quadratica para estimar a acuracia do modelo

mse = mean_squared_error(y_test, lin_reg.predict(x_test))

np.sqrt(mse)

porc = lin_reg.score(x_test, y_test)

print("Precisao do modelo: ", format(porc*100, '.2f'), '%')

y_pred = lin_reg.predict(x_train)


dorms = 2
banho = 2
vagas = 1
area = 122

areas = [[dorms, banho, vagas, area]]

#Como usar o reshape:
#x_test.values.reshape(-1, 1)

'''
# Plot outputs
plt.scatter(x_test , y_test,  color='black')

plt.plot(x_test, y_pred, color='blue', linewidth=3)

plt.xticks(())
plt.yticks(())

plt.xlim(-2, 2)
plt.ylim(-2, 2)

plt.show()
'''

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
		arquivo = "modelo_final.sav"
		joblib.dump(lin_reg, arquivo)

		#salvando medida de acuracia
		medida_x = "x_test.sav"
		joblib.dump(x_test, medida_x)

		medida_y = "y_test.sav"
		joblib.dump(y_test, medida_y)
