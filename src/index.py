# Bibliotecas
from pulp import *
import numpy as np

# Dados de Entrada #
# CSV Excel
custo = np.genfromtxt("./src/TSP_CSV.csv", delimiter = ",")

# Parametros
n_vertices = len(custo)
arcos = [(i,j) for i in range(n_vertices) for j in range(n_vertices) if custo[i,j] != 999] # Par de nós do arco 

# Iniciando o algoritmo de resolução (LP)
tsp = LpProblem("Caixeiro_Viajante", LpMinimize) # Nome do modelo, Função pra minimizar

# Variáveis de decisão
x = LpVariable.dicts("x", arcos, cat = "Binary") # Cria um dicinário de x
u = LpVariable.dicts("u", [i for i in range(n_vertices)], lowBound = 1, upBound = n_vertices, cat = "Continuous") # Variavel de decisão

# Funcao objetivo
tsp += lpSum(custo[i,j] * x[i,j] for (i,j) in arcos) # Calcula o valor final

# Restricao 1
for j in range(n_vertices):
    tsp += lpSum(x[i,j] for (i,m) in arcos if m==j) == 1 # Fixa o j

# Restricao 2
for i in range(n_vertices):
    tsp += lpSum(x[i,j] for (m,j) in arcos if m==i) == 1 # Fixa o i
    
# Restricao 3
for (i,j) in arcos:
    if i > 0 and i != j:
        tsp += u[i] - u[j] + n_vertices*x[i,j] <= n_vertices - 1

# Resolvendo o modelo
resolver_modelo = tsp.solve()
print(f"Status do problema: {LpStatus[resolver_modelo]}")

# Display variaveis
for var in tsp.variables():
    if var.varValue > 0:
        print(f"{var.name} = {var.varValue}")
        
# Display função-objetivo
print(f"Custo total = ${value(tsp.objective)}")
