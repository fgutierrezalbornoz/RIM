# CC5213 - TAREA 2 - RECUPERACIÓN DE INFORMACIÓN MULTIMEDIA
# Fecha: 08 de mayo de 2025
# Alumno: Francisco Gutiérrez Albornoz

# Este archivo es usado en tarea2-parte1.py, tarea2-parte2.py y tarea2-parte3.py
# Permite tener funciones compartidas entre los programas

# Se puede modificar este archivo para agregar más funciones (si es necesario)
# Incluir este archivo en la entrega de la tarea si fue modificado.

import os
import pickle
import subprocess
import librosa
import numpy 
import re
# funcion que recibe un nombre de archivo y llama a FFmpeg para crear un archivo wav
# requiere que el comando ffmpeg esté disponible
def convertir_a_wav(archivo_audio, sample_rate, dir_temporal):
    archivo_wav = os.path.join(dir_temporal, "{}.{}.wav".format(os.path.basename(archivo_audio), sample_rate))
    if os.path.isfile(archivo_wav):
        return archivo_wav
    os.makedirs(dir_temporal, exist_ok=True)
    comando = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-i", archivo_audio, "-ac", "1", "-ar", str(sample_rate),
               archivo_wav]
    code = subprocess.call(comando)
    if code != 0:
        raise Exception("ERROR en comando: " + " ".join(comando))
    return archivo_wav


# Retorna todos los archivos que terminan con el parametro extension
# ejemplo: listar_archivos_con_extension(dir, ".m4a") retorna los archivos en carpeta cuyo nombre termina con .m4a
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
        # print(archivo)
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

###################################################################################
# funciones agregadas (todas fueron sacadas del material docente y levemente modificadas)
###################################################################################
def convertir_a_wav(filename, sample_rate, carpeta_temporal):
    archivo_wav = "{}/{}.{}.wav".format(carpeta_temporal, os.path.basename(filename), sample_rate) 
    if os.path.isfile(archivo_wav):
        return archivo_wav
    os.makedirs(carpeta_temporal, exist_ok=True)
    # print("convertir {} a {}  samplerate {}".format(filename, archivo_wav, sample_rate))
    comando = ["ffmpeg", "-i", filename, "-ac", "1", "-ar", str(sample_rate), archivo_wav]
    # print("  COMANDO: {}".format(" ".join(comando)))
    with open(os.devnull, 'w') as devnull:
        code = subprocess.call(comando, stderr=devnull)
    if code != 0:
        raise Exception("ERROR en comando: " + " ".join(comando))
    return archivo_wav

    
def calcular_descriptores_mfcc(archivo_wav, sample_rate, samples_por_ventana, samples_salto, dimension):
    # leer audio
    samples, sr = librosa.load(archivo_wav, sr=None)
    # print("audio samples={} samplerate={} segundos={:.1f}".format(len(samples), sr, len(samples) / sr))
    # calcular MFCC
    mfcc = librosa.feature.mfcc(y=samples, sr=sr, n_mfcc=dimension, n_fft=samples_por_ventana, hop_length=samples_salto)
    # convertir a descriptores por fila
    mfcc_sin_volumen_global = mfcc[1:, :]
    descriptores = mfcc_sin_volumen_global.transpose()
    # en el descriptor MFCC la primera dimensión está relacionada al volumen global del audio (energía promedio)
    # usualmente es buena idea descartar la primera dimensión para tener descriptores invariantes al volumen global
    return descriptores


def calcular_mfcc_archivo(archivo_audio, sample_rate, samples_por_ventana, samples_salto, dimension, carpeta_temporal):
    os.makedirs(carpeta_temporal+'/audios_temporales', exist_ok=True)
    archivo_wav = convertir_a_wav(archivo_audio, sample_rate, carpeta_temporal+'/audios_temporales')
    descriptores = calcular_descriptores_mfcc(archivo_wav, sample_rate, samples_por_ventana, samples_salto, dimension)
    return descriptores

class Ventana:
    def __init__(self, nombre_archivo, segundos_desde, segundos_hasta):
        self.nombre_archivo = nombre_archivo
        self.segundos_desde = segundos_desde
        self.segundos_hasta = segundos_hasta
    
    def __str__(self):
        nombre_corto = self.nombre_archivo.split('\\')[-1]
        return "{} [{:6.3f}-{:6.3f}]".format(nombre_corto, self.segundos_desde, self.segundos_hasta)
def lista_ventanas(nombre_archivo, numero_descriptores, sample_rate, samples_por_ventana, lista_nombres=None):
    # tantas ventanas como numero de descriptores
    tiempos = []
    for i in range(numero_descriptores):

        # Crear objeto Ventana
        if lista_nombres is None:
            segundos_desde = (i * samples_por_ventana) / sample_rate
            segundos_hasta = ((i + 1) * samples_por_ventana - 1) / sample_rate
            v = Ventana(nombre_archivo, segundos_desde, segundos_hasta)
        else:
            match = re.search(r'\[\s*(\d+\.\d+)\s*-\s*(\d+\.\d+)\s*\]', lista_nombres[i].strip())
            segundos_desde = float(match.group(1))
            segundos_hasta = float(match.group(2))
            v = Ventana(lista_nombres[i], segundos_desde, segundos_hasta)
        # Agregar a la lista
        tiempos.append(v)
    return tiempos


def calcular_mfcc_varios_archivos(lista_archivos, sample_rate, samples_por_ventana, samples_salto, dimension, carpeta_temporal):
    descriptores_mfcc = []
    descriptores_ventanas = []
    for nombre_archivo in lista_archivos:
        audio_mfcc = calcular_mfcc_archivo(nombre_archivo, sample_rate, samples_por_ventana, samples_salto, dimension, carpeta_temporal)
        audio_ventanas = lista_ventanas(nombre_archivo, audio_mfcc.shape[0], sample_rate, samples_por_ventana)
        # print("  descriptores: {}".format(audio_mfcc.shape))
        if len(descriptores_mfcc) == 0:
            descriptores_mfcc = audio_mfcc
        else:
            # agregar como filas
            descriptores_mfcc = numpy.vstack([descriptores_mfcc, audio_mfcc])
        # agregar al final
        descriptores_ventanas.extend(audio_ventanas)
    return descriptores_ventanas, descriptores_mfcc
   
def imprimir_ventanas(ventanas, mfcc, muestreo_ventanas=1):
    print("ventanas={} descriptores={}".format(len(ventanas), mfcc.shape))
    print("mostrando algunas ventanas:")
    for i in range(0, len(ventanas), muestreo_ventanas):
        print(" {:4d}) {} descriptor={}".format(i, ventanas[i], mfcc[i].shape))


class Votos:
    def __init__(self, name, query, conocido):
        self.name = name
        self.query_nombre = query.nombre_archivo
        self.query_inicio = query.segundos_desde
        self.query_fin = query.segundos_hasta
        self.conocido_nombre = conocido.nombre_archivo
        self.conocido_inicio = conocido.segundos_desde
        self.conocido_fin = conocido.segundos_hasta
        self.numVotos = 1

    def addVoto(self, query, conocido):
        # muevo el final de la zona y sumo un voto
        self.query_fin = query.segundos_hasta
        self.conocido_fin = conocido.segundos_hasta
        self.numVotos += 1

    def __str__(self):
        return "{} entre [{:6.3f}-{:6.3f}]  se parece a  {} entre [{:6.3f}-{:6.3f}]  ({} votos)".format(
            self.query_nombre, self.query_inicio, self.query_fin, 
            self.conocido_nombre, self.conocido_inicio, self.conocido_fin,
            self.numVotos)