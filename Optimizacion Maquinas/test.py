
import numpy as np
import random

pesos = [7, 6, 8, 2] #pesos de los elementos
utilidad = [4, 5, 6, 3] #utilidad de los elementos

Pcruce=0.98  #Probabilidad de Cruce
Pmuta=0.1   #Probabilidad de Mutación
pesoMax = 50 # peso maximo que puede cargar la mochila

# Restricciones
# peso <= 50
try:
  cantVariables = int(input('Variables: '))
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
    peso = pesos[i//2]
    pesoTotal += valorDecimal * peso
  return pesoTotal

def llenadoGenotipoDecimales(genotipo):
  decimal = []
  for i in range(0,len(genotipo["datosBinarios"]),2):
    valorDecimal = int(str(genotipo["datosBinarios"][i])+str(genotipo["datosBinarios"][i+1]),2)
    decimal.append(valorDecimal)
  return decimal

def calculoFitness(genotipo):
  UtilidadTotal = 0
  for i in range(0,len(genotipo["datosBinarios"]),2):
    valorDecimal = int(str(genotipo["datosBinarios"][i])+str(genotipo["datosBinarios"][i+1]),2)
    utilidad = pesos[i//2]
    UtilidadTotal += valorDecimal * utilidad
  return UtilidadTotal

def llenadoTablaCompletaGenotipos(cantIndividuos):
  tablaCompletaGenotipos = {}
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
    tablaCompletaGenotipos[i+1] = genotipo
  return tablaCompletaGenotipos

def mostrarTabla(tablaGenotipos):
  for i in tablaGenotipos:
    print("=========== Genotipo ", i, " ===========")
    print("Datos Binarios:", tablaGenotipos[i]["datosBinarios"])
    print("Peso:", tablaGenotipos[i]["peso"])
    print("Datos Decimales:", tablaGenotipos[i]["datosDecimales"])
    print("Fitness:", tablaGenotipos[i]["fitness"])

elementos = llenadoTablaCompletaGenotipos(cantIndividuos)
print("Tabla de genotipos: ")
mostrarTabla(elementos)

try:
  numIter = int(input('ingrese el número de iteraciones que desea: '))
except:
  print('por favor ingrese un valor entero ejm 2 , 10')

for iter in range(numIter):
  print("Iteración: ", iter+1)
  # Seleccionar los mejores 2
  aleatorioCruce = random.random()
