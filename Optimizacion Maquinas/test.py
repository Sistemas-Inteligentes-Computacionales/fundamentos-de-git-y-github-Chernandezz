# Algoritmo Realizado Por: Cristian Felipe Hernandez Zuluaga - chernandezz@unal.edu.co
# Universidad Nacional de Colombia
# Facultad de Administracion
# Programa de Administracion de sistemas informaticos

import numpy as np
import random
from prettytable import PrettyTable
import matplotlib.pyplot as plt


pesos = [7, 6, 8, 2] #pesos de los elementos
utilidad = [4, 5, 6, 3] #utilidad de los elementos

Pcruce=0.98  #Probabilidad de Cruce
Pmuta=0   #Probabilidad de Mutación
pesoMax = 50 # peso maximo que puede cargar la mochila

# Restricciones
# peso <= 50
try:
  cantVariables = int(input('Variables: '))
  cantIndividuos = int(input('Individuos: '))
  while cantIndividuos % 2 != 0:
    print('El numero de individuos debe ser par')
    cantIndividuos = int(input('Individuos: '))
  cantidadBits = int(input('Bits por gen: '))
except:
  print('por favor ingrese un valor entero ejm 2 , 10')

def llenadoGenotipoBinarios():
  datosBinarios = []
  for i in range(cantVariables*cantidadBits):
    datosBinarios.append(random.randint(0, 1))
  return datosBinarios

def calculoPesos(genotipo):
  pesoTotal = 0
  for i in range(0,len(genotipo["datosBinarios"]),2):
    valorDecimal = int(str(genotipo["datosBinarios"][i])+str(genotipo["datosBinarios"][i+1]),2)
    peso = pesos[i//cantidadBits]
    pesoTotal += valorDecimal * peso
  return pesoTotal

def llenadoGenotipoDecimales(genotipo):
  decimal = []
  temp= ""
  for i in range(0,len(genotipo["datosBinarios"]),cantidadBits):
    for j in range(i,i+cantidadBits):
      temp += str(genotipo["datosBinarios"][j])
    valorDecimal = int(temp,2)
    temp = ""
    decimal.append(valorDecimal)
  return decimal

def calculoFitness(genotipo):
  UtilidadTotal = 0
  for i in range(0,len(genotipo["datosBinarios"]),2):
    valorDecimal = int(str(genotipo["datosBinarios"][i])+str(genotipo["datosBinarios"][i+1]),2)
    utilidadTemp = utilidad[i//cantidadBits]
    UtilidadTotal += valorDecimal * utilidadTemp
  return UtilidadTotal

def calculoPromedios(tablaGenotipos, fitnessTotal):
  promedioAcumulado = 0
  for i in range(1,len(tablaGenotipos)+1):
    promedio = tablaGenotipos[i]["fitness"] / fitnessTotal
    tablaGenotipos[i]["promedio"] = promedio
    promedioAcumulado += promedio
    tablaGenotipos[i]["promedioAcumulado"] = promedioAcumulado
  return tablaGenotipos

def llenadoTablaCompletaGenotipos(cantIndividuos):
  tablaCompletaGenotipos = {}
  fitnessTotal = 0
  for i in range(cantIndividuos):
    genotipo = {}
    # Validacion para que el peso no sea mayor a 50
    while True:
      genotipo["datosBinarios"] = llenadoGenotipoBinarios()
      genotipo["peso"] = calculoPesos(genotipo)
      if genotipo["peso"] <= pesoMax:
        break
    # Datos binarios a decimales
    genotipo["datosDecimales"] = llenadoGenotipoDecimales(genotipo)
    # Calculo del fitness
    genotipo["fitness"] = calculoFitness(genotipo)
    fitnessTotal += genotipo["fitness"]
    tablaCompletaGenotipos[i+1] = genotipo
  # Los promedios toca hacerlos al final porque se necesita el fitness total
  tablaCompletaGenotipos = calculoPromedios(tablaCompletaGenotipos, fitnessTotal)
  return tablaCompletaGenotipos, fitnessTotal

def creacionEstructuraGentipo(datosBinarios):
  genotipo = {}
  genotipo["datosBinarios"] = datosBinarios
  genotipo["peso"] = calculoPesos(genotipo)
  genotipo["datosDecimales"] = llenadoGenotipoDecimales(genotipo)
  genotipo["fitness"] = calculoFitness(genotipo)
  if genotipo["peso"] > pesoMax:
    genotipo["fitness"] = 0
  return genotipo

def mostrarDatosGen(tablaGenotipos):
  for i in tablaGenotipos:
    print("=========== Genotipo ", i, " ===========")
    print("Datos Binarios:", tablaGenotipos[i]["datosBinarios"])
    print("Peso:", tablaGenotipos[i]["peso"])
    print("Datos Decimales:", tablaGenotipos[i]["datosDecimales"])
    print("Fitness:", tablaGenotipos[i]["fitness"])
    print("Promedio:", tablaGenotipos[i]["promedio"])
    print("Promedio Acumulado:", tablaGenotipos[i]["promedioAcumulado"])

def mostrarTablaGenotipos(tablaGenotipos):
  tabla = PrettyTable()
  tabla.field_names = ["Genotipo", "Datos Binarios", "Peso", "Datos Decimales", "Fitness", "Promedio", "Promedio Acumulado"]
  for i in tablaGenotipos:
    tabla.add_row([i, tablaGenotipos[i]["datosBinarios"], tablaGenotipos[i]["peso"], tablaGenotipos[i]["datosDecimales"], tablaGenotipos[i]["fitness"], tablaGenotipos[i]["promedio"], tablaGenotipos[i]["promedioAcumulado"]])
  print(tabla)

def seleccionPadre(tablaGenotipos):
  aleatorio = random.random()
  for i in tablaGenotipos:
    if aleatorio <= tablaGenotipos[i]["promedioAcumulado"]:
      return tablaGenotipos[i]
    
def cruce(papa1, papa2):
  # Seleccionar el punto de cruce
  puntoCruce = random.randint(0, len(papa1["datosBinarios"])-1)
  # Hijo 1
  hijo1 = papa1["datosBinarios"][:puntoCruce] + papa2["datosBinarios"][puntoCruce:]
  # Hijo 2
  hijo2 = papa2["datosBinarios"][:puntoCruce] + papa1["datosBinarios"][puntoCruce:]
  return hijo1, hijo2

def mutacion(hijo):
  for i in range(len(hijo)):
    aleatorio = random.random()
    if aleatorio <= Pmuta:
      if hijo[i] == 0:
        hijo[i] = 1
      else:
        hijo[i] = 0
  return hijo

def calculoFitnessTotalTemporal(tablaGenotiposTemporal):
  fitnessTotalTemporal = 0
  for i in range(1,len(tablaGenotiposTemporal)+1):
    fitnessTotalTemporal += tablaGenotiposTemporal[i]["fitness"]
  return fitnessTotalTemporal

def mejorIndividuo(tablaGenotipos):
  mejorIndividuo = 0
  for i in range(1,len(tablaGenotipos)+1):
    if tablaGenotipos[i]["fitness"] > mejorIndividuo:
      mejorIndividuo = tablaGenotipos[i]["fitness"]
  return mejorIndividuo

def promedioFitness(tablaGenotipos):
  promedio = 0
  for i in range(1,len(tablaGenotipos)+1):
    promedio += tablaGenotipos[i]["fitness"]
  promedio = promedio / len(tablaGenotipos)
  return promedio

def mostrarResumenIteraciones(datosIteracion):
  tabla = PrettyTable()
  tabla.field_names = ["Iteración", "Mejor Fitness", "Promedio Fitness", "Fitness Total"]
  for i in range(len(datosIteracion)):
    tabla.add_row([datosIteracion[i][0], datosIteracion[i][1], datosIteracion[i][2], datosIteracion[i][3]])
  print(tabla)

def verificacionConvergencia(tablaGenotipos):
  primerFitness = tablaGenotipos[1]["fitness"]
  for i in range(1,len(tablaGenotipos)+1):
    if primerFitness != tablaGenotipos[i]["fitness"]:
      return False
  return True

def graficar(datosIteracion):
  x = []
  y = []
  for i in range(len(datosIteracion)):
    x.append(datosIteracion[i][0])
    y.append(datosIteracion[i][1])
  plt.plot(x, y)
  plt.title('Mejor Fitness por iteración')
  plt.xlabel('Iteración')
  plt.ylabel('Fitness')
  plt.show()

TablaGenes, fitnessTotal = llenadoTablaCompletaGenotipos(cantIndividuos)
print("Tabla de genotipos: ")
mostrarTablaGenotipos(TablaGenes)
print("Fitness Total: ", fitnessTotal)


try:
  numIter = int(input('ingrese el número de iteraciones que desea: '))
except:
  print('por favor ingrese un valor entero ejm 2 , 10')
datosIteracion = []
dato = []
dato.append(1)
dato.append(mejorIndividuo(TablaGenes))
dato.append(promedioFitness(TablaGenes))
dato.append(fitnessTotal)
datosIteracion.append(dato)

for iter in range(numIter):
  
  contPos = 1
  tablaGenotiposTemporal = {}
  dato = []
  for i in range(len(TablaGenes)//2):
  # Seleccionar los mejores 2
    aleatorioCruce = random.random()
    papa1 = seleccionPadre(TablaGenes)
    papa2 = seleccionPadre(TablaGenes)
    if aleatorioCruce <= Pcruce:
      # Cruce
      hijo1, hijo2 = cruce(papa1, papa2)
      # Mutación
      aleatorioMuta = random.random()
      if aleatorioMuta <= Pmuta:
        hijo1 = mutacion(hijo1)
        hijo2 = mutacion(hijo2)
      tablaGenotiposTemporal[contPos] = creacionEstructuraGentipo(hijo1)
      contPos += 1
      tablaGenotiposTemporal[contPos] = creacionEstructuraGentipo(hijo2)
      contPos += 1
    else:
      tablaGenotiposTemporal[contPos] = papa1
      contPos += 1
      tablaGenotiposTemporal[contPos] = papa2
      contPos += 1
  # # Calculo de los promedios
  fitnessTotalTemporal = calculoFitnessTotalTemporal(tablaGenotiposTemporal)
  tablaGenotiposTemporal = calculoPromedios(tablaGenotiposTemporal, fitnessTotalTemporal)
  TablaGenes = tablaGenotiposTemporal
  fitnessTotal = fitnessTotalTemporal
  dato.append(iter+2)
  dato.append(mejorIndividuo(TablaGenes))
  dato.append(promedioFitness(TablaGenes))
  dato.append(fitnessTotal)
  datosIteracion.append(dato)
  # Si se desea evitar que el programa se detenga al encontrar convergencia comentar el bloque del if -> linea 222 hasta la linea 225
  if verificacionConvergencia(TablaGenes):
    print("--------------- CONVERGENCIA ---------------")
    print("Se ha alcanzado la convergencia en la iteración: ", iter+1)
    print("SOLUCIÓN: ")
    mostrarTablaGenotipos(TablaGenes)
    print("Fitness Total: ", fitnessTotal)
    break
print("Resumen de iteraciones: ")
mostrarResumenIteraciones(datosIteracion)
print("Grafica: ")
graficar(datosIteracion)


