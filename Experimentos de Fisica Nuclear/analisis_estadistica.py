import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import poisson, kstest
from scipy.optimize import curve_fit

'''

Este documento va a analizar las mediciones tomadas para la parte estadistica del informe. El fin es determinar
si la distribucion de la cantidad de cuentas totales que detecta el centellador es de Poisson. Para eso se va a hacer
un test de Kolmogorov-Smirnov. Antes de este analisis se separaron las mediciones que se
tomaron por 10 mins en intervalos de tiempos iguales para hacer estadistica. Eso se hizo en el documento
"separacion.py" y se guardaron los histogramas hechos en archivos de numpy .npy, en este programa simplemente
importamos esos arrays para analizar.

'''

#%% Contemos la cantidad de puntos en cada fotopico.

PATH = 'D:/Fede/UBA/6/Laboratorio 5/Experimentos de Fisica Nuclear/Histogramas'

# Importamos los histogramas con los intervalos que queramos analizar.
H = np.load(PATH + '/Hist_120.npy', allow_pickle=True)


# Esta funcion va a contar la cantidad de cuentas total de cada histograma.
def puntos(h):
    s = np.sum(h[0])
    return s


cuentas = []
for j in range(0, len(H)):
    cuentas.append(puntos(H[j]))
cuentas = np.asarray(cuentas)
cuentas = np.sort(cuentas)

n = len(cuentas)
promedio = np.mean(cuentas)
var = np.var(cuentas)

#%% Grafiquemos la distribucion empirica junto a la distribucion de poisson con el promedio como parametro y con un
# ajuste.

F = np.arange(1 / n, 1 + 1 / n, 1 / n)


def poisson_Fit(x, param):
    p = poisson.cdf(x, param)
    return p


lamb, lamb_err = curve_fit(poisson_Fit, cuentas, np.arange(1 / n, 1 + 1/n, 1 / n), p0=promedio)


def histogramar(dom, imag):
    dom = dom.tolist()
    res = []
    j = 0
    for i in range(np.min(dom), np.max(dom) + 1):
        if i in dom:
            res.append(imag[dom.index(i)])
            j = dom.index(i)
        else:
            res.append(imag[j])
    res = np.asarray(res)
    return res


Dom = np.arange(np.min(cuentas), np.max(cuentas) + 1)

plt.plot(Dom, histogramar(cuentas, F), '-', label='Distribución Empírica')
plt.plot(Dom, poisson_Fit(Dom, promedio), '-',
         label=r"Distribución de Poisson con $\lambda = \bar{X}_n$")
plt.plot(Dom, poisson_Fit(Dom, lamb[0]), '-', label="Ajuste de la distribución")
plt.grid()
plt.legend()
plt.xlabel('Cuentas')
plt.savefig('distribuciones_{}.png'.format(n))
plt.show()

#%% Hagamos un test de Kolmogorov-Smirnov. H0 seria que la distribucion es de Poisson (F = P).

# Elijamos el error tipo I a usar.
alpha = 0.01

# Hagamos el test.
D, p_value = kstest(cuentas, 'poisson', args=[lamb[0]])

if p_value < alpha:
    print('p_valor = ', p_value)
    print('{} < {}'.format(p_value, alpha))
    print('Rechazamos la hipotesis nula.')
else:
    print('p_valor = ', p_value)
    print('{} > {}'.format(p_value, alpha))
    print('No podemos rechazar la hipotesis nula.')
