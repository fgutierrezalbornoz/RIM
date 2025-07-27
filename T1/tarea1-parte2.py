# CC5213 - TAREA 1 - RECUPERACIÓN DE INFORMACIÓN MULTIMEDIA
# Fecha: 27 de marzo de 2025
# Alumno: Francisco Gutiérrez Albornoz

import sys
import os
import util as util
import scipy
import numpy 

def tarea1_parte2(dir_input_imagenes_Q, dir_input_descriptores_R, file_output_resultados):
    if not os.path.isdir(dir_input_imagenes_Q):
        print("ERROR: no existe directorio {}".format(dir_input_imagenes_Q))
        sys.exit(1)
    elif not os.path.isdir(dir_input_descriptores_R):
        print("ERROR: no existe directorio {} (¿terminó bien tarea1-parte1.py?)".format(dir_input_descriptores_R))
        sys.exit(1)
    elif os.path.exists(file_output_resultados):
        print("ERROR: ya existe archivo {}".format(file_output_resultados))
        sys.exit(1)
    # Implementar la fase online

    # 1-calcular descriptores de Q para imágenes en dir_input_imagenes_Q
    imagenesQ = util.listar_archivos_con_extension(dir_input_imagenes_Q, 'jpg')
    desc_intensidades = util.calcular_descriptores(util.vector_de_intensidades, imagenesQ, dir_input_imagenes_Q)
    desc_color = util.calcular_descriptores(util.histograma_3d_por_zonas, imagenesQ, dir_input_imagenes_Q)
    p_color = 0.7
    p_intensidad = 0.3
    descriptoresQ = [numpy.concatenate((p_color * desc_color[i],p_intensidad * desc_intensidades[i])) for i in range(len(desc_color))]
    
    # 2-leer descriptores de R guardados en dir_input_descriptores_R
    descriptoresR = [util.leer_objeto(dir_input_descriptores_R, f'r{str(i).zfill(4)}_desc.bin') for i in range(1, len(os.listdir(dir_input_descriptores_R))+1)]
    
    # 3-para cada descriptor q localizar el mas cercano en R
    matriz_distancias = scipy.spatial.distance.cdist(descriptoresQ, descriptoresR, metric='cityblock')

    # 4-escribir en el archivo file_output_resultados un archivo con tres columnas separado por \t:

    listaDescR = util.listar_archivos_con_extension(dir_input_descriptores_R, 'bin')
    imagenesR = [i.split('_')[0] + '.jpg' for i in listaDescR]
    util.escribir_lista_de_columnas_en_archivo(util.imprimir_cercanos(imagenesQ, imagenesR, matriz_distancias), file_output_resultados)



# inicio de la tarea
if len(sys.argv) < 4:
    print("Uso: {}  dir_input_imagenes_Q  dir_input_descriptores_R  file_output_resultados".format(sys.argv[0]))
    sys.exit(1)

# lee los parametros de entrada
dir_input_imagenes_Q = sys.argv[1]
dir_input_descriptores_R = sys.argv[2]
file_output_resultados = sys.argv[3]

# ejecuta la tarea
tarea1_parte2(dir_input_imagenes_Q, dir_input_descriptores_R, file_output_resultados)
