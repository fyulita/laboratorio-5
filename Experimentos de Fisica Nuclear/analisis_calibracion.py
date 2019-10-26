import numpy as np
from scipy.io import loadmat
from scipy.signal import find_peaks
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

'''

El objetivo de este programa es calibrar los espectros de radiacion gamma que medimos con el centellador.

'''

#%% Importamos las mediciones hechas con matlab.

PATH = 'D:/Fede/UBA/6/Laboratorio 5/Experimentos de Fisica Nuclear'

print("Voy a importar las mediciones")

cesio0 = loadmat(PATH + "/Mediciones/cesio0.mat")
cesio0 = cesio0['data']
cesio0 = cesio0[:, 0]

cesio1 = loadmat(PATH + "/Mediciones/cesio1.mat")
cesio1 = cesio1['data']
cesio1 = cesio1[:, 0]

cesio2 = loadmat(PATH + "/Mediciones/cesio2.mat")
cesio2 = cesio2['data']
cesio2 = cesio2[:, 0]

cesio3 = loadmat(PATH + "/Mediciones/cesio3.mat")
cesio3 = cesio3['data']
cesio3 = cesio3[:, 0]

bario0 = loadmat(PATH + "/Mediciones/bario0.mat")
bario0 = bario0['data']
bario0 = bario0[:, 0]

bario1 = loadmat(PATH + "/Mediciones/bario1.mat")
bario1 = bario1['data']
bario1 = bario1[:, 0]

bismuto0 = loadmat(PATH + "/Mediciones/bismuto0.mat")
bismuto0 = bismuto0['data']
bismuto0 = bismuto0[:, 0]

bismuto1 = loadmat(PATH + "/Mediciones/bismuto1.mat")
bismuto1 = bismuto1['data']
bismuto1 = bismuto1[:, 0]

fondo = loadmat(PATH + "/Mediciones/fondo.mat")
fondo = fondo['data']
fondo = fondo[:, 0]

#%% Hacemos los histogramas y graficamos

umbral = 1      # V
t_sampleo = 120     # s
f_sampleo = 100000      # f

t = np.arange(0, t_sampleo, 1 / f_sampleo)


def hist(a):
    pks = find_peaks(a, umbral)
    pks_height = pks[1]['peak_heights']

    resolucion = np.min(np.diff(np.unique(a)))
    volt_range = np.arange(0, 10, resolucion * 100)
    h = np.histogram(pks_height, volt_range)

    return h


print("Voy a hacer los histogramas")

cesio0_hist = hist(cesio0)
cesio1_hist = hist(cesio1)
cesio2_hist = hist(cesio2)
cesio3_hist = hist(cesio3)
bario0_hist = hist(bario0)
bario1_hist = hist(bario1)
bismuto0_hist = hist(bismuto0)
bismuto1_hist = hist(bismuto1)
fondo_hist = hist(fondo)

print("Voy a graficar")

# Dividimos por 120 para que queden cuentas por segundo.
plt.figure('Sin calibrar')
plt.plot(cesio0_hist[1][:-1], cesio0_hist[0] / 120, 'o', label='Cs 0')
plt.plot(cesio1_hist[1][:-1], cesio1_hist[0] / 120, 'o', label='Cs 1')
plt.plot(cesio2_hist[1][:-1], cesio2_hist[0] / 120, 'o', label='Cs 2')
plt.plot(cesio3_hist[1][:-1], cesio3_hist[0] / 120, 'o', label='Cs 3')
plt.plot(bario0_hist[1][:-1], bario0_hist[0] / 120, 'o', label='Ba 0')
plt.plot(bario1_hist[1][:-1], bario1_hist[0] / 120, 'o', label='Ba 1')
plt.plot(bismuto0_hist[1][:-1], bismuto0_hist[0] / 120, 'o', label='Bi 0')
plt.plot(bismuto1_hist[1][:-1], bismuto1_hist[0] / 120, 'o', label='Bi 1')
plt.plot(fondo_hist[1][:-1], fondo_hist[0] / 120, 'o', label='Fondo')
plt.grid()
plt.legend()
plt.xlabel('Voltaje (V)')
plt.ylabel('cps')
plt.savefig('mediciones.png')
plt.show()

#%% Calibramos.


def fotopico(hist, i):
    array = hist[0][i:-1]
    m = np.max(array)
    l = (hist[0].tolist()).index(m)
    pico = hist[1][l]
    return pico


pico_cesio = fotopico(cesio0_hist, 0)
pico_bario = fotopico(bario0_hist, 0)
pico_bis_1 = fotopico(bismuto0_hist, 62)
pico_bis_2 = fotopico(bismuto0_hist, 153)

errV = 0.05      # Error de apreciacion para la tension en V.


def recta(x, a, b):
    y = a * x + b
    return y


picos_x = np.array([pico_bario, pico_bis_1, pico_cesio, pico_bis_2])
picos_y = np.array([356.017, 569.702, 661.657, 1063.662])       # Ver la pag web de donde sacamos estos valores.

popt, pcov = curve_fit(recta, picos_x, picos_y)

errores_cesio = np.sqrt((cesio0_hist[1][:-1] ** 2) * (18 ** 2) + 4 ** 2)
errores_bario = np.sqrt((bario0_hist[1][:-1] ** 2) * (18 ** 2) + 4 ** 2)
errores_bismuto = np.sqrt((bismuto0_hist[1][:-1] ** 2) * (18 ** 2) + 4 ** 2)

plt.figure('Calibrado')
plt.errorbar(recta(cesio0_hist[1][:-1], popt[0], popt[1]), cesio0_hist[0] / 120, 0, errores_cesio, 'o', label='Cs')
plt.errorbar(recta(bario0_hist[1][:-1], popt[0], popt[1]), bario0_hist[0] / 120, 0, errores_bario, 'o', label='Ba')
plt.errorbar(recta(bismuto0_hist[1][:-1], popt[0], popt[1]), bismuto0_hist[0] / 120, 0, errores_bismuto, 'o',
             label='Bi')
plt.grid()
plt.legend()
plt.xlabel('Energía (keV)')
plt.xlim([150, 1500])
plt.ylabel('cps')
plt.savefig('mediciones_calibradas.png')
plt.show()

# En escala logaritmica se ven mejor las mesetas de compton del cesio y del bismuto.
plt.figure('Calibrado LOG')
plt.errorbar(recta(cesio0_hist[1][:-1], popt[0], popt[1]), cesio0_hist[0] / 120, 0, errores_cesio, 'o',
             label='Cs')
plt.errorbar(recta(bario0_hist[1][:-1], popt[0], popt[1]), bario0_hist[0] / 120, 0, errores_bario, 'o',
             label='Ba')
plt.errorbar(recta(bismuto0_hist[1][:-1], popt[0], popt[1]), bismuto0_hist[0] / 120, 0, errores_bismuto, 'o',
             label='Bi')
plt.grid()
plt.legend()
plt.xlabel('Energía (keV)')
plt.xlim([150, 1500])
plt.ylabel('cps')
plt.xscale('log')
plt.savefig('mediciones_calibradas_LOG.png')
plt.show()
