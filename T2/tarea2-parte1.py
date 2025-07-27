# CC5213 - TAREA 2 - RECUPERACIÓN DE INFORMACIÓN MULTIMEDIA
# Fecha: 08 de mayo de 2025
# Alumno: Francisco Gutiérrez Albornoz

import sys
import os
import util as util


def tarea2_parte1(carpeta_entrada_audios, carpeta_salida_descriptores):
    if not os.path.isdir(carpeta_entrada_audios):
        print("ERROR: no existe carpeta {}".format(carpeta_entrada_audios))
        sys.exit(1)
    elif os.path.exists(carpeta_salida_descriptores):
        print("ERROR: ya existe {}".format(carpeta_salida_descriptores))
        sys.exit(1)
    #
    # Implementar la tarea con los siguientes pasos:
    #
    #  1-leer los archivos con extension .m4a que están carpeta_entrada_audios
    #    puede servir la funcion util.listar_archivos_con_extension() que está definida en util.py
    archivos_audio = util.listar_archivos_con_extension(carpeta_entrada_audios, ".m4a")
    #
    #  2-convertir cada archivo de audio a wav (guardar los wav temporales en carpeta_salida_descriptores)
    #    puede servir la funcion util.convertir_a_wav() que está definida en util.py
    #
    sample_rate = 44100         #calidad del audio (44100 es HD, se puede bajar)
    samples_por_ventana = 4096  #tamaño de la ventana a la que se calcula un descriptor MFCC (usualmente unas 5 a 10 por segundo)
    samples_salto = 4096        #se puede probar con un  el salto es menor al tamaño de la ventana para que haya traslape entre ventanas
    dimension = 55              #largo del descriptor MFCC (usualmente entre 10 a 64)

    ruta_archivos_audio = [os.path.join(carpeta_entrada_audios, archivo) for archivo in archivos_audio]
    ventanas, mfcc = util.calcular_mfcc_varios_archivos(ruta_archivos_audio, sample_rate, samples_por_ventana, samples_salto, dimension, carpeta_salida_descriptores)
    for descriptor,ventana in zip(mfcc, ventanas):
        util.guardar_objeto(descriptor, carpeta_salida_descriptores, str(ventana))
  

# inicio de la tarea
if len(sys.argv) != 3:
    print("Uso: {} [carpeta_entrada_audios] [carpeta_salida_descriptores]".format(sys.argv[0]))
    sys.exit(1)

# lee los parametros de entrada
carpeta_entrada_audios = sys.argv[1]
carpeta_salida_descriptores = sys.argv[2]

# llamar a la tarea
tarea2_parte1(carpeta_entrada_audios, carpeta_salida_descriptores)
