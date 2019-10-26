import numpy as np
import matplotlib.pyplot as plt
from scipy.io import loadmat

'''

El fin de este programa es separar las mediciones de 10 mins en n intervalos de mediciones. De las mediciones de 
Matlab guardamos los arrays pks y locs. pks tiene los valores (en V) de los picos que se midieron en esos 10 mins y
el array locs tiene los lugares (indices) del array data (donde estan todos los valores de voltaje que se midieron)
donde estan los picos. Entonces, lo que hicimos fue dividir al tiempo total en n intervalos de igual duracion,
fijarse los ultimos indices de cada uno de esos intervalos, luego separar el array locs en n array "cortando" en los
indices mencionados (esto hace que no todos los arrays sean necesariamente de igual largo), luego separar el array
pks en base a como se separo el array locs, y finalmente hacer n histogramas con cada array. Este es un proceso que
a la maquina le requiere mucho trabajo, y por lo tanto los histogramas finales se guardaron en archivos .npy para 
no tener que hacer lo mismo muchas veces. El programa puede llegar a tardar entre 5 - 10 mins dependiendo de la pc
asi que denle un tiempito.

'''

#%% Separamos las mediciones de Cs en n sub-mediciones

# Especificamos la cantidad de intervalos.
n = 120

popt = [188.886, -25.54827996]


def recta(x, a, b):
    y = a * x + b
    return y


PATH = 'D:/Fede/UBA/6/Laboratorio 5/Experimentos de Fisica Nuclear'

print('Voy a importar los picos')

cesio_peaks = loadmat(PATH + "/Mediciones/Estadistica/cs_pks.mat")
cesio_peaks = cesio_peaks['pks']
cesio_peaks = cesio_peaks[:, 0]
cesio_peaks = cesio_peaks.tolist()

cesio_locs = loadmat(PATH + "/Mediciones/Estadistica/cs_locs.mat")
cesio_locs = cesio_locs['locs']
cesio_locs = cesio_locs[:, 0]
cesio_locs = cesio_locs.tolist()

# Para cesio hallamos los picos en este intervalo de voltajes. Primero vamos a cortar a los arrays para disminuir
# su longitud y disminuir la cantidad de cuentas que tiene que hacer la maquina.
V_min = 3.2
V_max = 5

print('Voy a cortar el espectro para tener solo el fotopico.')

pks = []
locs = []
for i in range(0, len(cesio_peaks)):
    if (cesio_peaks[i] > V_min) and (cesio_peaks[i] < V_max):
        pks.append(cesio_peaks[i])
        locs.append(cesio_locs[i])

f_sampleo_est = 100000
t_sample_est = 600

# Estos son los indices que salen de dividir el tiempo en intervalos de igual duracion.
indices = np.linspace(f_sampleo_est * t_sample_est / n, f_sampleo_est * t_sample_est, n)

# En estos arrays van a estar los arrays con los locs y los pks.
L = []
P = []
for i in range(0, n):
    P.append([])
    L.append([])

print('Voy a separar los datos.')

for i in range(0, len(locs)):
    if locs[i] < indices[0]:
        L[0].append(locs[i])
    else:
        for j in range(0, n):
            if indices[j - 1] < locs[i] < indices[j]:
                L[j].append(locs[i])

print('Voy a separar los picos:')

for j in range(0, n):
    for i in range(0, len(L[j])):
        P[j].append(pks[locs.index(L[j][i])])
    print('     Termine con el array numero {}.'.format(j))

L = np.asarray(L)
P = np.asarray(P)

#%% Hacemos los histogramas

print('Voy a hacer los histogramas.')

res = 0.000329      # La misma resolucion que para los datos de la calibracion.
V_range = np.arange(V_min, V_max, 100 * res)

H = []
for j in range(0, n):
    H.append(np.histogram(P[j], V_range))

print('Voy a graficar.')

# Deberian verse todos los histogramas iguales, solo la cantidad de puntos en cada uno deberia ser distinta.
plt.figure('Histogramas')
for j in range(0, n):
    plt.plot(recta(H[j][1][:-1], popt[0], popt[1]), H[j][0], 'o', label='{}'.format(j))
plt.grid()
plt.xlabel('Energía (keV)')
plt.ylabel('Cuentas')
plt.legend()
plt.show()

print('Voy a guardar los histogramas.')

np.save(PATH + '/Histogramas/Hist_{}'.format(n), H)
