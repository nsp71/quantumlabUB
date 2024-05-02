import matplotlib.pyplot as plt
import numpy as np
import random
from collections import deque



##########################################################################################################################

#IN: 1) Mida n de la matriu. 2) Probabilitat p de tenir 1 a una posició determinada
#OUT: Matriu nxn de 1's i 0's

def matriu_quadrat(n,p):
    matriu = np.zeros((n,n),int)    #Comencem generant una matriu buida de dimensions nxn

    for i in range(n):
        for j in range(n):
            q = random.random() #Probabilitat de formar enllaç, si  q >= p es forma enllaç (1 a la matriu), altrament 0
            if q < p:
                matriu[i,j] = 1
    return matriu

############################################################################################################################

#nomes funciona fins matrius de mida n = 60 :(
#IN: 1) Matriu nxn. 2) Posició i, j (ha de tenir una valor = 1)
#OUT: Llista de les posicions del cluster que comença a i,j

def cluster_funcio(matriu, i, j, n, visitat):
    max_depth = 10
    cluster_vec = []

    # Funció per buscar veins de veins etc recursiva (potser no és el més eficient) -> peta amb matrius de mida >= 60
    def veins_recursius(x, y, depth):
        if depth >= max_depth or visitat[x, y]:
            return
        visitat[x, y] = True
        cluster_vec.append((x, y))

        # Explorar los vecinos
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < len(matriu) and 0 <= ny < len(matriu[0]) and matriu[nx, ny] == 1 and not visitat[nx, ny]:
                veins_recursius(nx, ny,0)

    veins_recursius(i, j, 0)
    return cluster_vec

###########################################################################################################################


#Esta función emplea el algoritmo bfs para encontrar caminos a partir de un punto dado.
#Devuelve un vector con los puntos de la matriz visitados
#Inici és una tupla de dos números que indiquen una posició dins la matriu.
def bfs(matriu, inici, visitat):
    #visitat = np.zeros(matriu.shape, dtype=bool)
    queue = deque([inici])
    vertex_actius = []

    #Mientras queden elementos en la cola para ser explorados el bucle no para
    #El concepto de deque es una abstracción de estructura de datos que sigue el principio fifo.
    while queue:
        row, col = queue.popleft()
        visitat[row, col] = True

        if matriu[row,col] == 1:
            vertex_actius.append((row,col))

        # Obtener vecinos válidos no visitados
        for neighbor_row, neighbor_col in [(row-1, col), (row+1, col), (row, col-1), (row, col+1)]:
            #amb la condició 0 <= ens assegurem que estem dins dels límits de la matriu.
            if 0 <= neighbor_row < len(matriu) and 0 <= neighbor_col < len(matriu[0]) and not visitat[neighbor_row, neighbor_col] and matriu[neighbor_row, neighbor_col] == 1:
                visitat[neighbor_row, neighbor_col] = True
                vertex_actius.append((neighbor_row,neighbor_col))
                queue.append((neighbor_row, neighbor_col))

    return vertex_actius

############################################################################################################################


#IN: 1) Matriu quadrada de dimensions nxn
#OUT: Llista amb tots els clusters de la matriu. Utilitza la funció cluster_funcio per buscar el
# cluster que comença a la posició i j

#Ara funciona amb bfs en comptes d'utilitzar la funció cluster_funcio (petava per matrius de mida >= 60

def busca_clusters(matriu):

    n = len(matriu[0])
    visitat = np.full((n, n), False, dtype=bool)
    llista_clusters = []

    for i in range(n):
        for j in range(n):
            if matriu[i, j] == 1 and not visitat[i, j]:
                llista_clusters.append(bfs(matriu, (i, j), visitat))

    return llista_clusters

###########################################################################################################################

#IN: 1) Matriu quadrada nxn. 2) Llista dels clusters
#OUT: Matriu amb els diferents clusters identificats amb diferents números

def pintar_clusters(matriu,vertex_actius):

    matriu_pintada = matriu.copy()
    for k in range(len(vertex_actius)):
        for i in range(len(vertex_actius[k])):
            x = vertex_actius[k][i][0]
            y = vertex_actius[k][i][1]
            matriu_pintada[x,y] = k + 1
    return matriu_pintada

###########################################################################################################################

#IN: 1) Matriu de dimensions nxn
#    2) cluster_per: llista inicialment buida. Si hi ha percolació es guardaran aquí
#       les posicions del cluster que percola
#OUT: Un número natural que indica quin és el cluster que ha percolat. Si no hi ha percolació es retorna -1

def percola(matriu, cluster_per):

    clusters = busca_clusters(matriu)
    # # de clusters del sistema
    n = len(clusters)
    #ens servirà per identificar el cluster que percola. Els enters no poden canviar si són passats com arguments de la funció
    perc_n = 0

    #Anem cluster per cluster veient si hi ha algun punt a la part superior, inferior
    #esquerra o dreta. Posem les variables corresponents a True i a partir de veure si
    #hi han vores oposades amb valors True determinem la percolació (o no percolació)

    top = False
    bottom = False
    left = False
    right = False

    for k in range(len(clusters)):
        for i in range(len(clusters[k])):
            if clusters[k][i][0] == 0:
                top = True
                perc_n = k
            if clusters[k][i][1] == n - 1:
                bottom = True
                perc_n = k
            if clusters[k][i][0] == n - 1:
                left = True
                perc_n = k
            if clusters[k][i][1] == n - 1:
                right = True
                perc_n = k

        #comprovem totes les possibilitats de percolació

    if ((top and bottom) or (top and right) or (top and left) or (left and right) or (bottom and right) or (bottom and left)):
        #clusters_per = cluster_percolat.append(clusters[perc_n])
        perc_n += 1
    else:
        perc_n = -1

    return perc_n

###########################################################################################################################

#IN: 1) Matriu de dimensions nxn
#OUT: Fracció de vèrtexs connectats

def fraccio_ver_con(matriu):

    ver_total = len(matriu)*len(matriu[0])
    clusters = busca_clusters(matriu)
    count_ver = set()
    count = 0

    for cluster in clusters:
        if len(cluster) > 1:
            for vertex in cluster:
                if vertex not in count_ver:
                    count_ver.add(vertex)
                    count += 1

    return count/ver_total

###########################################################################################################################

#IN: 1) Matriu de dimensions nxn
#OUT: Fracció de la mida del cluster més gran

def biggest_cluster_frac(matriu):

    ver_total = len(matriu)*len(matriu[0])
    clusters = busca_clusters(matriu)
    max_cluster_size = 0

    #Eliminen les repeticions de clusters. Altrament serà molt complicat trobar la mida del cluster més gran
    clusters_sin_repeticiones = []
    for cluster in clusters:
        cluster_sin_repeticiones = list(
            set(cluster))  # Convertimos a conjunto para eliminar repeticiones y luego a lista
        clusters_sin_repeticiones.append(cluster_sin_repeticiones)

    for cluster in clusters_sin_repeticiones:
        cluster_size = len(cluster)
        #actualitzem la mida del cluster més gran fins el moment
        if cluster_size > max_cluster_size:
             max_cluster_size = cluster_size

    return max_cluster_size/ver_total



###########################################################################################################################

#Gràfica del punt crític de percolació en funció de les dimensions de la matriu quadrada pel cas site percolation
def g1():
    # Gràfica que mostra el punt crític de percolació en funció de les dimensions de la matriu
    # Per cada probabilitat dins de probabilities generem matrius des de la mida inferior fins
    # la superior (elements dins de matrix_size) i busquem el punt de percolació amb percola.
    # Emmagatzemem el punt de percolació i mostrem els resultats en una gràfica

    probabilities = np.arange(0.1, 1.0, 0.01)
    matrix_sizes = range(2, 61)  # Mides de matrius que anem a provar
    num_trials = 1000
    aux = []

    critical_probabilities = {size: None for size in matrix_sizes}

    for size in matrix_sizes:
        for p in probabilities:
            percolating_trials = 0
            matrix = matriu_quadrat(size, p)
            if percola(matrix,aux) != -1:
                percolating_trials += 1
            if percolating_trials / 1 > 0:  # Percola, afegim el punt
                critical_probabilities[size] = p
                break
    # Regressió polinòmica per veure possibles tendències
    x_values = np.array(list(critical_probabilities.keys()))
    y_values = np.array(list(critical_probabilities.values()))
    regression_coeffs = np.polyfit(x_values, y_values, 2)  # Adjust degree as needed
    regression_line = np.poly1d(regression_coeffs)
    plt.plot(x_values, y_values, marker='o', label='Data')
    plt.plot(x_values, regression_line(x_values), linestyle='--', color='red', label='Regression')

    plt.plot(matrix_sizes, list(critical_probabilities.values()), marker='o')
    plt.xlabel('Mida de la matriu')
    plt.ylabel('Punt crític de percolació')
    plt.title('Punt crític de percolació en funció de la mida de la matriu')
    plt.grid(True)
    plt.show()

###########################################################################################################################

#Gràfica de la fracció de vèrtexs connectats en funció de la probabilitat de percolació pel cas site percolation
def g2():
    probabilities = np.arange(0.1, 1.0, 0.01)
    num_trials = 100  # Número de matrices a generar para cada probabilidad
    avg_fracs = []  # Almacenar el promedio de las fracciones de vértices conectados

    for p in probabilities:
        frac_sum = 0
        for _ in range(num_trials):
            matrix = matriu_quadrat(500, p)
            frac_sum += biggest_cluster_frac(matrix)  #fracció de cluster més gran
        avg_frac = frac_sum / num_trials  #mitjana de cluster de mida més gran per matriu de mida n i p
        avg_fracs.append(avg_frac)

    #Graficar els resultats
    plt.plot(probabilities, avg_fracs)
    plt.xlabel('p')
    plt.ylabel('Fracció del cluster més gran')
    plt.title('Fracció del cluster més gran en funció de p')
    plt.grid(True)
    plt.show()

############################################################################################################################
############################################################################################################################

                                # CÓDIGO PRINCIPAL:

#Gràfica del punt crític de percolació en funció de les dimensions de la matriu quadrada pel cas site percolation
#g1()

#Gràfica de la fracció de vèrtexs connectats en funció de la probabilitat de percolació
g2()


############################################################################################################################

                                # PRUEBAS ETC:

n = 4
p = 0.3

matriu = matriu_quadrat(n,p)
cluster_vec = []
visitat = np.full((n, n), False, dtype=bool)
print(matriu)
trobat = False
for i in range(n):
    for j in range(n):
        if matriu[i,j] == 1 and not trobat:
            cluster_vec = cluster_funcio(matriu, i, j, n,visitat)
            trobat = True
    if trobat:
        break

print(cluster_vec)
print(busca_clusters(matriu))
print(len(busca_clusters(matriu)))
caca = busca_clusters(matriu)
print(pintar_clusters(matriu,caca))
cluster_percolat = []
num = percola(matriu,cluster_percolat)
if num != -1:
    print(num)
    print(cluster_percolat)
else:
    print('No ha percolat :(')

print(fraccio_ver_con(matriu))
print(biggest_cluster_frac(matriu))

