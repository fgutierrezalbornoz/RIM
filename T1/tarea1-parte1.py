# CC5213 - TAREA 1 - RECUPERACIÓN DE INFORMACIÓN MULTIMEDIA
# Fecha: 27 de marzo de 2025
# Alumno: Francisco Gutiérrez Albornoz

import sys
import os
import util as util
import auxiliar
import threading
import numpy as np

def tarea1_parte1(dir_input_imagenes_R, dir_output_descriptores_R):
    if not os.path.isdir(dir_input_imagenes_R):
        print("ERROR: no existe directorio {}".format(dir_input_imagenes_R))
        sys.exit(1)
    elif os.path.exists(dir_output_descriptores_R):
        print("ERROR: ya existe directorio {}".format(dir_output_descriptores_R))
        sys.exit(1)
    # Implementar la fase offline

    # 1-leer imágenes en dir_input_imagenes
    imagenes = util.listar_archivos_con_extension(dir_input_imagenes_R, 'jpg')

    # 2-calcular descriptores de imágenes
    descriptores_intensidades = util.calcular_descriptores(util.vector_de_intensidades, imagenes, dir_input_imagenes_R)
    desc_color = util.calcular_descriptores(util.histograma_3d_por_zonas, imagenes, dir_input_imagenes_R)
    
    # 3-escribir en dir_output_descriptores_R los descriptores calculados en uno o más archivos
    
    #ponderación para que el descriptor de color tenga más peso.
    p_color = 0.7
    p_intensidad = 0.3
    for i in range(1, len(desc_color)+1):
        util.guardar_objeto(np.concatenate((p_color * desc_color[i-1],p_intensidad * descriptores_intensidades[i-1])), 
                            dir_output_descriptores_R, f'r{str(i).zfill(4)}_desc.bin')
        
# inicio de la tarea
if len(sys.argv) < 3:
    print("Uso: {}  dir_input_imagenes_R  dir_output_descriptores_R".format(sys.argv[0]))
    sys.exit(1)

# lee los parametros de entrada
dir_input_imagenes_R = sys.argv[1]
dir_output_descriptores_R = sys.argv[2]

# ejecuta la tarea
tarea1_parte1(dir_input_imagenes_R, dir_output_descriptores_R)
