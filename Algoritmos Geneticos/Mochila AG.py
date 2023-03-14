## CREADO NDD Sept 2020
## modificado estudiantes curso 2020

import random
import numpy as np


"""   Comentarios son Una Linea: #
O triple comilla doble: Un bloque"""

"""Si se desea una población inicial no aleatoria
cromosoma1 = [1, 0, 0, 0, 1]
cromosoma2 = [0, 1, 0, 0, 0]
cromosoma3 = [1, 1, 0, 0, 1]
cromosoma4 = [1, 1, 1, 0, 1]
poblInicial = np.array([cromosoma1, cromosoma2, cromosoma3, cromosoma4]
"""

# MEJORA: Tamaño de la Población como parametro 
#random.seed(1)
#print("\n","aletorio:", random.randrange(2)) #Entero 0 o 1

##### FUNCIONES PARA OPERADORES

def evalua(n,x,poblIt,utilidad):
    suma=0
    total=0
    for i in range(0, n):
      for j in range(0,x):
        suma+=poblIt[i,j]*utilidad[j]
      fitness[i]=suma
      total+=suma
      suma=0
    return fitness,total

def imprime(n,total,fitness,poblIt):
    #Tabla de evaluación de la Población
    acumula=0
    print ("\n",'Tabla Iteración:',"\n")
    for i in range(0, n):
      probab=fitness[i]/total
      acumula+=probab
      print([i+1]," ",poblIt[i],"  ",fitness[i]," ","{0:.3f}".format(probab)," ","{0:.3f}".format(acumula))
      acumulado[i]=acumula
    print("Total Fitness:      ", total)
    return acumulado

def seleccion(acumulado):
    escoje=np.random.rand()
    print("escoje:      ", escoje)
    
    for i in range(0,n):
      if acumulado[i]>escoje:
        print('indiv ', i+1)
        return poblIt[i] # retorna el padre escogido
    

def cruce(p1,p2): # se modifica el punto de corte para hacerlo aleatorio.
  a1=np.random.rand()

  if a1<= Pcruce:
    print("Mas grande", Pcruce, "que ", a1, "-> Si Cruzan")
    
    proCorte = np.random.rand()#probabilidad donde se hace el corte
    puntoCorte = 1/(x-1) # nos entrega el porcentaje de corte entre gen

    # cada 1/(x-1) hay punto de corte 
    i=1
    pos=0
    print('\n donde se debe hacer el corte ',proCorte)
    for i in range(x):
      if i*puntoCorte > proCorte:
        pos=i
        break    
    print('\n el corte es en la posicion', pos)
    temp1=p1[0:pos] #[i:j] corta desde [i a j)
    temp2=p1[pos:x]
    print(temp1,temp2)
    temp3=p2[0:pos]
    temp4=p2[pos:x]
    print(temp3,temp4)
    hijo1 = list(temp1)
    hijo1.extend(list(temp4))
    hijo2 = list(temp3)
    hijo2.extend(list(temp2))

  else:
    print("Menor", Pcruce, "que ", a1, "-> NO Cruzan")
    hijo1=p1
    hijo2=p2
  
  return hijo1,hijo2


def mutacion(h): # h = al hijo que entra para verificar si muta uno de los genes
  
  for i in range(x): 
    a1=np.random.rand()
    if a1<= Pmuta:
      print("Mas grande", Pmuta, "que ", a1, "-> Si muta el gen", i+1, 'de ', h)
      if h[i] == 0:
         h[i] = 1
      else:
        h[i] = 0

  return h


def factible(h): 
  mult = 0
  for i in range(x):#x es el numero de genes 
    mult +=pesos[i]*h[i]

  return (mult <= pesoMax)    
      
    
#### Parametros #####
x=4  #numero de variables de decision - Elementos diferentes: x
n=4  #numero de individuos en la poblacion - cromosomas: n
Pcruce=0.98  #Probabilidad de Cruce
Pmuta=0.1   #Probabilidad de Mutación
pesoMax = 15 # peso maximo que puede cargar la mochila

fitness= np.empty((n))
acumulado= np.empty((n))
suma=0
total=0

# Ingresar los datos del Problema de la Mochila - Peso y Utilidad de los Elementos
pesos = [7, 6, 8, 2]
utilidad = [4, 5, 6, 3]
#pesos = [5, 7, 10, 30, 25]
#utilidad = [10, 20, 15, 30,15]

#Individuos, soluciones o cromosomas 
poblInicial = np.random.randint(0, 2, (n, x)) # aleatorios (n por x) enteros entre [0 y2)
 
for i in range(n):
  while not factible(poblInicial[i]):
    poblInicial[i] = np.random.randint(0, 2) # aleatorios (n por x) enteros entre [0 y2)


#random.random((4,5)) # 4 individuos 4 genes




print("Poblacion inicial Aleatoria:","\n", poblInicial)
print("\n","Utilidad:", utilidad) 
print("\n","Pesos", pesos )   
poblIt=poblInicial

######  FIN DE LOS DATOS INICIALES





##Llama función evalua, para calcular el fitness de cada individuo
fitness,total=evalua(n,x,poblIt,utilidad)
#####print("\n","Funcion Fitness por individuos",  fitness)
#####print("\n","Suma fitness: ",  total)

##### imprime la tabla de la iteracion
imprime(n,total,fitness,poblIt)

##### ***************************************
# Inicia Iteraciones

# Crear matriz de 5x2 vacio  a = numpy.zeros(shape=(5,2))
a = np.zeros(shape=(n,x))
poblintermedia = a.astype(int) # convierte a enteros todos los 0  de la matriz

pos=0

try:
  numIter = int(input('ingrese el número de iteraciones que desea: '))
except:
  print('por favor ingrese un valor entero ejm 2 , 10')

for iter in range(numIter):
  print("\n","Iteración ", iter+1)
  pos=0

  while pos < n: # para generar los hijos en todas las posiciones del vector 

    for i in [0,2]:  ## Para el bloque de 2 hijos cada vez
      papa1=seleccion(acumulado) # Padre 1 con la posicion que ocupa 
      print("padre 1:", papa1)
      papa2=seleccion(acumulado) # Padre 2 con la posicion que ocupa 
      print("padre 2:", papa2)
      
      hijoA,hijoB=cruce(papa1,papa2)
      hijoA = mutacion(hijoA)
      hijoB = mutacion(hijoB)

      if factible(hijoA) and factible(hijoB) and pos < n-1:
        print("hijo1: ", hijoA)
        poblintermedia[pos]=hijoA
        print("hijo2: ", hijoB)
        pos+=1
        poblintermedia[pos]=hijoB
        pos+=1 # se aumenta en 1 porque se agrego un hijo a la matriz
    
      elif factible(hijoA) and pos<n:
        print("hijo1: ", hijoA)
        poblintermedia[pos]=hijoA
        pos+=1

      elif factible(hijoB) and pos<n:
        print("hijo2: ", hijoB)
        poblintermedia[pos]=hijoB
        pos+=1

      else:
        print('ningun hijo es factible se continua...')

  poblIt=poblintermedia  
    
    
  print("\n","Poblacion Iteración ", iter+1,"\n", poblIt)
  fitness,total=evalua(n,x,poblIt,utilidad)
  #### print("\n","Funcion Fitness por individuos",  fitness)
  #### print("\n","Suma fitness: ",  total)

  ##### imprime la tabla de la iteracion
  imprime(n,total,fitness,poblIt)
    
