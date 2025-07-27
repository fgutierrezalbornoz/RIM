# CC5213 - TAREA 2 - RECUPERACIÓN DE INFORMACIÓN MULTIMEDIA
# Fecha: 08 de mayo de 2025
# Alumno: Francisco Gutiérrez Albornoz

import sys
import os
import util as util
import scipy
import numpy

def tarea2_parte2(carpeta_descriptores_radio_Q, carpeta_descritores_canciones_R, carpeta_salida_ventanas_similares):
    if not os.path.isdir(carpeta_descriptores_radio_Q):
        print("ERROR: no existe carpeta {}".format(carpeta_descriptores_radio_Q))
        sys.exit(1)
    elif not os.path.isdir(carpeta_descritores_canciones_R):
        print("ERROR: no existe carpeta {}".format(carpeta_descritores_canciones_R))
        sys.exit(1)
    elif os.path.exists(carpeta_salida_ventanas_similares):
        print("ERROR: ya existe {}".format(carpeta_salida_ventanas_similares))
        sys.exit(1)
    #
    # Implementar la tarea con los siguientes pasos:
    #
    #  1-leer descriptores de Q y R: datos en carpeta_descriptores_radio_Q y carpeta_descritores_canciones_R
    #     esas carpetas fueron creadas por tarea2_parte1
    #     puede servir la funcion util.leer_objeto() que está definida en util.py
    #
    descriptores_R = []
    nombres_R = []
    descriptores_Q = []
    nombres_Q = []
    #lecturas de archivos R
    for archivo_R in os.listdir(carpeta_descritores_canciones_R):
        if archivo_R != 'audios_temporales':
            nombres_R.append(archivo_R) #guardo el nombre del archivo en una lista
            descriptores_R.append(util.leer_objeto(carpeta_descritores_canciones_R, archivo_R)) #guardo el descriptor leído en otra lista
    #lecturas de archivos Q
    for archivo_Q in os.listdir(carpeta_descriptores_radio_Q):
        if archivo_Q != 'audios_temporales':
            nombres_Q.append(archivo_Q)
            descriptores_Q.append(util.leer_objeto(carpeta_descriptores_radio_Q, archivo_Q))

    #  2-para cada descriptor de Q localizar el más cercano en R
    #     se puede usar cdist como en la tarea 1
    #
    matriz_distancias = scipy.spatial.distance.cdist(descriptores_Q, descriptores_R, metric='cityblock')

    #  3-crear la carpeta carpeta_salida_ventanas_similares
    #     guardar un archivo que asocie cada ventana de Q con su ventana más parecida en R
    #     tambien guardar el nombre del archivo y los tiempos de inicio y fin que representa cada ventana de Q y R
    #     puede servir la funcion util.guardar_objeto() que está definida en util.py
    #
    os.makedirs(carpeta_salida_ventanas_similares, exist_ok=True) #crea la carpeta

    posicion_min = numpy.argmin(matriz_distancias, axis=1)
    minimo = numpy.min(matriz_distancias, axis=1)
    resultados = []
    ventanas_Q = util.lista_ventanas(nombres_Q, len(descriptores_Q), 44100, 4096, nombres_Q)
    ventanas_R = util.lista_ventanas(nombres_R, len(descriptores_R), 44100, 4096, nombres_R)

    for i, indice in enumerate(posicion_min):
        ventana_Q = ventanas_Q[i]
        ventana_R = ventanas_R[indice]
        distancia = minimo[i]
        resultados.append([
            ventana_Q.nombre_archivo, 
            round(ventana_Q.segundos_desde, 3),
            round(ventana_Q.segundos_hasta, 3),
            ventana_R.nombre_archivo, 
            round(ventana_R.segundos_desde, 3),
            round(ventana_R.segundos_hasta, 3),
            round(distancia, 3)
        ]) #resultado que indica el R más cercado a cada Q y su distancia 

    #guardado de los resultados
    archivo_resultados = os.path.join(carpeta_salida_ventanas_similares, "ventanas_similares")
    util.escribir_lista_de_columnas_en_archivo(resultados, archivo_resultados)
    util.guardar_objeto(resultados, carpeta_salida_ventanas_similares, "ventanas_similares.bin")

# inicio de la tarea
if len(sys.argv) != 4:
    print(
        "Uso: {} [carpeta_descriptores_radio_Q] [carpeta_descritores_canciones_R] [carpeta_salida_ventanas_similares]".format(
            sys.argv[0]))
    sys.exit(1)

# lee los parametros de entrada
carpeta_descriptores_radio_Q = sys.argv[1]
carpeta_descritores_canciones_R = sys.argv[2]
carpeta_salida_ventanas_similares = sys.argv[3]

# llamar a la tarea
tarea2_parte2(carpeta_descriptores_radio_Q, carpeta_descritores_canciones_R, carpeta_salida_ventanas_similares)
