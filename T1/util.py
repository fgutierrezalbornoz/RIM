# CC5213 - TAREA 1 - RECUPERACIÓN DE INFORMACIÓN MULTIMEDIA
# Fecha: 27 de marzo de 2025
# Alumno: Francisco Gutiérrez Albornoz

# Este archivo es usado por tarea1-parte1.py y tarea1-parte2.py
# Permite tener funciones compartidas entre ambos programas

# Se puede modificar este archivo para agregar más funciones (si es necesario)
# Incluir este archivo en la entrega de la tarea si fue modificado.

import os
import pickle
import cv2
import numpy
import time
import pandas

# Retorna todos los archivos que terminan con el parametro extension
# ejemplo: listar_archivos_con_extension(dir, ".jpg") retorna los archivos en dir cuyo nombre termina con .jpg
def listar_archivos_con_extension(carpeta, extension):
    lista = []
    for archivo in os.listdir(carpeta):
        # los que terminan con la extension se agregan a la lista de nombres
        if archivo.endswith(extension):
            lista.append(archivo)
    lista.sort()
    return lista


# escribe el objeto de python en un archivo binario
def guardar_objeto(objeto, carpeta, nombre_archivo):
    if carpeta == "" or carpeta == "." or carpeta is None:
        archivo = nombre_archivo
    else:
        archivo = os.path.join(carpeta, nombre_archivo)
        # asegura que la carpeta exista
        os.makedirs(carpeta, exist_ok=True)
    # usa la librería pickle para escribir el objeto en un archivo binario
    # ver https://docs.python.org/3/library/pickle.html
    with open(archivo, 'wb') as handle:
        pickle.dump(objeto, handle, protocol=pickle.HIGHEST_PROTOCOL)


# reconstruye el objeto de python que está guardado en un archivo
def leer_objeto(carpeta, nombre_archivo):
    if carpeta == "" or carpeta == "." or carpeta is None:
        archivo = nombre_archivo
    else:
        archivo = os.path.join(carpeta, nombre_archivo)
    with open(archivo, 'rb') as handle:
        objeto = pickle.load(handle)
    return objeto


# Recibe una lista de listas y lo escribe en un archivo separado por \t
# Por ejemplo:
# listas = [
#           ["dato1a", "dato1b", "dato1c"],
#           ["dato2a", "dato2b", "dato2c"],
#           ["dato3a", "dato3b", "dato3c"] ]
# al llamar:
#   escribir_lista_de_columnas_en_archivo(listas, "archivo.txt")
# escribe un archivo de texto con:
# dato1a  dato1b   dato1c
# dato2a  dato2b   dato3c
# dato2a  dato2b   dato3c
def escribir_lista_de_columnas_en_archivo(lista_con_columnas, archivo_texto_salida):
    with open(archivo_texto_salida, 'w') as handle:
        for columnas in lista_con_columnas:
            textos = []
            for col in columnas:
                textos.append(str(col))
            texto = "\t".join(textos)
            print(texto, file=handle)

#función entregada en material del curso
def calcular_descriptores(funcion_descriptor, nombres_imagenes, imagenes_dir):
    matriz_descriptores = None
    num_fila = 0
    t0 = time.time()
    for nombre_imagen in nombres_imagenes:
        descriptor_imagen = funcion_descriptor(nombre_imagen, imagenes_dir)
        # crear la matriz de descriptores (numero imagenes x largo_descriptor)
        if matriz_descriptores is None:
            matriz_descriptores = numpy.zeros((len(nombres_imagenes), len(descriptor_imagen)), numpy.float32)
        # copiar descriptor a una fila de la matriz de descriptores
        matriz_descriptores[num_fila] = descriptor_imagen
        num_fila += 1
    return matriz_descriptores

#calcula el descriptor vector de intensidades considerando una imagen y su espejo horizontal
def vector_de_intensidades(nombre_imagen, imagenes_dir):
    archivo_imagen = imagenes_dir + "/" + nombre_imagen
    imagen = cv2.imread(archivo_imagen, cv2.IMREAD_GRAYSCALE)
    imagen_flip = cv2.flip(imagen, 1)
    if imagen is None:
        raise Exception("no puedo abrir: " + archivo_imagen)
    
    imagen_reducida = cv2.resize(imagen, (10, 10), interpolation=cv2.INTER_CUBIC)
    imagen_reducida_flip = cv2.resize(imagen_flip, (10, 10), interpolation=cv2.INTER_CUBIC)
    # flatten convierte una matriz de nxm en un array de largo nxm

    descriptor_imagen = imagen_reducida.flatten()
    descriptor_imagen_flip = imagen_reducida_flip.flatten()
    return numpy.maximum(descriptor_imagen, descriptor_imagen_flip) / 255.0


# función entregada en material del curso
def imprimir_cercanos(lista_nombres, lista_nombres2, matriz_distancias):
    # completar la diagonal con un valor muy grande para que el mas cercano no sea si mismo
    numpy.fill_diagonal(matriz_distancias, numpy.inf)

    # obtener la posicion del mas cercano por fila
    posiciones_minimas = numpy.argmin(matriz_distancias, axis=1)
    valores_minimos = numpy.amin(matriz_distancias, axis=1)

    tabla_resultados = []
    for i in range(len(matriz_distancias)):
        query = lista_nombres[i]
        distancia = valores_minimos[i]
        mas_cercano = lista_nombres2[posiciones_minimas[i]]
        tabla_resultados.append([query, mas_cercano, distancia])

    df = pandas.DataFrame(tabla_resultados, columns=["query", "más_cercana", "distancia"])
    return df.values.tolist()

#--------------------------------------------------------------------------


# funcion que divide un rango [0, max) en  intervalos.
# Por ej: limites(256, 2) -> [0, 128, 256] que define los rangos [0, 128) y [128, 256)
# Se usa para definir los rangos de cada bin de histograma o para dividir la imagen en zonas
def calcular_limites(maximo_no_incluido, cantidad):
    list = [round(maximo_no_incluido * i / cantidad) for i in range(cantidad)]
    list.append(maximo_no_incluido)
    return list

#funcion base para descriptores globales que se calculan por zonas rectangulares
def descriptor_por_zona_generico(imagen, num_zonas_x, num_zonas_y, funcion_descriptor_zona):
    descriptor = []
    limites_y = calcular_limites(imagen.shape[0], num_zonas_y)
    limites_x = calcular_limites(imagen.shape[1], num_zonas_x)
    for j in range(num_zonas_y):
        desde_y = limites_y[j]
        hasta_y = limites_y[j + 1]
        for i in range(num_zonas_x):
            desde_x = limites_x[i]
            hasta_x = limites_x[i + 1]
            # recortar la zona de la imagen a la que se calcula el descriptor
            zona = imagen[desde_y:hasta_y, desde_x:hasta_x]
            # recortar la zona imagen de visualizacion para mostrar el resultado del descriptor
            zona_mostrar = None
            # descriptor de la zona
            descriptor_zona = funcion_descriptor_zona(zona)
            # agregar descriptor de la zona al descriptor global
            descriptor.extend(descriptor_zona)
    return descriptor

def color_de_cada_bin_3d(cantidad_bins):
    limites_dim = calcular_limites(256, cantidad_bins)
    colores_bins = []
    for i in range(cantidad_bins):
        val1 = round((limites_dim[i] + limites_dim[i + 1] - 1) / 2)
        for j in range(cantidad_bins):
            val2 = round((limites_dim[j] + limites_dim[j + 1] - 1) / 2)
            for k in range(cantidad_bins):
                val3 = round((limites_dim[k] + limites_dim[k + 1] - 1) / 2)
                colores_bins.append((val1, val2, val3))
    return colores_bins
                    
def histograma_3d(imagen_zona):
    global cantidad_bins_3d
    hist = cv2.calcHist(images=[imagen_zona], channels=[0, 1, 2], mask=None, histSize=[cantidad_bins_3d,cantidad_bins_3d,cantidad_bins_3d], ranges=[0, 256, 0, 256, 0, 256])
    descriptor_zona = hist.flatten()
    descriptor_zona = descriptor_zona / numpy.sum(descriptor_zona)
    return descriptor_zona


def histograma_3d_por_zonas(imagen, imagenes_dir):
    global zonas_x_3d, zonas_y_3d
    archivo_imagen = cv2.imread(imagenes_dir + "/" + imagen, cv2.IMREAD_COLOR)
    descriptor_imagen = descriptor_por_zona_generico(archivo_imagen, zonas_x_3d, zonas_y_3d, histograma_3d)
    return descriptor_imagen


zonas_x_3d = 4
zonas_y_3d = 4
cantidad_bins_3d = 6