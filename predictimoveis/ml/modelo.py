#Arquivo que carrega o modelo treinado
#e executa a funcionalidade

from sklearn.externals import joblib
from sklearn.metrics import mean_squared_error
import numpy as np


carrega_modelo = joblib.load('../saves/modelo_final.sav')
medida_x = joblib.load('../saves/x_test.sav')
medida_y = joblib.load('../saves/y_test.sav')

dorms = int(input('Digite a quantidade de dormitórios: '))
banho = int(input('Digite a quantidade de banhos: '))
vagas = int(input('Digite a quantidade de vagas para carros: '))
area = int(input('Digite area total da residência: '))

#Prevendo com entrada manual

areas = [[dorms, banho, vagas, area]]

print("Valor estimado R$", carrega_modelo.predict(areas))

#Usando a funcao quadratica para estimar a acuracia do modelo

mse = mean_squared_error(medida_y, carrega_modelo.predict(medida_x))

np.sqrt(mse)

porc = carrega_modelo.score(medida_x, medida_y)

print("Precisao do modelo: ", format(porc*100, '.2f'), '%')

